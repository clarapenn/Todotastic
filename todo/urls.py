from django.urls import path
from todo.views import (
    list_todos,
    todo_detail,
    todo_delete,
    todo_add_edit,
    toggle_completion,
)

urlpatterns = [
    path("", list_todos, name="todo-list"),
    path("todo/add/", todo_add_edit, name="todo-add"),
    path("todo/<int:todo_id>/detail/", todo_detail, name="todo-detail"),
    path("todo/<int:todo_id>/edit/", todo_add_edit, name="todo-edit"),
    path(
        "todo/<int:todo_id>/complete/toggle/",
        toggle_completion,
        name="todo-complete-toggle",
    ),
    path("todo/<int:todo_id>/delete/", todo_delete, name="todo-delete"),
]
