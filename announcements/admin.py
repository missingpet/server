from django.contrib import admin

from django.utils.html import format_html

from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "announcement_type",
        "animal_type",
        "created_at",
    )
    list_filter = ("announcement_type", "animal_type")
    readonly_fields = (
        "get_photo",
        "created_at",
        "updated_at",
    )

    def get_photo(self, obj):
        src = obj.photo.url
        width = 200
        return format_html("<img src={} width={}>".format(src, width))

    get_photo.short_description = "Миниатюра"

    save_on_top = True
