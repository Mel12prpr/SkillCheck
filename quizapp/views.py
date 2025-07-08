from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.views import View
from django.views.generic import TemplateView
from rest_framework.views import APIView
from .models import Quiz, Question, Attempt, UserResponse
from .serializers import QuizSerializer, QuestionSerializer
from utils.serializer_factory import SerializerGetter
from django.shortcuts import render, redirect
from .forms import QuizForm, QuestionGenerationForm, TakeQuizForm
from django.contrib.auth.decorators import login_required
import openai
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='.env')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

serializer_getter = SerializerGetter(
    default=QuizSerializer,
    create=QuizSerializer,
    generate_questions=QuestionSerializer,
)


def home(request):
    quizzes = Quiz.objects.all()
    # could be sorted by popularity after adding attempt model
    # could be filtered by categories after adding category model
    return render(request, 'home/index.html', {'quizzes': quizzes})


def about(request):
    return render(request, 'home/about.html')


# Quiz creation view

class QuizCreateView(LoginRequiredMixin, View):
    login_url = '/user/login/'

    def get(self, request):
        form = QuizForm()
        return render(request, 'quizapp/quiz_create.html', {'form': form})

    def post(self, request):
        form = QuizForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['num_questions'] > 20:
                form.add_error('num_questions', 'The maximum number of questions allowed is 20.')
                return render(request, 'quizapp/quiz_create.html', {'form': form})
            quiz = form.save(commit=False)
            quiz.creator = request.user
            quiz.save()

            focus_area = form.cleaned_data['focus_area']
            num_questions = form.cleaned_data['num_questions']
            difficulty = form.cleaned_data['difficulty']
            prompt = (
                f"Generate {num_questions} short open-ended questions on the topic '{quiz.topic}', "
                f"focusing on '{focus_area}' with difficulty '{difficulty}'. "
                "Each question should be one simple sentence, 20 words max. "
                "Return only the questions, numbered from 1 to N, no extra text or commentary."
            )

            response = openai.ChatCompletion.create(
                model="gpt-4o",


            messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100 * num_questions
            )
            question_texts = response['choices'][0]['message']['content'].strip().split("\n")
            questions = []
            for question_text in question_texts:
                if not question_text:
                    continue
                question = Question.objects.create(
                    quiz=quiz,
                    question_text=question_text,
                    focus_area=focus_area
                )
                questions.append(question)

            question_data = QuestionSerializer(questions, many=True).data

            # Render the generated questions template with serialized data
            return render(request, 'quizapp/questions_generated.html', {
                'questions': question_data,
                'quiz': quiz
            })

        return render(request, 'quizapp/quiz_create.html', {'form': form})


class TakeQuiz(LoginRequiredMixin,APIView):
    login_url = '/user/login/'

    def get(self, request, quiz_id):
        quiz = Quiz.objects.get(id=quiz_id)
        questions = Question.objects.filter(quiz_id=quiz_id)
        form = TakeQuizForm(questions)
        return render(request, 'quizapp/take_quiz.html', {'quiz': quiz, 'questions': questions, 'form': form})

    def post(self, request, quiz_id):
        questions = Question.objects.filter(quiz_id=quiz_id)
        form = TakeQuizForm(questions, request.POST)

        if form.is_valid():
            user_responses = form.cleaned_data
            mark = 0
            for_context = []
            quiz = Quiz.objects.get(id=quiz_id)
            attempt = Attempt.objects.create(quiz=quiz, user=request.user, score=0)
            for question_id, user_response in user_responses.items():

                question_id = int(question_id.split('_')[1])
                question = questions.get(id=question_id)
                if not user_response.strip():
                    correctness = 0
                    prompt = (
                        f"Question: {question.question_text}\n"
                        ", provide the correct answer in this format: '- [correct answer]'."
                    )
                    response = openai.ChatCompletion.create(
                        model="gpt-4o",

                    messages=[{
                            "role": "user",
                            "content": prompt
                        }],
                        max_tokens=100
                    )

                    correct_answer = response["choices"][0]["message"]["content"].strip()
                    for_context.append((question, '', correctness, correct_answer))
                    UserResponse.objects.create(
                        question=question,
                        user=request.user,
                        answer=user_response,
                        is_correct=False,
                        attempt=attempt
                    )
                    continue
                if question:
                    prompt = (
                        f"Question: {question.question_text}\n"
                        f"Answer: {user_response}\n"
                        "Is this answer correct? Reply 'Yes' or 'No'. If incorrect or no answer, provide the correct answer in this format: 'No - [correct answer]'."
                    )
                    response = openai.ChatCompletion.create(
                        model="gpt-4o",

                    messages=[{
                            "role": "user",
                            "content": prompt
                        }],
                        max_tokens=100
                    )

                    result = response["choices"][0]["message"]["content"]
                    print(response)
                    print(result)
                    if result.lower().startswith("yes"):
                        mark += 1
                        correctness = 1
                        correct_answer = None
                    elif result.lower().startswith("no"):
                        correctness = 0
                        correct_answer = result.split("-")[1].strip() if "-" in result else None
                    else:
                        correctness = 0
                        correct_answer = None
                    for_context.append((question, user_response, correctness, correct_answer))
                    UserResponse.objects.create(
                        question=question,
                        user=request.user,
                        answer=user_response,
                        is_correct=correctness == 1,
                        attempt=attempt
                    )
            attempt.score = mark
            attempt.save()
            context = {
                'mark': mark,
                'total': len(questions),
                'questions': for_context,
                'quiz': Quiz.objects.get(id=quiz_id)
            }
            return render(request, 'quizapp/quiz_result.html', context)

        return redirect('home')


class QuizPreview(APIView):
    def get(self, request, quiz_id):
        quiz = Quiz.objects.get(id=quiz_id)
        return render(request, 'quizapp/quiz_preview.html', {'quiz': quiz, 'num': len(quiz.questions.all())})


@login_required(login_url='/user/login/')
def my_quizzes(request):
    # Fetch all quizzes from the database
    quizzes = Quiz.objects.filter(creator=request.user.id).prefetch_related('attempts')
    return render(request, 'home/my_quizzes.html', {'quizzes': quizzes})


class QuizTemplateView(TemplateView):
    template_name = 'home/quizzes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        difficulty = self.request.GET.get('difficulty')
        num_questions = self.request.GET.get('num_questions')
        quizzes = Quiz.objects.all()
        if difficulty:
            quizzes = quizzes.filter(difficulty__iexact=difficulty)
        if num_questions:
            try:
                quizzes = quizzes.filter(num_questions__gte=int(num_questions))
            except ValueError:
                pass
        paginator = Paginator(quizzes, 2)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['quizzes'] = quizzes
        context['page_obj'] = page_obj
        return context


@login_required(login_url='/user/login/')
def quiz_attempts(request, quiz_id):
    quiz = Quiz.objects.prefetch_related('attempts').get(id=quiz_id)
    if quiz.creator != request.user:
        return redirect('not_allowed')
    return render(request, 'quizapp/attempts_on_quiz.html', {'quiz': quiz})


@login_required(login_url='/user/login/')
def my_attempts(request):
    attempts = Attempt.objects.filter(user=request.user)
    return render(request, 'home/my_attempts.html', {'attempts': attempts})


@login_required(login_url='/user/login/')
def attempt(request, attempt_id):
    attmpt = Attempt.objects.prefetch_related('responses').get(id=attempt_id)
    if attmpt.user != request.user:
        return redirect('/home/not_allowed')
    return render(request, 'quizapp/attempt.html', {'attempt': attmpt})


def not_allowed(request):
    return render(request, 'home/not_allowed.html')
