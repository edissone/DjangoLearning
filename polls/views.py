from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.views import generic
from django.utils import timezone

from .forms import NewQuestionForm, ChoiceForm, ChoiceFormSet
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
    if request.method == 'POST':
        form = NewQuestionForm(request.POST)
        formset = ChoiceFormSet(request.POST)
        #TODO: FUCKED UP HERE
        if formset.is_valid() and form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.publish_date = timezone.now()
            question.save()
            for form_choice in formset:
                choice = form_choice.save(commit=False)
                choice.question = question
                choice.votes = 0
                choice.save()
            return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))
    else:
        form = NewQuestionForm(request.POST)
        formset = ChoiceFormSet
    return render(request, 'polls/new_question.html', {'form': form,'formset': formset})


'''def question_new(request):
    if request.method == 'POST':
        form = NewQuestionForm(request.POST)
        form_choice = ChoiceForm(request.POST)
        if form.is_valid() and form_choice.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.publish_date = timezone.now()
            question.save()

            choice = form_choice.save(commit=False)
            choice.question = question
            choice.votes = 0
            choice.save()

            return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))
    else:
        form = NewQuestionForm()
        form_choice = ChoiceForm()
    return render(request, 'polls/new_question.html', {'form': form, 'form_choice': form_choice})
'''

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
