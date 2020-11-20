from django.urls import reverse

from django.test import tag

from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_201_CREATED
from rest_framework.status import HTTP_204_NO_CONTENT

from ..models import User


class ApiTestCases(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_1 = User.objects.create_user(
            'test@email.com',
            'test',
            'password'
        )

    @tag('sign-up')
    def test_sign_up(self):
        """Тестирует регистрацию нового пользователя."""
        data = {
            'username': 'username',
            'email': 'some@email.com',
            'password': 'password'
        }
        response = self.client.post(reverse('sign-up'), data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    @tag('sign-in')
    def test_sign_in(self):
        """Тестирует вход в профиль."""
        data = {
            'email': 'test@email.com',
            'password': 'password'
        }
        response = self.client.post(reverse('sign-in'), data)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def tearDown(self):
        pass


class WithAuthApiTestCases(APITestCase):

    def setUp(self):
        self.client = APIClient()
        # Создаём тестового пользователя.
        self.auth_user = User.objects.create_user(
            'auth@email.com',
            'auth',
            'auth_password'
        )
        # Тело запроса.
        data = {
            'email': 'auth@email.com',
            'password': 'auth_password'
        }
        # Входим в аккаунт.
        response = self.client.post(reverse('sign-in'), data)
        # Получаем учётные данные.
        self.access = response.data['tokens']['access']
        self.refresh = response.data['tokens']['refresh']
        # Добавляем access-токен в заголовок запроса.
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.access))

    @tag('sign-out')
    def test_sign_out(self):
        """Тестирует выход из профиля."""
        data = {
            'refresh': self.refresh
        }
        response = self.client.post(reverse('sign-out'), data)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

    def tearDown(self):
        pass
