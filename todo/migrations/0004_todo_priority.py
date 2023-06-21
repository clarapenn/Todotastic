# Generated by Django 4.2.1 on 2023-06-21 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("todo", "0003_todo_owner"),
    ]

    operations = [
        migrations.AddField(
            model_name="todo",
            name="priority",
            field=models.IntegerField(
                choices=[
                    (1, "Critical"),
                    (2, "Urgent"),
                    (3, "Important"),
                    (4, "Medium"),
                    (5, "Neutral"),
                ],
                default=5,
            ),
        ),
    ]
