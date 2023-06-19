from django.shortcuts import redirect, render, get_object_or_404
from todo.models import Todo
from todo.forms import TodoForm, CompletionForm, AddForm
from django.views.decorators.http import require_POST
from django.contrib import messages


def list_todos(request):

    template_name = "todo/list_todos.html"

    todos = Todo.objects.all().order_by("-date_created")
    context = {"todos": todos}

    return render(request, template_name, context)


def todo_detail(request, todo_id):

    todo = get_object_or_404(Todo, id=todo_id)
    template_name = "todo/todo_detail.html"
    context = {"todo": todo}

    return render(request, template_name, context)


def todo_add_edit(request, todo_id=None):
    # This view handles both serving the edit form ready for
    # use (responding to a GET) and also processing the data
    # submitted from a form (responding to a POST)

    template_name = "todo/todo_add_edit.html"

    if todo_id:
        todo = get_object_or_404(Todo, id=todo_id)
        form_class = TodoForm
        redirect_args = ("todo-detail", todo_id)
        success_message = "Todo updated!"
    else:
        todo = None
        form_class = AddForm
        redirect_args = ("todo-list",)
        success_message = "It's on the list!"

    # If the user has submitted the form, that will be
    # with a POST request. Let's process that submitted data
    if request.method == "POST":
        form = form_class(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            # because this is a ModelForm, it has a save method,
            # which updates the fields of the todo instance we passed in
            # when we made the form a few lines earlier

            messages.success(request, success_message, extra_tags="alert alert-success")
            # After editing, send the user to a page where they can see the result
            return redirect(*redirect_args)
        else:
            # TO COME: show a message to the user
            pass
    else:
        # ie, request.GET - just loading a page, but the page
        # still needs a form to render, so that the user can
        # edit the todo -- and so we also need to pass in the
        # todo as "instance" so that the form is pre-filled with
        # the details of the specific todo being edited

        form = form_class(instance=todo)

    context = {"form": form, "todo": todo}

    return render(request, template_name, context)


@require_POST
def toggle_completion(request, todo_id):

    todo = get_object_or_404(Todo, id=todo_id)

    form = CompletionForm(request.POST, instance=todo)

    if form.is_valid():
        # All ok so let's mark the todo as completed

        if todo.completed:
            todo.mark_incomplete()

            messages.info(
                request,
                f"{todo.task}: back on the list!",
                extra_tags="alert alert-info",
            )
        else:
            todo.mark_complete()

            messages.success(
                request,
                f"{todo.task}: done!!",
                extra_tags="alert alert-success",
            )

    return redirect("todo-list")
    return redirect("todo-list")
