import random
from datetime import date, timedelta

from django.utils import timezone

from board.forms import SearchForm, FilterForm
from board.urls import urlpatterns

from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from board.models import Project, Task, Worker, TaskType, Position


def create_user(
    position: Position = None,
    username: str = "copy_ninja",
    password: str = "SuperSecretPassword",
    first_name: str = "Kakashi",
    last_name: str = "Hatake",
) -> get_user_model():
    return get_user_model().objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        position=Position.objects.create(name="Develorer")
        if not position
        else position,
    )


def create_projects_and_tasks(quantity: int) -> None:
    for i in range(quantity):
        project = Project.objects.create(
            name=f"Test project {i}",
            description=f"Description {i}",
            deadline=date.today() + timedelta(days=i),
            status=random.choice([1, 2, 3, 4]),
        )
        task_type = TaskType.objects.create(name=f"TaskType{i}")
        Task.objects.create(
            name=f"Task{i}",
            task_type=task_type,
            project=project,
            deadline=date.today() + timedelta(days=i),
        )


class TestUserAccess(TestCase):
    def setUp(self) -> None:
        self.user = create_user()
        self.url_names = [url for url in urlpatterns if hasattr(url, "name")]

    def test_login_required_for_anonymous_user(self):
        for url in self.url_names:
            if url.name in ["index", "worker-create"]:
                continue
            if "<int:pk>" in str(url):
                valid_url = reverse(f"board:{url.name}", kwargs={"pk": 1})
            else:
                valid_url = reverse(f"board:{url.name}")

            with self.subTest(url=url):
                res = self.client.get(valid_url)
                self.assertNotEqual(res.status_code, 200)


class TestPagination(TestCase):
    def setUp(self) -> None:
        create_projects_and_tasks(12)
        self.user = create_user()
        self.client.force_login(self.user)

    def test_pagination_is_ten(self):
        response = self.client.get(reverse("board:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertTrue(len(response.context["project_list"]) == 10)

    def test_second_page_objects_quantity(self):
        response = self.client.get(reverse("board:index") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context["project_list"]) == 2)


class TestCorrectTemplate(TestCase):
    def setUp(self) -> None:
        self.user = create_user()
        self.client.force_login(self.user)
        create_projects_and_tasks(12)

    def test_views_use_correct_templates_for_project(self):
        index_page = self.client.get(reverse("board:index"))
        index_page_user_projects = self.client.get(
            reverse("board:user-project-list", kwargs={"pk": self.user.pk})
        )
        project_detail = self.client.get(
            reverse("board:project-detail", kwargs={"pk": 1})
        )
        project_form_create = self.client.get(reverse("board:project-create"))
        project_form_update = self.client.get(
            reverse("board:project-update", kwargs={"pk": 1})
        )

        self.assertTemplateUsed(index_page, "board/index.html")
        self.assertTemplateUsed(index_page_user_projects, "board/index.html")
        self.assertTemplateUsed(project_detail, "board/project_detail.html")
        self.assertTemplateUsed(project_form_create, "board/project_form.html")
        self.assertTemplateUsed(project_form_update, "board/project_form.html")

    def test_views_use_correct_templates_for_task(self):
        index_page_user_tasks = self.client.get(
            reverse("board:user-task-list", kwargs={"pk": self.user.pk})
        )
        task_detail = self.client.get(
            reverse("board:task-detail", kwargs={"pk": 1})
        )
        task_form_create = self.client.get(reverse("board:task-create"))
        task_form_update = self.client.get(
            reverse("board:task-update", kwargs={"pk": 1})
        )

        self.assertTemplateUsed(index_page_user_tasks, "board/task_list.html")
        self.assertTemplateUsed(task_detail, "board/task_detail.html")
        self.assertTemplateUsed(task_form_create, "board/task_form.html")
        self.assertTemplateUsed(task_form_update, "board/task_form.html")

    def test_views_use_correct_templates_for_authentication(self):
        login = self.client.get(reverse("login"))
        logout = self.client.get(reverse("logout"))
        self.assertTemplateUsed(login, "registration/login.html")
        self.assertTemplateUsed(logout, "registration/logged_out.html")


class TestSearchMixins(TestCase):
    def setUp(self) -> None:
        self.user = create_user()
        self.client.force_login(self.user)
        create_projects_and_tasks(10)

    def test_search_form_in_context(self):
        response = self.client.get(reverse_lazy("board:index"))
        self.assertIsInstance(response.context["search_form"], SearchForm)

    def test_get_projects_queryset(self):
        all_projects = Project.objects.all()
        project0 = Project.objects.get(pk=1)
        response = self.client.get(
            reverse_lazy("board:index"), {"search_criteria": "Test project 0"}
        )
        self.assertContains(response, project0)
        self.assertNotEqual(
            all_projects, response.context_data.get("project_list")
        )

    def test_get_tasks_queryset(self):
        project0 = Project.objects.get(pk=1)
        task = Task.objects.create(
            name="New_task",
            task_type_id=1,
            project=project0,
            deadline=date.today(),
        )
        response = self.client.get(
            reverse("board:project-detail", kwargs={"pk": project0.pk}),
            {"search_criteria": "New_task"},
        )
        self.assertEqual(
            task, response.context_data.get("task_list").get(pk=task.pk)
        )
        self.assertNotEqual(
            project0.tasks.all(), response.context_data.get("task_list")
        )


class TestFilterFormMixins(TestCase):
    def setUp(self) -> None:
        self.user = create_user()
        self.client.force_login(self.user)
        create_projects_and_tasks(10)

    def test_filter_form_in_context(self):
        response = self.client.get(reverse_lazy("board:index"))
        self.assertIsInstance(response.context["filter_form"], FilterForm)

    def test_projects_query_set(self):
        in_dev_projects = Project.objects.filter(status=1).order_by("deadline")
        in_dev_support_projects = Project.objects.filter(
            status__in=[1, 2]
        ).order_by("-deadline")
        response_in_dev = self.client.get(
            reverse("board:index"), {"status": [1], "deadline": "deadline"}
        )
        response_in_dev_support = self.client.get(
            reverse("board:index"), {"status": [1, 2], "deadline": "-deadline"}
        )
        self.assertEqual(
            list(response_in_dev.context_data.get("project_list")),
            list(in_dev_projects),
        )
        self.assertEqual(
            list(response_in_dev_support.context_data.get("project_list")),
            list(in_dev_support_projects),
        )


class TestToggleAssignToTask(TestCase):
    def setUp(self):
        self.user = create_user()
        self.client.force_login(user=self.user)
        create_projects_and_tasks(5)

    def test_toggle_assign_to_task(self):
        task = Task.objects.get(pk=1)

        self.client.post(
            reverse_lazy("board:task-toggle-assign", kwargs={"pk": task.pk})
        )
        task.refresh_from_db()
        self.assertIn(self.user, task.assignees.all())

        self.client.post(
            reverse_lazy("board:task-toggle-assign", kwargs={"pk": task.pk})
        )
        task.refresh_from_db()
        self.assertNotIn(self.user, task.assignees.all())


class TestToggleTaskChangeIsCompleted(TestCase):
    def setUp(self):
        self.user = create_user()
        self.client.force_login(user=self.user)
        create_projects_and_tasks(5)

    def test_toggle_task_change_is_completed(self):
        task = Task.objects.get(pk=2)

        self.client.post(
            reverse_lazy(
                "board:task-change-is-completed", kwargs={"pk": task.pk}
            )
        )
        task.refresh_from_db()
        self.assertTrue(task.is_completed)

        self.client.post(
            reverse_lazy(
                "board:task-change-is-completed", kwargs={"pk": task.pk}
            )
        )
        task.refresh_from_db()
        self.assertFalse(task.is_completed)
