import datetime

from django.contrib.auth.models import User

from django.db import models


class Todo(models.Model):
    TODO_CRITICAL = 1
    TODO_URGENT = 2
    TODO_IMPORTANT = 3
    TODO_MEDIUM = 4
    TODO_NEUTRAL = 5

    PRIORITY_CHOICES = [
        (TODO_CRITICAL, "Critical"),
        (TODO_URGENT, "Urgent"),
        (TODO_IMPORTANT, "Important"),
        (TODO_MEDIUM, "Medium"),
        (TODO_NEUTRAL, "Neutral"),
    ]
    task = models.CharField(
        max_length=1000,
        help_text="e.g wash car",
    )
    completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES,
        default=TODO_NEUTRAL,
    )

    def __str__(self):
        return f"Todo #{self.id} for {self.owner}: {self.task}"

    def mark_complete(self):
        self.completed = True
        self.date_completed = datetime.date.today()
        self.save()

    def mark_incomplete(self):
        self.completed = False
        self.date_completed = None
        self.save()
