from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.forms import inlineformset_factory
from .forms import NewQuestionForm, ChoiceForm
from .models import Question, Choice


# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            publish_date__lte=timezone.now()
        ).order_by('-publish_date')[:5]


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


def question_new(request):
    form = NewQuestionForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.publish_date = timezone.now()
            question.save()
            return HttpResponseRedirect(reverse('polls:add_choices', args=(question.id,)))
    else:
        form = NewQuestionForm(request.POST)

    context = {'form': form}
    return render(request, 'polls/new_question.html', context=context)

def add_choices(request, question_id):
    ChoiceFormSet = inlineformset_factory(Question, Choice, fields=('choice_text',), extra=5)
    question = get_object_or_404(Question, pk=question_id)
    formset = ChoiceFormSet(instance=question)
    if request.method == 'POST':
        formset = ChoiceFormSet(request.POST, instance=question)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('polls:detail', args=(question_id,)))

    context = {'formset':formset}
    return render(request, 'polls/add_choices.html' ,context=context)

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
        return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))
