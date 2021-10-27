from django.db.models import IntegerChoices


class AnnouncementType(IntegerChoices):
    """Тип объявления"""

    LOST = (1, "Потеряно")
    FOUND = (2, "Найдено")


class AnimalType(IntegerChoices):
    """Тип животного"""

    DOGS = (1, "Собаки")
    CATS = (2, "Кошки")
    OTHERS = (3, "Иные")