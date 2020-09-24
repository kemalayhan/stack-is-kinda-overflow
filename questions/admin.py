from django.contrib import admin

from .models import Question, QuestionAnswer, QuestionVote, AnswerVote


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    class Meta:
        model = Question
        list_display = ['content', 'created_date']

admin.site.register(QuestionAnswer)
admin.site.register(QuestionVote)
admin.site.register(AnswerVote)

