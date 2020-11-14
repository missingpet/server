from django.contrib import admin

from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'created_at'
    )
    list_filter = (
        'announcement_type',
        'animal_type'
    )
