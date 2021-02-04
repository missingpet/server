from django.test import tag
from django.test import TestCase

from .. import models

from . import test_data


class ModelsTestCases(TestCase):
    def setUp(self):
        self.user = models.User.objects.create_user(
            test_data.TEST_USER_EMAIL,
            test_data.TEST_USER_NICKNAME,
            test_data.TEST_USER_PASSWORD,
        )
        self.superuser = models.User.objects.create_superuser(
            test_data.TEST_SUPERUSER_EMAIL,
            test_data.TEST_SUPERUSER_NICKNAME,
            test_data.TEST_SUPERUSER_PASSWORD,
        )

    @tag('users-count')
    def test_users_count(self):
        self.assertEqual(models.User.objects.count(), 2)

    @tag('nickname')
    def test_nickname(self):
        self.assertEqual(self.user.nickname, test_data.TEST_USER_NICKNAME)
        self.assertEqual(self.superuser.nickname, test_data.TEST_SUPERUSER_NICKNAME)

    @tag('email')
    def test_email(self):
        self.assertEqual(self.user.email, test_data.TEST_USER_EMAIL)
        self.assertEqual(self.superuser.email, test_data.TEST_SUPERUSER_EMAIL)

    @tag('password')
    def test_password(self):
        self.assertTrue(self.user.check_password(test_data.TEST_USER_PASSWORD))
        self.assertTrue(self.superuser.check_password(test_data.TEST_SUPERUSER_PASSWORD))

    @tag('is-active')
    def test_is_active(self):
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.superuser.is_active)

    @tag('user-rights')
    def test_user_rights(self):
        self.assertTrue(self.superuser.is_superuser)
        self.assertFalse(self.user.is_superuser)
        self.assertTrue(self.superuser.is_staff)
        self.assertFalse(self.user.is_staff)

    def tearDown(self):
        pass
