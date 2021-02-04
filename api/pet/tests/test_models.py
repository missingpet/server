from django.test import tag
from django.test import TestCase
from ..models import User


class UserModelTestCases(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user',
                                             'user@email.com',
                                             'User123*')
        self.superuser = User.objects.create_superuser('superuser',
                                                       'superuser@email.com',
                                                       'Superuser456*')

    @tag('users-count')
    def test_users_count(self):
        pass

    @tag('nickname')
    def test_nickname(self):
        pass

    @tag('email')
    def test_email(self):
        pass

    @tag('password')
    def test_password(self):
        pass

    @tag('is-active')
    def test_is_active(self):
        pass

    @tag('user-rights')
    def test_user_rights(self):
        pass

    def tearDown(self):
        pass

