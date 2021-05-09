"""
Test cases for views.
"""
from django.urls import reverse
from rest_framework import status
from rest_framework import test

from ..models import User


class ViewTestCase(test.APITestCase):
    def setUp(self):
        data = {
            "nickname": "nickname",
            "email": "email@email.com",
            "password": "Password123^",
        }
        self.user = User.objects.create_user(**data)
        self.client = test.APIClient()

    def test_password_reset_request_view(self):
        query_dict = {
            "email": "email@email.com",
        }
        response = self.client.post(
            reverse("password-reset-request", args=("v1",)), query_dict
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def tearDown(self):
        pass
