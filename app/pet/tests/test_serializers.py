"""
Test cases for serializers.
"""
from django import test

from .. import serializers


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

    def test_change_nickname_serializer(self):
        invalid_data = {
            "nickname": "new_nickname",
        }
        serializer = serializers.UserNicknameChangeSerializer(
            data=invalid_data)
        self.assertFalse(serializer.is_valid())

        valid_data = {
            "nickname": "NewNickname",
        }
        serializer = serializers.UserNicknameChangeSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def tearDown(self):
        pass
