from rest_framework.permissions import IsAuthenticatedOrReadOnly


class AnnouncementPermission(IsAuthenticatedOrReadOnly):
    """Custom permission class which allows to delete \
    announcement only for authors, create announcements \
    only for authenticated users and to read announcements for any user."""

    def has_object_permission(self, request, view, obj):
        return (obj.user == request.user if request.method == "DELETE" else
                super(AnnouncementPermission, self).has_object_permission(
                    request, view, obj))
