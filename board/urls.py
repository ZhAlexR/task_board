from django.urls import path

from board.views import (
    IndexListView,
    TaskDetailView,
    TaskUpdateView,
    TaskDeleteView
)

app_name = "board"

urlpatterns = [
    path("", IndexListView.as_view(), name="index"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/update", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete", TaskDeleteView.as_view(), name="task-delete"),
]
