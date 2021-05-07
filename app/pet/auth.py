from django.contrib.auth import backends, get_user_model

UserModel = get_user_model()


class EmailAuthBackend(backends.ModelBackend):
    """Custom authentication backend to perform authentication via email."""

    def authenticate(self, request, username=None, password=None, **kwargs):

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
