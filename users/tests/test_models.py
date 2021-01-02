from django.test import TestCase
from django.test import tag

from users.models import User


class UserTestCases(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user", email="user@email.com", password="123"
        )
        self.superuser = User.objects.create_superuser(
            username="superuser", email="superuser@email.com", password="456"
        )

    @tag("users-count")
    def test_users_count(self):
        pass

    @tag("username")
    def test_username(self):
        pass

    @tag("email")
    def test_email(self):
        pass

    @tag("password")
    def test_password(self):
        pass

    @tag("is-active")
    def test_is_active(self):
        pass

    @tag("user-rights")
    def test_user_rights(self):
        pass

    def tearDown(self):
        pass
