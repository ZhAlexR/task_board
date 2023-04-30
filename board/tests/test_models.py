from django.test import TestCase
from django.utils import timezone

from board.models import Position, TaskType, Worker, Task, Project


class TestModels(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Manager")
        self.worker = Worker.objects.create_user(
            username="john.doe",
            password="123",
            first_name="John",
            last_name="Doe",
            position=self.position,
        )
        self.task_type = TaskType.objects.create(name="Bug")
        self.project = Project.objects.create(
            name="My Project",
            description="A project description",
            deadline=timezone.now() + timezone.timedelta(days=7),
            status=Project.PROJECT_STATUS[0][0],
        )
        self.task = Task.objects.create(
            name="My Task",
            description="A task description",
            deadline=timezone.now() + timezone.timedelta(days=3),
            priority=Task.TASK_PRIORITY[2][0],
            task_type=self.task_type,
            project=self.project,
        )
        self.task.assignees.add(self.worker)

    def test_position_str(self):
        self.assertEqual(str(self.position), "Manager")

    def test_task_type_str(self):
        self.assertEqual(str(self.task_type), "Bug")

    def test_worker_str(self):
        self.assertEqual(str(self.worker), "John Doe(Manager)")

    def test_task_str(self):
        self.assertEqual(str(self.task), "My Task")

    def test_project_str(self):
        self.assertEqual(str(self.project), "My Project")

    def test_task_assignees(self):
        self.assertEqual(self.task.assignees.count(), 1)
        self.assertIn(self.worker, self.task.assignees.all())
