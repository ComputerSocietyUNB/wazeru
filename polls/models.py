import datetime
from datetime import date

from django.db import models
from django.utils import timezone

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.jobstores import register_events



def create_question(question_text, days=0):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


def create_choices(choice_map, question):
    """
    Create a map of choices and votes with the given `choice_map` and the
    given question of `question_pk`.
    """
    # print(choice_map.items())
    choices = []
    for choice, votes in choice_map.items():
        choices.append(Choice.objects.create(
            choice_text=choice,
            votes=votes,
            question=question
        ))
    return choices


def create_poll(question_text, choice_map, days=0):
    question = create_question(question_text=question_text, days=days)
    choices = create_choices(choice_map, question)
    return [question, choices]


class Question(models.Model):
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    def __str__(self):
        return self.choice_text

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
register_events(scheduler)

@scheduler.scheduled_job("interval", seconds=10, id="job")
def job():
    choice_map = {
        '<img src="{% static "img/happyface.png" %}" class="img-fluid" alt="Meh face"/>': 2,
        '<img src="{% static "img/okface.png" %}" class="img-fluid" alt="Meh face"/>': 3
    }
    create_poll("Como está o RU?" + strtime(), choice_map)
