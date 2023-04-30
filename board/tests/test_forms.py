from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from board.forms import ProjectForm, TaskForm
from board.models import Project, TaskType, Position


class ProjectFormTestCase(TestCase):
    def test_invalid_deadline(self):
        past_date = timezone.now() - timezone.timedelta(days=2)
        form_data = {
            "name": "Test Project",
            "description": "Test Description",
            "status": 1,
            "deadline": past_date,
        }
        form = ProjectForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("deadline", form.errors)

    def test_valid_deadline(self):
        future_date = timezone.now() + timezone.timedelta(days=1)
        form_data = {
            "name": "Test Project",
            "description": "Test Description",
            "status": 1,
            "deadline": future_date,
        }
        form = ProjectForm(data=form_data)
        self.assertTrue(form.is_valid())


class TaskFormTestCase(TestCase):
    def setUp(self) -> None:
        self.project = Project.objects.create(
            name="Test Project",
            description="Test Description",
            deadline=timezone.now() + timezone.timedelta(days=7),
        )
        self.task_type = TaskType.objects.create(name="Test Task Type")
        self.worker = get_user_model().objects.create_user(
            username="User",
            password="password",
            position=Position.objects.create(name="Develorer"),
        )

    def test_invalid_deadline_in_past(self):
        past_date = timezone.now() - timezone.timedelta(days=1)
        form_data = {
            "name": "Test Task",
            "description": "Test Description",
            "deadline": past_date,
            "status": "urgent",
            "project": self.project.id,
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("deadline", form.errors)

    def test_valid_deadline(self):
        future_date = timezone.now() + timezone.timedelta(days=1)
        form_data = {
            "name": "Test Task",
            "description": "Test Description",
            "deadline": future_date,
            "priority": "urgent",
            "task_type": self.task_type,
            "assignees": [self.worker.pk],
            "project": self.project.id,
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_deadline_farther_then_project_deadline(self):
        far_future_date = timezone.now() + timezone.timedelta(days=14)
        form_data = {
            "name": "Test Task",
            "description": "Test Description",
            "deadline": far_future_date,
            "priority": "urgent",
            "task_type": self.task_type,
            "assignees": [self.worker.pk],
            "project": self.project.id,
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("deadline", form.errors)
