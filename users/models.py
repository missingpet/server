from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db.models import BooleanField, CharField, DateTimeField, EmailField
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    """Менеджер пользователей."""

    def create_user(self, email, username, password):
        """Создание пользователя."""
        if not email:
            raise ValueError("Email address must be set.")
        if not username:
            raise ValueError("Username must be set.")
        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password):
        """Создание суперпользователя."""
        if not password:
            raise ValueError("Password must be set.")
        user = self.create_user(username=username, email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Пользователь с email."""

    email = EmailField("Адрес электронной почты", unique=True, db_index=True)
    username = CharField("Имя пользователя", max_length=64, unique=True, db_index=True)
    is_active = BooleanField("Активирован", default=True)
    is_staff = BooleanField("Персонал", default=False)
    is_superuser = BooleanField("Суперпользователь", default=False)
    created_at = DateTimeField("Создан", auto_now_add=True)
    updated_at = DateTimeField("Обновлён", auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)

    objects = UserManager()

    class Meta:
        ordering = ("-username", "-email")
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def __str__(self):
        return self.email
