from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.QuizCreateView.as_view(), name='quiz_create'),

    # Generate questions view (with quiz_id as a parameter)
    path('take/<int:quiz_id>/', views.TakeQuiz.as_view(), name='take_quiz'),
    path('<int:quiz_id>/', views.QuizPreview.as_view(), name='quiz_preview'),
    path('quizzes/', views.QuizTemplateView.as_view(), name='quizzes'),
    path('<int:quiz_id>/attempts/', views.quiz_attempts, name='quiz_attempts'),
    path('my_attempts/', views.my_attempts, name='my_attempts'),
    path('attempt/<int:attempt_id>/', views.attempt, name='attempt'),
    path('not_allowed/', views.not_allowed, name='not_allowed'),
]



