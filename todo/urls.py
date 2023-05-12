from django.urls import path
from todo.views import list_todos

urlpatterns = [
    path("", list_todos, name="todo-list"),
]
