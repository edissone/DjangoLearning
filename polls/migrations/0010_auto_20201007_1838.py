# Generated by Django 3.1 on 2020-10-07 18:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0009_auto_20201007_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='votes',
            field=models.ManyToManyField(blank=True, default=None, related_name='votes', to=settings.AUTH_USER_MODEL),
        ),
    ]
