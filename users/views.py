from django.views import generic

from polls.models import Question


class UserProfileView(generic.DetailView):
    template_name = 'users/user_profile.html'
    context_object_name = 'user_questions'

    def get_queryset(self):
        return Question.objects.filter(author=self.request.user)