from rest_framework.permissions import IsAuthenticatedOrReadOnly


class AnnouncementPermission(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return (obj.user == request.user if request.method == "DELETE" else
                super(AnnouncementPermission, self).has_object_permission(
                    request, view, obj))
