from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django_bulk_update.helper import bulk_update
from extra_views import CreateWithInlinesView

from polls.forms import ChoiceInline, VoteForm, CommentForm
from polls.models import Question, Choice


# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    paginate_by = 10

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

    def get_object(self, **kwargs):
        return Question.objects.prefetch_related('choices', 'comments', 'comments__author',
                                                 'choices__votes').get(pk=self.kwargs['pk'])


class CreateQuestionFormView(CreateWithInlinesView):
    model = Question
    inlines = [ChoiceInline]
    template_name = 'polls/create_question.html'
    fields = ['question_text', 'description', 'image', 'choice_type']
    widgets = {
        'description': forms.Textarea(attrs={'rows': 5, 'cols': 10}),
        'image': forms.ImageField
    }

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.publish_date = timezone.now()
        form.instance.save()
        return HttpResponseRedirect(reverse('polls:vote', args=(form.instance.id,)))

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
        choices_list = []
        if isinstance(form.cleaned_data['choice'], Choice):
            choice = form.cleaned_data['choice']
            choice.votes.add(self.request.user)
            choices_list.append(choice)
        elif isinstance(form.cleaned_data['choice'], str):
            choice = Choice(question_id=self.kwargs['question_id'], choice_text=form.cleaned_data['choice'])
            choice.save()
            choice.votes.add(self.request.user)
        else:
            for choice in form.cleaned_data['choice']:
                choice.votes.add(self.request.user)
                choices_list.append(choice)
        bulk_update(choices_list)
        return HttpResponseRedirect(reverse('polls:results', args=(self.get_form_kwargs()['question_id'],)))


class CommentView(generic.FormView):
    template_name = 'polls/comment.html'
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.instance
        comment.question_id = self.kwargs['question_id']
        comment.author = self.request.user
        comment.publish_date = timezone.now()
        comment.save()
        return HttpResponseRedirect(reverse('polls:results', args=(self.kwargs['question_id'],)))
