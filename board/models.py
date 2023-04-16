from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=63, unique=True, default="Developer")

    def __str__(self) -> str:
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self) -> str:
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        related_name="workers",
    )

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}" f"({self.position.name})"


class Task(models.Model):
    TASK_PRIORITY = [
        ("urgent", "Urgent"),
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]

    MEDIUM_PRIORITY = TASK_PRIORITY[2][0]

    name = models.CharField(max_length=63)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=15, choices=TASK_PRIORITY, default=MEDIUM_PRIORITY
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
    )
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL)

    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="tasks"
    )

    class Meta:
        default_related_name = "tasks"

    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    PROJECT_STATUS = [
        (1, "In development"),
        (2, "In support"),
        (3, "Deployed"),
        (4, "Closed"),
    ]

    name = models.CharField(max_length=63)
    description = models.TextField()
    deadline = models.DateTimeField()
    status = models.IntegerField(choices=PROJECT_STATUS, default=1)

    def __str__(self) -> str:
        return self.name
