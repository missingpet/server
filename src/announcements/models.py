from django.db.models import CASCADE
from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import FloatField
from django.db.models import ForeignKey
from django.db.models import ImageField
from django.db.models import IntegerField
from django.db.models import Model
from django.utils.translation import gettext_lazy as _

from config.settings import ANNOUNCEMENTS_PHOTO
from users.models import User


class Announcement(Model):
    """Объявление о пропавшем/найденном питомце."""

    LOST = 1
    FOUND = 2
    ANNOUNCEMENT_TYPES = ((LOST, _("Потеряно")), (FOUND, _("Найдено")))

    DOGS = 1
    CATS = 2
    OTHERS = 3
    ANIMAL_TYPES = ((DOGS, _("Собаки")), (CATS, _("Кошки")), (OTHERS, _("Иные")))

    user = ForeignKey(User, on_delete=CASCADE, verbose_name=_("Пользователь"))
    description = CharField(_("Описание"), max_length=5000)
    photo = ImageField(_("Фотография животного"), upload_to=ANNOUNCEMENTS_PHOTO)
    announcement_type = IntegerField(_("Тип объявления"), choices=ANNOUNCEMENT_TYPES)
    animal_type = IntegerField(_("Тип животного"), choices=ANIMAL_TYPES)
    address = CharField(_("Место пропажи или находки"), max_length=1000)
    latitude = FloatField(_("Широта"))
    longitude = FloatField(_("Долгота"))
    contact_phone_number = CharField(_("Контактный телефон"), max_length=12)
    created_at = DateTimeField(_("Создано"), auto_now_add=True)
    updated_at = DateTimeField(_("Обновлено"), auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Объявление")
        verbose_name_plural = _("Объявления")

    def save(self, *args, **kwargs):
        # При обновлении фотографии старую фотографию удаляем.
        this_record = Announcement.objects.filter(id=self.id).first()
        if this_record:
            if this_record.photo != self.photo:
                this_record.photo.delete(save=False)
        super(Announcement, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Удаляем фотографию вместе с объявлением.
        self.photo.delete(save=False)
        super(Announcement, self).delete(*args, **kwargs)

    def __str__(self):
        return str(self.user)
