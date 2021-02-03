from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models


class AnnouncementManager(models.Manager):

    def get_feed_for_user(self, user_id):
        return self.get_queryset().exclude(user_id=user_id).order_by('-created_at')

    def get_announcements_of_user(self, user_id):
        return self.get_queryset().filter(user_id=user_id).order_by('-created_at')


class Announcement(models.Model):
    LOST = 1
    FOUND = 2
    ANNOUNCEMENT_TYPES = ((LOST, "Потеряно"), (FOUND, "Найдено"))

    DOGS = 1
    CATS = 2
    OTHERS = 3
    ANIMAL_TYPES = ((DOGS, "Собаки"), (CATS, "Кошки"), (OTHERS, "Иные"))

    user = models.ForeignKey(get_user_model(),
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
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return str(self.user)
