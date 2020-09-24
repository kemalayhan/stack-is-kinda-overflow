from django import forms

from .models import Question, QuestionAnswer
from tags.models import Tag
from crispy_forms.helper import FormHelper

class QuestionCreateForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = [
            'title', 'content', 'image', 'tag'
        ]


class QuestionAnswerForm(forms.ModelForm):

    class Meta:
        model = QuestionAnswer
        fields = ['content']

        widgets = {
            'content' : forms.Textarea(attrs={'rows':2})
        }