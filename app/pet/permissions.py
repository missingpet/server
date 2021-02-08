from rest_framework.permissions import IsAuthenticatedOrReadOnly


class AnnouncementPermission(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            return obj.user == request.user
        return super(AnnouncementPermission,
                     self).has_object_permission(request, view, obj)
