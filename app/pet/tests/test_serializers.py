"""Test cases for serializers."""
from django import test

from .. import serializers
from .data_factories import UserFactory


class SerializerTestCase(test.TestCase):
    def setUp(self):
        pass

    def test_user_create_serializer(self):
        valid_data = {
            "email": "test@email.com",
            "nickname": "nickname",
            "password": "Password123*",
        }

        serializer = serializers.UserCreateSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        invalid_email_data = {
            "email": "its not an email address",
            "nickname": "nickname",
            "password": "Password123*",
        }

        serializer = serializers.UserCreateSerializer(data=invalid_email_data)
        self.assertFalse(serializer.is_valid())

        invalid_nickname_data = {
            "email": "test@email.com",
            "nickname": "()*%$",
            "password": "Password123*",
        }

        serializer = serializers.UserCreateSerializer(
            data=invalid_nickname_data)
        self.assertFalse(serializer.is_valid())

        invalid_password_data = {
            "email": "test@email.com",
            "nickname": "nickname",
            "password": "abc",
        }

        serializer = serializers.UserCreateSerializer(
            data=invalid_password_data)
        self.assertFalse(serializer.is_valid())

    def test_password_reset_request_serializer(self):
        user = UserFactory(email="email@mail.ru")

        data = {
            "email": user.email,
        }
        serializer = serializers.PasswordResetRequestSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def tearDown(self):
        pass
