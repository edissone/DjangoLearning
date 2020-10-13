from django import forms
from extra_views import InlineFormSetFactory

from polls.models import Question, Choice


class VoteForm(forms.Form):
    def __init__(self, *args, **kwargs):
        question = Question.objects.get(pk=kwargs.pop('question_id'))
        super(VoteForm, self).__init__(*args, **kwargs)
        if question.choice_type == 'c':
            self.fields['choice'] = forms.ModelMultipleChoiceField(question.choice_set,
                                                                   widget=forms.CheckboxSelectMultiple)
        if question.choice_type == 'r':
            self.fields['choice'] = forms.ModelChoiceField(question.choice_set,
                                                           widget=forms.RadioSelect)
        else:
            self.fields['choice'] = forms.CharField(max_length=150, widget=forms.Textarea)

    class Meta:
        fields = ['choice', ]


class ChoiceInline(InlineFormSetFactory):
    model = Choice
    fields = ['choice_text']
    factory_kwargs = {"extra": 5, "can_delete": False}
