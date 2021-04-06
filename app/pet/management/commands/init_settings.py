"""Custom django-admin command to initialize default mobile app settings."""
from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import Settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not Settings.objects.filter(
                settings_name=settings.SETTINGS_ACTUAL_NAME).exists():
            Settings.objects.create(
                settings_name=settings.SETTINGS_ACTUAL_NAME)
