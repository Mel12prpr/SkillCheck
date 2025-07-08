from django import forms
from .models import Quiz, UserResponse

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['topic', 'num_questions', 'focus_area' , 'difficulty']  # Include fields that the user will fill out
        widgets = {
            'focus_area': forms.Textarea(attrs={'rows': 4, 'cols': 50}),  # Custom widget for the description field
        }

class QuestionGenerationForm(forms.Form):
    # Form to allow the user to enter a 'focus_area' to generate questions
    focus_area = forms.CharField(max_length=100, required=False, label="Focus Area")


class TakeQuizForm(forms.Form):
    def __init__(self, questions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for question in questions:
            self.fields[f'question_{question.id}'] = forms.CharField(
                label=question.question_text,
                widget=forms.Textarea(attrs={
                    'class': 'form-control',
                    'rows': 3
                }),
                required=False
            )
