"""Custom django-admin command to perform password change."""

from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand

from ...models import User


class Command(BaseCommand):
    def add_arguments(self, parser):

        parser.add_argument("-e",
                            "--email",
                            type=str,
                            help="Адрес электронной почты")

        parser.add_argument("-p", "--password", type=str, help="Пароль")

    def handle(self, *args, **options):
        email = options.get("email")
        password = options.get("password")

        if not email or not password:
            self.stderr.write("Адрес электронной почты или пароль не заданы")
            return

        try:
            user = User.objects.get(email=email, is_active=True)
        except ObjectDoesNotExist:
            self.stderr.write("Пользователь не найден")
            return

        user.set_password(password)
        user.save()
        self.stderr.write(f"Пароль изменен на {password}")
