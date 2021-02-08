from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserCreationCustomForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "nickname")


class UserChangeCustomForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "nickname")
