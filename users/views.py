from django.views import generic


class UserProfileView(generic.DetailView):
    template_name = 'users/user_profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['questions'] = self.request.user.questions.all()
        return context
