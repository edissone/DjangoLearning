from extra_views import InlineFormSetFactory

from polls.models import Choice


class ChoiceInline(InlineFormSetFactory):
    model = Choice
    fields = ['choice_text']
    factory_kwargs = {"extra": 5, "can_delete": False}
