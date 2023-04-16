from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from board.urls import urlpatterns


class TestUserAccess(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="TestUser",
            password="SuperSecretPassword"
        )
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
