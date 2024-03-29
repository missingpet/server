import os
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from . import choices


class UserManager(BaseUserManager):
    """Custom user manager"""
    def create_user(self, email, nickname, password, **extra_fields):
        if not email or not nickname:
            raise ValueError("All fields are required.")
        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, nickname, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        return self.create_user(email, nickname, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model with email as a username"""

    email = models.EmailField(
        "Адрес электронной почты",
        unique=True,
        db_index=True,
    )
    nickname = models.CharField("Никнейм", max_length=64)
    is_staff = models.BooleanField("Статус персонала", default=False)
    is_superuser = models.BooleanField("Статус суперпользователя",
                                       default=False)
    is_active = models.BooleanField("Активирован", default=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлён", auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("nickname", )

    objects = UserManager()

    class Meta:
        ordering = ("-created_at", )
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


def upload_photo(instance, filename):
    extension = os.path.splitext(filename)[1]
    filename = uuid4().hex
    path = os.path.join(settings.ANNOUNCEMENTS_PHOTOS,
                        "{}{}".format(filename, extension))
    return path


class AnnouncementManager(models.Manager):
    pass


class Announcement(models.Model):
    """Объявление о пропавшем или найденном питомце"""

    ANNOUNCEMENT_TYPES = choices.AnnouncementType.choices
    ANIMAL_TYPES = choices.AnimalType.choices

    user = models.ForeignKey(
        User,
        models.CASCADE,
        "announcements",
        verbose_name="Пользователь",
    )
    description = models.CharField("Описание", max_length=5000)
    photo = models.ImageField("Фотография животного", upload_to=upload_photo)
    announcement_type = models.IntegerField("Тип объявления",
                                            choices=ANNOUNCEMENT_TYPES)
    animal_type = models.IntegerField("Тип животного", choices=ANIMAL_TYPES)
    address = models.CharField("Место пропажи или находки", max_length=1000)
    latitude = models.FloatField("Широта")
    longitude = models.FloatField("Долгота")
    contact_phone_number = models.CharField("Контактный телефон",
                                            max_length=12)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    objects = AnnouncementManager()

    class Meta:
        ordering = ("-created_at", )
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return str(self.user)