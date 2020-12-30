from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ("last_login",)
    list_display = ("id", "username", "email", "created_at", "is_active")
    list_display_links = (
        "id",
        "username",
        "email",
    )
    list_filter = ("is_staff", "is_superuser")
    search_fields = ("username", "email")
    save_on_top = True
