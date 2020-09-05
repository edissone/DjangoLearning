from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from extra_views import CreateWithInlinesView
from polls.forms import ChoiceInline
from polls.models import Question, Choice
from django.contrib.auth.models import User


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
    fields = ['question_text']
    template_name = 'polls/create_question.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.publish_date = timezone.now()
        form.instance.save()
        return HttpResponseRedirect(reverse('polls:detail', args=(form.instance.id,)))

    def get_success_url(self):
        return self.object.get_absolute_url()


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
