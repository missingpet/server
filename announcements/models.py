from django.db.models import Model
from django.db.models import CharField
from django.db.models import ImageField
from django.db.models import IntegerField
from django.db.models import FloatField
from django.db.models import DateTimeField
from django.db.models import ForeignKey
from django.db.models import CASCADE

from django.core.exceptions import ObjectDoesNotExist

from users.models import User


class Announcement(Model):
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

    user = ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name=User._meta.verbose_name
    )
    description = CharField(
        'Описание',
        max_length=1000,
        blank=True,
        null=True
    )
    photo = ImageField(
        'Фотография животного',
        upload_to='announcements',
    )
    announcement_type = IntegerField(
        'Тип объявления',
        choices=ANNOUNCEMENT_TYPES,
        default=LOST
    )
    animal_type = IntegerField(
        'Тип животного',
        choices=ANIMAL_TYPES,
        default=DOG
    )
    address = CharField(
        'Место пропажи/находки',
        max_length=500,
        blank=True,
        null=True
    )
    latitude = FloatField(
        'Широта',
        blank=True,
        null=True
    )
    longitude = FloatField(
        'Долгота',
        blank=True,
        null=True
    )
    contact_phone_number = CharField(
        'Контактный телефон',
        max_length=12
    )
    created_at = DateTimeField(
        'Создано',
        auto_now_add=True
    )
    updated_at = DateTimeField(
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
