from django.test import tag
from django.urls import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_201_CREATED
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from ..models import User


class ApiTestCases(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_1 = User.objects.create_user("test@email.com", "test", "password")

    @tag("sign-up")
    def test_sign_up(self):
        """Тестирует регистрацию нового пользователя."""
        data = {
            "username": "username",
            "email": "some@email.com",
            "password": "password",
        }
        response = self.client.post(reverse("sign-up"), data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    @tag("sign-in")
    def test_sign_in(self):
        """Тестирует вход в профиль."""
        data = {"email": "test@email.com", "password": "password"}
        response = self.client.post(reverse("sign-in"), data)
        self.assertEqual(response.status_code, HTTP_200_OK)

    @tag("sign-out")
    def test_sign_out(self):
        """Тестирует выход из профиля."""
        data = {"email": "test@email.com", "password": "password"}
        response = self.client.post(reverse("sign-in"), data)
        data = {"refresh": response.data["tokens"]["refresh"]}
        response = self.client.post(reverse("sign-out"), data)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

    def tearDown(self):
        pass
