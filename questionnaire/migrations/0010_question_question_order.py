# Generated by Django 5.2.4 on 2025-07-11 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("questionnaire", "0009_alter_question_survey"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="question_order",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
