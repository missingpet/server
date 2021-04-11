"""Django model data factories."""
import factory

from .. import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User
