from django.urls import include, path

from .views import (AllMapInfoListAPIView, AnnouncementListCreateAPIView,
                    AnnouncementRetrieveDestroyAPIView,
                    FeedAnnouncementsListAPIView, FeedMapInfoListAPIView,
                    UserAnnouncementsListAPIView)

user_urls = [
    path(
        "<int:user_id>/announcements/",
        UserAnnouncementsListAPIView.as_view(),
        name="user-announcements",
    ),
    path("<int:user_id>/feed/", FeedAnnouncementsListAPIView.as_view(), name="feed"),
    path(
        "<int:user_id>/objects_for_announcements_map/feed/",
        FeedMapInfoListAPIView.as_view(),
        name="feed-map-info",
    ),
]

announcement_urls = [
    path(
        "<int:pk>/",
        AnnouncementRetrieveDestroyAPIView.as_view(),
        name="retrieve-destroy-announcement",
    ),
    path("", AnnouncementListCreateAPIView.as_view(), name="create-announcement"),
]

objects_for_announcements_map_urls = [
    path("", AllMapInfoListAPIView.as_view(), name="all-map-info"),
]

urlpatterns = [
    path("user/", include(user_urls)),
    path("announcement/", include(announcement_urls)),
    path("objects_for_announcements_map/", include(objects_for_announcements_map_urls)),
]
