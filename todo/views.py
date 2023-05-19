from django.shortcuts import redirect, render, get_object_or_404
from todo.models import Todo
from todo.forms import TodoForm


def list_todos(request):

    template_name = "todo/list_todos.html"
    context = {"todos": Todo.objects.all()}

    return render(request, template_name, context)


def todo_detail(request, todo_id):

    todo = get_object_or_404(Todo, id=todo_id)
    template_name = "todo/todo_detail.html"
    context = {"todo": todo}

    return render(request, template_name, context)


def todo_edit(request, todo_id):

    todo = get_object_or_404(Todo, id=todo_id)

    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            # because this is a ModelForm, it has a save method,
            # which updates the fields of the todo instance we passed in
            # when we made the form a few lines earlier

            # After editing, send the user to a page where they can see the result
            return redirect("todo-detail", todo_id)
        else:
            # TO COME: show a message to the user
            pass
    else:  # ie, request.GET - just loading a page
        form = TodoForm(instance=todo)

    template_name = "todo/todo_edit.html"
    context = {"form": form, "todo": todo}

    return render(request, template_name, context)
