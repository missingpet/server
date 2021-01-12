from django.urls import include
from django.urls import path

from .views import AnnouncementListCreateAPIView
from .views import AnnouncementRetrieveDestroyAPIView
from .views import AnnouncementsMapForUserListAPIView
from .views import AnnouncementsMapListAPIView
from .views import FeedForUserListAPIView
from .views import UserAnnouncementsListAPIView

user_urls = [
    path(
        "<int:user_id>/announcements/",
        UserAnnouncementsListAPIView.as_view(),
        name="user-announcements",
    ),
    path("<int:user_id>/feed/", FeedForUserListAPIView.as_view(), name="feed-for-user"),
    path(
        "<int:user_id>/announcements_map/",
        AnnouncementsMapForUserListAPIView.as_view(),
        name="announcements-map-for-user",
    ),
]

announcement_urls = [
    path(
        "<int:pk>/",
        AnnouncementRetrieveDestroyAPIView.as_view(),
        name="retrieve-destroy-announcement",
    ),
    path("", AnnouncementListCreateAPIView.as_view(), name="list-create-announcement"),
]

announcements_map_urls = [
    path("", AnnouncementsMapListAPIView.as_view(), name="announcements-map"),
]

urlpatterns = [
    path("user/", include(user_urls)),
    path("announcement/", include(announcement_urls)),
    path("announcements_map/", include(announcements_map_urls)),
]
