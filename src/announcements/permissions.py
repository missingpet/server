from rest_framework import permissions


class IsAnnouncementAuthorOrAuthenticatedOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            return obj.user == request.user
        return super(IsAnnouncementAuthorOrAuthenticatedOrReadOnly,
                     self).has_object_permission(request, view, obj)
