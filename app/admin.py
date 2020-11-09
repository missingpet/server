from django.contrib import admin

from .models import User, Announcement


admin.site.register(User)
admin.site.register(Announcement)
