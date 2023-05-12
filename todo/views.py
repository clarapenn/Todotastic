from django.shortcuts import render
from todo.models import Todo


def list_todos(request):

    template_name = "todo/list_todos.html"
    context = {"todos": Todo.objects.all()}

    return render(request, template_name, context)
