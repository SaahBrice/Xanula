# Generated by Django 5.1 on 2024-08-21 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_quizattempt_questionresponse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizattempt',
            name='date_attempted',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
