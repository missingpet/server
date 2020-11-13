from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('last_login', )
    list_display = ('email', 'username', 'created_at', 'is_active')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('username', 'email')
