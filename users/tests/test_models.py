from django.test import TestCase

from users.models import User


class UserTestCases(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='user',
            email='user@email.com',
            password='123'
        )
        self.superuser = User.objects.create_superuser(
            username='superuser',
            email='superuser@email.com',
            password='456'
        )

    def test_users_count(self):
        pass

    def test_username(self):
        pass

    def test_email(self):
        pass

    def test_password(self):
        pass

    def test_is_active(self):
        pass

    def test_user_rights(self):
        pass

    def tearDown(self):
        pass
