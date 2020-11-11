from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist

from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    """Менеджер пользователей"""
    def create_user(self, email, username, password=None):
        if email is None:
            raise TypeError('Адрес электронной почты не может иметь значение None.')
        if username is None:
            raise TypeError('Имя пользователя не может иметь значение None.')
        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password=None):
        if password is None:
            raise TypeError('Пароль не может иметь значение None.')
        user = self.create_user(username=username, email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Пользователь"""
    email = models.CharField(
        'Адрес электронной почты',
        max_length=255,
        unique=True,
        db_index=True
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=64,
        unique=True,
        db_index=True
    )
    is_active = models.BooleanField(
        'Активирован',
        default=True
    )
    is_staff = models.BooleanField(
        'Персонал',
        default=False
    )
    is_superuser = models.BooleanField(
        'Суперпользователь',
        default=False
    )
    created_at = models.DateTimeField(
        'Создан',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        'Обновлён',
        auto_now=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        ordering = ['-email', '-username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def tokens(self):
        refresh_token = RefreshToken.for_user(self)
        return {'refresh': f'{refresh_token}', 'access': f'{refresh_token.access_token}'}

    def __str__(self):
        return '{}'.format(self.email)


class Announcement(models.Model):
    """Объявление"""
    LOST = 1
    FOUND = 2
    ANNOUNCEMENT_TYPES = (
        (LOST, 'Потеряно'),
        (FOUND, 'Найдено')
    )

    DOG = 1
    CAT = 2
    OTHER = 3
    ANIMAL_TYPES = (
        (DOG, 'Собака'),
        (CAT, 'Кошка'),
        (OTHER, 'Другое')
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=User._meta.verbose_name
    )
    description = models.CharField(
        'Описание',
        max_length=1000,
        default='Описание отсутствует'
    )
    photo = models.ImageField(
        'Фотография животного',
        upload_to='announcements',
    )
    announcement_type = models.IntegerField(
        'Тип объявления',
        choices=ANNOUNCEMENT_TYPES,
        default=LOST
    )
    animal_type = models.IntegerField(
        'Тип животного',
        choices=ANIMAL_TYPES,
        default=DOG
    )
    address = models.CharField(
        'Место пропажи/находки',
        max_length=500,
        blank=True,
        null=True
    )
    latitude = models.FloatField(
        'Широта',
        blank=True,
        null=True
    )
    longitude = models.FloatField(
        'Долгота',
        blank=True,
        null=True
    )
    contact_phone_number = models.CharField(
        'Контактный телефон',
        max_length=12
    )
    created_at = models.DateTimeField(
        'Создано',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        'Изменено',
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def save(self, *args, **kwargs):
        try:
            this_record = Announcement.objects.get(id=self.id)
            if this_record.photo != self.photo:
                this_record.photo.delete(save=False)
        except ObjectDoesNotExist:
            pass
        super(Announcement, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.photo.delete(save=False)
        super(Announcement, self).delete(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.user)
