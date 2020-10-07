from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from extra_views import CreateWithInlinesView

from polls.forms import ChoiceInline, VoteForm
from polls.models import Question, Choice


# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    paginate_by = 2

    def get_queryset(self):
        return Question.objects.get_queryset().order_by('id')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(publish_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


class CreateQuestionFormView(CreateWithInlinesView):
    model = Question
    inlines = [ChoiceInline]
    template_name = 'polls/create_question.html'
    fields = ['question_text', 'image', 'choices_type']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.publish_date = timezone.now()
        form.instance.save()
        return HttpResponseRedirect(reverse('polls:detail', args=(form.instance.id,)))

    def get_success_url(self):
        return self.object.get_absolute_url()


class ChoiceVoteView(generic.FormView):
    template_name = 'polls/vote.html'
    form_class = VoteForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs().copy()
        kwargs.update({"question_id": self.kwargs['question_id']})
        return kwargs

    def form_valid(self, form):
        for choice in form.cleaned_data['choice']:
            choice.votes += 1
            choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(self.get_form_kwargs()['question_id'],)))
