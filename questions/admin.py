from django.contrib import admin

from .models import Question, QuestionAnswer


admin.site.register(Question)

admin.site.register(QuestionAnswer)
