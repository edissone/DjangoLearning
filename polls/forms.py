from django import forms
from extra_views import InlineFormSetFactory

from polls.models import Question, Choice, Comment


class VoteForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self._question = Question.objects.prefetch_related('choices', 'author').get(pk=kwargs.pop('question_id'))
        super(VoteForm, self).__init__(*args, **kwargs)
        if self._question.choice_type == Question.TYPE.multi:
            self.fields['choice'] = forms.ModelMultipleChoiceField(self._question.choices,
                                                                   widget=forms.CheckboxSelectMultiple)
        if self._question.choice_type == Question.TYPE.single:
            self.fields['choice'] = forms.ModelChoiceField(self._question.choices,
                                                           widget=forms.RadioSelect)
        else:
            self.fields['choice'] = forms.CharField(max_length=150, widget=forms.Textarea)

    class Meta:
        fields = ['choice', ]


class CommentForm(forms.ModelForm):
    text = forms.CharField(max_length=155, widget=forms.Textarea)

    class Meta:
        fields = ['text']
        model = Comment


class ChoiceInline(InlineFormSetFactory):
    model = Choice
    fields = ['choice_text']
    factory_kwargs = {"extra": 5, "can_delete": False}
