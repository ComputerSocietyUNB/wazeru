from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[0]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_question = get_latest_question()
        media_votes = media(latest_question)
        context['media_votos'] = media_votes
        return context


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_question = get_latest_question()
        context['latest_question'] = latest_question
        return context

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'charts/results.html'

    def get_context_data(self, **kwargs):
        question = kwargs['object']
        choice = question.choice_set
        c = choice.reverse()
        context = {}
        context['values'] = []
        for i in range((len(c))):
            context['values'].append(
            [
                choice.get(pk=c[i].pk).choice_text,
                choice.get(pk=c[i].pk).votes
            ])
        context['latest_question'] = question
        context['media_votos'] = media(question)
        return context

def ResultSemanalView(request, slug):
    context = {}
    question = get_latest_question()
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

    context_graph = [['7-8',dia[0]],
                        ['8-9',dia[1]],
                        ['11-12',dia[2]],
                        ['12-13',dia[3]],
                        ['13-14',dia[4]],
                        ['14-15',dia[5]],
                        ['17-18',dia[6]],
                        ['18-19',dia[7]],
                        ['19-20',dia[8]]
                        ]
    context['values'] = context_graph
    context['dia'] = slug
    context['latest_question'] = question

    return render(
        request, 'charts/results.html',
        context
    )

def semanal_template(request):
    question = get_latest_question()
    context = {}
    context['latest_question'] = question
    return render(
        request, 'polls/semanal.html',
        context
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


def get_latest_question():
    return Question.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')[0]


def media(question):
    choices_set = question.choice_set
    vote_peso = 0
    vote_qtd = 0
    media_votes = 0
    for choice in choices_set.all().order_by('id'):
        media_votes += (vote_peso * choice.votes)
        vote_peso += 1
        vote_qtd += choice.votes
    media_votes = media_votes/vote_qtd
    if media_votes == 0:
        media_votes = 2
    return (10*media_votes)/10
