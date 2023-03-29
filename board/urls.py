from django.urls import path

from board.views import IndexListView, TaskDetailView

app_name = "board"

urlpatterns = [
    path("", IndexListView.as_view(), name="index"),
    path("tasks/<int:pk>/detail", TaskDetailView.as_view(), name="task-detail")
]
