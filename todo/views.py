from django.shortcuts import redirect, render, get_object_or_404
from todo.models import Todo
from todo.forms import TodoForm, CompletionForm, AddForm, DeletionForm
from django.views.decorators.http import require_POST
from django.contrib import messages


def list_todos(request):

    template_name = "todo/list_todos.html"

    todos = Todo.objects.all().order_by("-date_created")

    all_todos_count = todos.count()  # effectively same as Todo.objects.all().count()

    completed_todos_count = Todo.objects.filter(completed=True).count()
    incomplete_todos_count = Todo.objects.filter(completed=False).count()
    # Or could do it with exclude, which is like the opposite of filter()
    # incomplete_todos_count = Todo.objects.exclude(completed=True).count()

    try:
        percentage_complete = completed_todos_count / all_todos_count * 100
    except ZeroDivisionError:
        percentage_complete = 0

    context = {
        "todos": todos,
        "completed_todos_count": completed_todos_count,
        "incomplete_todos_count": incomplete_todos_count,
        "percentage_complete": int(percentage_complete),
    }

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


@require_POST
def todo_delete(request, todo_id):

    todo = get_object_or_404(Todo, id=todo_id)

    form = DeletionForm(request.POST, instance=todo)

    if form.is_valid():

        # form.data is the data from request.POST, before cleaning
        # cleaned_data is the checked version of what we got in request.POST
        submitted_data = form.data
        submitted_todo_id = submitted_data["id"]

        # raw data is always a string, but todo_id is an int, and we need to
        # compare like with like
        if submitted_todo_id != str(todo_id):
            # someone has been tampering with the page because the todos don't match
            messages.warning(
                request,
                "Tampering detected",
                extra_tags="alert alert-warning",
            )
        else:
            # All ok so let's mark the todo as deleted
            todo.delete()

            messages.success(
                request,
                f"{todo.task}: deleted",
                extra_tags="alert alert-success",
            )
    return redirect("todo-list")
