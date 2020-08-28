from django import forms
from django.forms import formset_factory

from .models import Question, Choice

class NewQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_text',)

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ('choice_text',)

