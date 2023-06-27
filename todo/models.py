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
    date_due = models.DateTimeField(null=True, blank=True)

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

    def is_overdue(self):
        today = datetime.date.today()
        # This is currently ONLY comparing dates. TODO: make it compare timezone-aware datetimes
        if self.date_due and self.date_due.date() < today:
            return True

        return False

    def refresh_priorities(self):
        """If this Todo is marked as critical, make sure it's the only critical one.
        Return the Downgraded todo after the work is done."""

        downgraded_todo = None

        if self.priority == self.TODO_CRITICAL:
            other_critical_todos = Todo.objects.exclude(id=self.id).filter(
                priority=self.TODO_CRITICAL
            )
            # other_critical_todos will be a queryset with 0 or 1 things in it,
            # and so we can safely get that with the .first() method, which
            # returns the todo or None
            downgraded_todo = other_critical_todos.first()
            # We need to get this ^^ before we change it in the database, because
            # then it won't be in the queryset results after the update()

            # Two ways to update multiple records/rows:
            # 1. Queryset.update() does it in one hit
            other_critical_todos.update(priority=self.TODO_URGENT)
            # 2. Or we can loop through and deal with each one manually:
            # downgraded_todo_count = len(other_critical_todos)
            # for other_todo in other_critical_todos:
            #     other_todo.priority = TODO_URGENT
            #     other_todo.save()
        return downgraded_todo
