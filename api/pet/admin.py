from django.contrib import admin
from django.utils.html import format_html

from . import models
from . import forms


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    form = forms.UserAdminForm
    readonly_fields = ('last_login', )
    list_display = ('id', 'nickname', 'email', 'created_at', 'is_active')
    list_display_links = ('id',
                          'nickname',
                          'email')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('nickname', 'email')
    save_on_top = True


@admin.register(models.Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    form = forms.AnnouncementAdminForm
    list_display = ('id',
                    'user',
                    'announcement_type',
                    'animal_type',
                    'created_at')
    list_display_links = ("id","user")
    list_filter = ('announcement_type', "animal_type")
    readonly_fields = ('get_photo', 'created_at', 'updated_at')
    search_fields = ('description', 'address')

    def get_photo(self, obj):
        return format_html("<img src={} width={}>".format(obj.photo.url, 200))

    get_photo.short_description = 'Миниатюра'

    save_on_top = True
