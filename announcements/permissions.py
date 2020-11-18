from rest_framework.permissions import IsAuthenticated


class IsAnnouncementAuthor(IsAuthenticated):
    """Является ли пользователель автором объявления."""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
