from django import forms
from extra_views import InlineFormSetFactory

from polls.models import Choice

# TODO: realize dynamic form for voting
class VoteForm(forms.Form):
    pass


class ChoiceInline(InlineFormSetFactory):
    model = Choice
    fields = ['choice_text']
    factory_kwargs = {"extra": 5, "can_delete": False}
