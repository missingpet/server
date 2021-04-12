"""Django model data factories."""
import factory

from .. import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User


class PasswordResetConfirmationCodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PasswordResetConfirmationCode

    user = factory.SubFactory(UserFactory)


class AnnouncementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Announcement

    user = factory.SubFactory(UserFactory)
    photo = factory.django.ImageField()
