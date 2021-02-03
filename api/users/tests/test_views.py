from django.test import tag
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from ..models import User


class ApiTestCases(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_1 = User.objects.create_user("test@email.com", "test",
                                               "password")

    @tag("sign-up")
    def test_sign_up(self):
        data = {
            "username": "username",
            "email": "some@email.com",
            "password": "password",
        }
        response = self.client.post(reverse("sign-up"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @tag('sign-in')
    def test_sign_in(self):
        data = {'email': 'test@email.com', 'password': 'password'}
        response = self.client.post(reverse('sign-in'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        pass
