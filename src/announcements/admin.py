from django.contrib.admin import ModelAdmin, register
from django.utils.html import format_html

from .models import Announcement


@register(Announcement)
class AnnouncementAdmin(ModelAdmin):
    list_display = (
        "id",
        "user",
        "announcement_type",
        "animal_type",
        "created_at",
    )
    list_display_links = (
        "id",
        "user",
    )
    list_filter = ('announcement_type', 'animal_type')
    readonly_fields = (
        "get_photo",
        "created_at",
        "updated_at",
    )
    search_fields = ('description', 'address')

    def get_photo(self, obj):
        src = obj.photo.url
        width = 200
        return format_html('<img src={} width={}>'.format(src, width))

    get_photo.short_description = 'Миниатюра'

    save_on_top = True
