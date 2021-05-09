"""
Module which contains test cases for custom Django models.
"""
from django.test import TestCase

from ..models import User
from .test_data import *  # NOQA


class UserTestCase(TestCase):
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

    def test_users_count(self):
        self.assertEqual(User.objects.count(), 2)

    def test_nickname_set_on_model_create(self):
        self.assertEqual(self.user.nickname, test_user_nickname)
        self.assertEqual(self.superuser.nickname, test_superuser_nickname)

    def test_email_set_on_model_create(self):
        self.assertEqual(self.user.email, test_user_email)
        self.assertEqual(self.superuser.email, test_superuser_email)

    def test_password_set_on_model_create(self):
        self.assertTrue(self.user.check_password(test_user_password))
        self.assertTrue(self.superuser.check_password(test_superuser_password))

    def test_is_active_set_on_model_create(self):
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.superuser.is_active)

    def test_user_rights_are_correct_on_model_create(self):
        self.assertTrue(self.superuser.is_superuser)
        self.assertFalse(self.user.is_superuser)
        self.assertTrue(self.superuser.is_staff)
        self.assertFalse(self.user.is_staff)

    def tearDown(self):
        pass
