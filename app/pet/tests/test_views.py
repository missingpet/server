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

    def tearDown(self):
        pass
