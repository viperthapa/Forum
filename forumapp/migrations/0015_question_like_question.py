# Generated by Django 2.2.1 on 2020-04-26 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forumapp', '0014_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='like_question',
            field=models.IntegerField(default=0),
        ),
    ]