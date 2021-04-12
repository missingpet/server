"""Test cases for models."""
from django import test

from ..models import User
from .test_data import (
    test_user_email,
    test_user_nickname,
    test_user_password,
    test_superuser_email,
    test_superuser_nickname,
    test_superuser_password,
)


class UserTestCase(test.TestCase):
    def setUp(self):
        test_user_data = {
            "email": test_user_email,
            "nickname": test_user_nickname,
            "password": test_user_password,
        }
        self.user = User.objects.create_user(**test_user_data)

        test_superuser_data = {
            "email": test_superuser_email,
            "nickname": test_superuser_nickname,
            "password": test_superuser_password,
        }
        self.superuser = User.objects.create_superuser(**test_superuser_data)

    @test.tag("users-count")
    def test_users_count(self):
        self.assertEqual(User.objects.count(), 2)

    @test.tag("nickname")
    def test_nickname(self):
        self.assertEqual(self.user.nickname, test_user_nickname)
        self.assertEqual(self.superuser.nickname, test_superuser_nickname)

    @test.tag("email")
    def test_email(self):
        self.assertEqual(self.user.email, test_user_email)
        self.assertEqual(self.superuser.email, test_superuser_email)

    @test.tag("password")
    def test_password(self):
        self.assertTrue(self.user.check_password(test_user_password))
        self.assertTrue(self.superuser.check_password(test_superuser_password))

    @test.tag("is-active")
    def test_is_active(self):
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.superuser.is_active)

    @test.tag("user-rights")
    def test_user_rights(self):
        self.assertTrue(self.superuser.is_superuser)
        self.assertFalse(self.user.is_superuser)
        self.assertTrue(self.superuser.is_staff)
        self.assertFalse(self.user.is_staff)

    def tearDown(self):
        pass
