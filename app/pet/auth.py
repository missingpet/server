from django.contrib.auth import backends
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class EmailAuthBackend(backends.ModelBackend):
    """Custom backend to perform authentication via email."""
    def authenticate(self, request, username=None, password=None, **kwargs):
        """Authenticates user by email and password."""

        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel.objects.get(
                email=username,
                is_active=True,
            )
        except UserModel.DoesNotExist:
            pass
        else:
            if user.check_password(password):
                return user
