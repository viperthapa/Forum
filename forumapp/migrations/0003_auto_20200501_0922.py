# Generated by Django 2.2.1 on 2020-05-01 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forumapp', '0002_auto_20200501_0630'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='views',
        ),
        migrations.AddField(
            model_name='question',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]