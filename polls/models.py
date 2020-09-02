import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=155)
    publish_date = models.DateTimeField('date published')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.publish_date <= now

    was_published_recently.admin_order_field = 'publish_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=50)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
