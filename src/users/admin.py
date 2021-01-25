from django.contrib.admin import ModelAdmin, register

from .models import User


@register(User)
class UserAdmin(ModelAdmin):
    readonly_fields = ('last_login', )
    list_display = ('id', 'username', 'email', 'created_at', 'is_active')
    list_display_links = (
        'id',
        'username',
        'email',
    )
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    save_on_top = True
