from django import forms
from todo.models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        exclude = ("id",)  # ie, we don't want to be able to edit the id of the Todo
