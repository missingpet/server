from django.contrib.auth import backends
from django.contrib.auth import get_user_model

from rest_framework import serializers

from . import const

UserModel = get_user_model()


def check_account_availability(user):
    """Checks if user is active."""

    if not user.is_active:
        raise serializers.ValidationError(const.INACTIVE_ACCOUNT_ERROR_MESSAGE)


class EmailAuthBackend(backends.ModelBackend):
    """Custom backend to perform authentication via email."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """Authenticates user by email and password."""

        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            pass
        else:
            check_account_availability(user)

            if user.check_password(password):
                return user
