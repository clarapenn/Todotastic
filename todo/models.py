import datetime

from django.db import models


class Todo(models.Model):
    task = models.CharField(
        max_length=1000,
        help_text="e.g wash car",
    )
    completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Todo {self.id}: {self.task}"

    def mark_complete(self):
        self.completed = True
        self.date_completed = datetime.date.today()
        self.save()

    def mark_incomplete(self):
        self.completed = False
        self.date_completed = None
        self.save()
