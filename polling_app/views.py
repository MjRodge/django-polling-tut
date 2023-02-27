from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polling_app/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """return th last 5 published question"""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polling_app/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polling_app/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polling_app/detail.html', {
            'question': question,
            'error_message': "you didn't select an option.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polling_app:results', args=(question.id, )))

