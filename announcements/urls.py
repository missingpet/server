from django.urls import path

from .views import AllAnnouncementsListAPIView
from .views import AllMapInfoListAPIView
from .views import AnnouncementCreateAPIView
from .views import AnnouncementRetrieveDestroyAPIView
from .views import FeedAnnouncementsListAPIView
from .views import FeedMapInfoListAPIView
from .views import UserAnnouncementsListAPIView

urlpatterns = [
    path(
        "announcement/all/",
        AllAnnouncementsListAPIView.as_view(),
        name="all-announcements",
    ),
    path(
        "announcement/user/<int:user_id>/",
        UserAnnouncementsListAPIView.as_view(),
        name="user-announcements",
    ),
    path(
        "announcement/user/<int:user_id>/feed/",
        FeedAnnouncementsListAPIView.as_view(),
        name="feed-announcements",
    ),
    path(
        "announcement/<int:pk>/",
        AnnouncementRetrieveDestroyAPIView.as_view(),
        name="retrieve-destroy-announcement",
    ),
    path(
        "announcement/",
        AnnouncementCreateAPIView.as_view(),
        name="create-announcement",
    ),
    path(
        "announcement/map_info/all/",
        AllMapInfoListAPIView.as_view(),
        name="all-map-info",
    ),
    path(
        "announcement/map_info/user/<int:user_id>/feed/",
        FeedMapInfoListAPIView.as_view(),
        name="feed-map-info",
    ),
]
