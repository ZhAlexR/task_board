from django.urls import path

from board.views import (
    IndexListView,
    ProjectCreateView,
    TaskDetailView,
    TaskUpdateView,
    TaskDeleteView,
    ProjectDeleteView,
    ProjectUpdateView,
    toggle_assign_to_task,
    UserTaskListView,
    ProjectDetailView, UserProjectListView, TaskCreateView, WorkerCreateView, toggle_task_change_is_completed,
)

app_name = "board"

urlpatterns = [
    path("", IndexListView.as_view(), name="index"),
    path(
        "projects/create", ProjectCreateView.as_view(), name="project-create"
    ),
    path(
        "projects/user/<int:pk>/list/",
        UserProjectListView.as_view(),
        name="user-project-list",
    ),
    path(
        "projects/<int:pk>/update",
        ProjectUpdateView.as_view(),
        name="project-update",
    ),
    path(
        "projects/<int:pk>/delete",
        ProjectDeleteView.as_view(),
        name="project-delete",
    ),
    path(
        "projects/<int:pk>/detail",
        ProjectDetailView.as_view(),
        name="project-detail",
    ),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path(
        "tasks/<int:pk>/update", TaskUpdateView.as_view(), name="task-update"
    ),
    path(
        "tasks/<int:pk>/delete", TaskDeleteView.as_view(), name="task-delete"
    ),
    path(
        "tasks/user/<int:pk>/list/",
        UserTaskListView.as_view(),
        name="user-task-list",
    ),
    path(
        "tasks/<int:pk>/toogle_assign/",
        toggle_assign_to_task,
        name="task-toggle-assign",
    ),
    path(
            "tasks/<int:pk>/toogle_change_is_completed/",
            toggle_task_change_is_completed,
            name="task-change-is-completed",
        ),
    path(
        "worker/create/",
        WorkerCreateView.as_view(),
        name="worker-create"
        ),
]
