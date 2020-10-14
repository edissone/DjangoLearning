import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
from config.settings import MEDIA_URL


class Question(models.Model):
    CHOICES_TYPE = [
        ('t', 'Text field'),
        ('c', 'Multiple'),
        ('r', 'Single')
    ]
    question_text = models.CharField(max_length=30)
    description = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to=MEDIA_URL.join('polls/'))
    choice_type = models.CharField(max_length=2, choices=CHOICES_TYPE, default='r')
    publish_date = models.DateTimeField('date published')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.publish_date <= now

    was_published_recently.admin_order_field = 'publish_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=50)
    votes = models.ManyToManyField(User, related_name="votes", default=None, blank=True)

    def __str__(self):
        return self.choice_text

class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=155, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    publish_date = models.DateTimeField('date published')