"""Custom django-admin command to initialize default superuser."""
from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(email=settings.ADMIN_EMAIL).exists():
            User.objects.create_superuser(
                settings.ADMIN_EMAIL,
                settings.ADMIN_NICKNAME,
                settings.ADMIN_PASSWORD,
            )