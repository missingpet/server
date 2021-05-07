from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm

from .models import User


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "nickname")


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "nickname")
