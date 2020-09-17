from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from extra_views import CreateWithInlinesView

from polls.forms import ChoiceInline
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
    context_object_name = 'choices_list'

    def get_queryset(self):
        return Choice.objects.order_by('votes')


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
    error_msg = ""
    model = Question
    template_name = 'poll/detail.html'
    context_object_name = 'question'

    def get_object(self):
        return self.request.question

    def get_context_data(self, **kwargs):
        context = super(ChoiceVoteView, self).get_context_data(**kwargs)
        context['error_message'] = self.error_msg

    def get_choices(self):
        return self.object.choice_set.get(pk=self.request.POST['choice'])

    def form_valid(self, form):
        form.instance.votes += 1
        form.instance.save()
        return HttpResponseRedirect(reverse('polls:results', args=(self.object.id,)))
