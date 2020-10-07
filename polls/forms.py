from django import forms
from extra_views import InlineFormSetFactory

from polls.models import Question, Choice


class VoteForm(forms.Form):

    def __init__(self, *args, **kwargs):
        q_id = kwargs.pop('question_id')
        super(VoteForm, self).__init__(*args, **kwargs)
        self.fields['choice'] = forms.ModelMultipleChoiceField(Question.objects.get(pk=q_id).choice_set,
                                                               widget=forms.CheckboxSelectMultiple)

    class Meta:
        fields = ['choice', ]


class ChoiceInline(InlineFormSetFactory):
    model = Choice
    fields = ['choice_text']
    factory_kwargs = {"extra": 5, "can_delete": False}
