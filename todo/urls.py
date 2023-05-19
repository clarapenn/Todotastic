from django.urls import path
from todo.views import list_todos, todo_detail, todo_edit

urlpatterns = [
    path("", list_todos, name="todo-list"),
    path("todo/<int:todo_id>/", todo_detail, name="todo-detail"),
    path("todo/<int:todo_id>/edit/", todo_edit, name="todo-edit"),
]
