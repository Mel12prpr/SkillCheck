from django.contrib import admin

from quizapp.models import Question, UserResponse, Quiz, Attempt

# Register your models here.

admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(UserResponse)
admin.site.register(Attempt)
