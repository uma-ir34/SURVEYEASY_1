# Generated by Django 5.2.4 on 2025-07-11 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("questionnaire", "0007_question_survey_alter_question_question_type"),
    ]

    operations = [
        migrations.RenameField(
            model_name="participant",
            old_name="group_label",
            new_name="contact_info",
        ),
        migrations.RemoveField(
            model_name="participant",
            name="c_section",
        ),
        migrations.RemoveField(
            model_name="participant",
            name="date",
        ),
        migrations.RemoveField(
            model_name="participant",
            name="menopausal_status",
        ),
        migrations.RemoveField(
            model_name="participant",
            name="parity",
        ),
        migrations.RemoveField(
            model_name="participant",
            name="vaginal_delivery",
        ),
        migrations.AddField(
            model_name="participant",
            name="gender",
            field=models.CharField(
                choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
                default="Other",
                max_length=10,
            ),
        ),
    ]
