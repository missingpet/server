from django import forms

from . import models


class UserAdminForm(forms.ModelForm):
    """Form which uses to provide more detailed\
    information for \"User\" model in admin site."""

    class Meta:
        model = models.User
        fields = "__all__"
        help_texts = {
            "is_active": "Вместо удаления аккауна отключите этот пункт.",
            "is_staff":
            "Может ли пользователь заходить в административную панель.",
            "is_superuser":
            "Имеет ли пользователь все права без их явного назначения.",
            "nickname": "Никнеймы не являются уникальными.",
            "email":
            "Адрес электронной почты является уникальным для каждого пользователя.",
            "password": "Пароль хранится в виде хеша.",
        }


class AnnouncementAdminForm(forms.ModelForm):
    """Form which uses to provide more detailed\
    information for \"Announcement\" model in admin site."""

    class Meta:
        model = models.Announcement
        fields = "__all__"
        help_texts = {
            "user":
            "Автор объявления.",
            "description":
            "Подробное описание объявления.",
            "contact_phone_number":
            "Номер телефона, по которому можно связаться с автором объявления.",
            "address":
            "Это адрес, по которому животное было найдено или потеряно.",
        }
