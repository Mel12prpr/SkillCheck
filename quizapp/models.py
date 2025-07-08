from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quizzes")
    topic = models.CharField(max_length=255)
    focus_area = models.CharField(max_length=100)
    num_questions = models.PositiveIntegerField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    focus_area = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class UserResponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="responses")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.TextField()
    is_correct = models.BooleanField(null=True)
    attempt = models.ForeignKey('Attempt', on_delete=models.CASCADE, related_name="responses")


class Attempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)
