from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_question = Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
        context['latest_question_list'] = latest_question
        return context

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'charts/results.html'

    def get_context_data(self, **kwargs):
        choice = kwargs['object'].choice_set
        questions = Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
        c = choice.reverse()
        context = {}
        context['values'] = []
        for i in range((len(c))):
            context['values'].append(
            [
                choice.get(pk=c[i].pk).choice_text,
                choice.get(pk=c[i].pk).votes
            ])
        context['latest_question_list'] = questions
        return context

def ResultSemanalView(request, slug):
    """
    Grafico Diario
    """
    segunda = [2,1,2,4,3,1,2,4,1]
    terca = [1,1,3,4,4,2,2,3,1]
    quarta = [2,2,3,4,3,2,2,3,2]
    quinta = [1,1,3,4,4,2,2,3,1]
    sexta = [1,1,3,4,4,2,2,3,1]
    sabado = [1,1,3,4,4,2,2,3,1]
    domingo = [1,1,3,4,4,2,2,3,1]
    if slug == 'segunda':
        dia = segunda
    elif slug == 'terca':
        dia = terca
    elif slug == 'quarta':
        dia = quarta
    elif slug == 'quinta':
        dia = quinta
    elif slug == 'sexta':
        dia = sexta
    elif slug == 'sabado':
        dia = sabado
    elif slug == 'domingo':
        dia = domingo

    context = [['7-8',dia[0]],
                        ['8-9',dia[1]],
                        ['11-12',dia[2]],
                        ['12-13',dia[3]],
                        ['13-14',dia[4]],
                        ['14-15',dia[5]],
                        ['17-18',dia[6]],
                        ['18-19',dia[7]],
                        ['19-20',dia[8]]
                        ]

    return render(
        request, 'charts/results.html',
        {
            'values': context,
            'dia': slug
        }
    )


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
