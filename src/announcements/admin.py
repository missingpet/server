from django.contrib import admin
from django.utils.html import format_html

from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'user',
                    'announcement_type',
                    'animal_type',
                    'created_at')
    list_display_links = ("id","user")
    list_filter = ("announcement_type", "animal_type")
    readonly_fields = ('get_photo', 'created_at', 'updated_at')
    search_fields = ("description", "address")

    def get_photo(self, obj):
        return format_html("<img src={} width={}>".format(obj.photo.url, 200))

    get_photo.short_description = "Миниатюра"

    save_on_top = True
