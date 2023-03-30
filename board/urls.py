from django.urls import path

from board.views import (
    IndexListView,
    ProjectDetailView,
    TaskDetailView,
    TaskUpdateView,
    TaskDeleteView,
)

app_name = "board"

urlpatterns = [
    path("", IndexListView.as_view(), name="index"),
    path("projects/<int:pk>/", IndexListView.as_view(), name="user-projects"),
    path("project/<int:pk>/detail", ProjectDetailView.as_view(), name="project-detail"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/update", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete", TaskDeleteView.as_view(), name="task-delete"),
]
