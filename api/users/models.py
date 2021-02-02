from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Адрес электронной почты',
                              unique=True,
                              db_index=True)
    username = models.CharField('Имя пользователя', max_length=64)
    is_staff = models.BooleanField('Статус персонала', default=False)
    is_superuser = models.BooleanField('Статус суперпользователя', default=False)
    is_active = models.BooleanField('Активирован', default=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлён', auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', )

    objects = UserManager()

    class Meta:
        ordering = ('-email',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def __str__(self):
        return self.email
