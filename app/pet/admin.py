"""
Module which contains admin models description.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from . import models
from .forms import CustomUserChangeForm
from .forms import CustomUserCreationForm


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    readonly_fields = ("last_login", "created_at", "updated_at")
    list_display = ("id", "email", "nickname", "created_at", "updated_at")
    list_display_links = (
        "id",
        "email",
        "nickname",
    )
    list_filter = ("is_staff", "is_superuser", "is_active")
    fieldsets = (
        (None, {
            "fields": ("password", "email", "nickname", "is_active", "groups")
        }),
        ("Особые права", {
            "fields": ("is_superuser", "is_staff")
        }),
        (
            "Дополнительно",
            {
                "classes": ("collapse", ),
                "fields": ("created_at", "updated_at")
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide", ),
                "fields": (
                    "email",
                    "nickname",
                    "password1",
                    "password2",
                    "is_active",
                    "groups",
                ),
            },
        ),
        (
            "Особые права",
            {
                "classes": ("collapse", ),
                "fields": ("is_superuser", "is_staff")
            },
        ),
    )
    search_fields = ("email", "nickname")
    ordering = ("email", )
    save_on_top = True


@admin.register(models.Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "announcement_type", "animal_type",
                    "created_at")
    list_display_links = ("id", "user")
    list_filter = ("announcement_type", "animal_type")
    readonly_fields = ("get_photo", "created_at", "updated_at")
    search_fields = ("description", "address")

    def get_photo(self, obj):
        src = obj.photo.url
        width = 200
        return format_html(f"<img src={src} width={width}>")

    get_photo.short_description = "Миниатюра"

    save_on_top = True