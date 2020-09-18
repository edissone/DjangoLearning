from django import forms
from extra_views import InlineFormSetFactory

from polls.models import Choice


# TODO: realize dynamic form for voting
class VoteForm(forms.ModelForm):
    model = Choice

    def __init__(self, initial=None, prefix=None):
        choice_set = Choice.objects.filter()
        choices = []
        for i in choice_set:
            choices.append((f'{i.id}', f'{i.choice_text}'))
        self.choice = forms.IntegerField(widget=forms.widgets.RadioSelect, choices=choices)


class ChoiceInline(InlineFormSetFactory):
    model = Choice
    fields = ['choice_text']
    factory_kwargs = {"extra": 5, "can_delete": False}
