from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.db import models


class UserManager(BaseUserManager):
    """Custom user manager."""

    def create_user(self, email, nickname, password, **extra_fields):
        if not email or not nickname:
            raise ValueError('All fields are required.')
        user = self.model(email=self.normalize_email(email), nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, nickname, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(email, nickname, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user with email as a username."""

    email = models.EmailField('Адрес электронной почты',
                              unique=True,
                              db_index=True)
    nickname = models.CharField('Никнейм', max_length=64)
    is_staff = models.BooleanField('Статус персонала', default=False)
    is_superuser = models.BooleanField('Статус суперпользователя', default=False)
    is_active = models.BooleanField('Активирован', default=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлён', auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('nickname', )

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class AnnouncementManager(models.Manager):
    """Custom announcement manager."""

    def get_feed_for_user(self, user_id):
        return self.get_queryset().exclude(user_id=user_id).order_by('-created_at')

    def get_announcements_of_user(self, user_id):
        return self.get_queryset().filter(user_id=user_id).order_by('-created_at')


class Announcement(models.Model):
    """Announcement of a missing or found pet."""

    LOST = 1
    FOUND = 2
    ANNOUNCEMENT_TYPES = ((LOST, 'Потеряно'), (FOUND, 'Найдено'))

    DOGS = 1
    CATS = 2
    OTHERS = 3
    ANIMAL_TYPES = ((DOGS, 'Собаки'), (CATS, 'Кошки'), (OTHERS, 'Иные'))

    user = models.ForeignKey(User,
                             models.CASCADE,
                             'announcements',
                             verbose_name="Пользователь")
    description = models.CharField("Описание", max_length=5000)
    photo = models.ImageField('Фотография животного',
                              upload_to=settings.ANNOUNCEMENTS_PHOTO)
    announcement_type = models.IntegerField("Тип объявления",
                                            choices=ANNOUNCEMENT_TYPES)
    animal_type = models.IntegerField("Тип животного", choices=ANIMAL_TYPES)
    address = models.CharField("Место пропажи или находки", max_length=1000)
    latitude = models.FloatField("Широта")
    longitude = models.FloatField("Долгота")
    contact_phone_number = models.CharField("Контактный телефон", max_length=12)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    objects = AnnouncementManager()

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return str(self.user)
