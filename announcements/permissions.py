from rest_framework.permissions import BasePermission


class IsAnnouncementAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        return obj.user == request.user
