from django.urls import path

from .views import FeedAnnouncementListAPIView
from .views import AnnouncementRetrieveAPIView
from .views import AllAnnouncementListAPIView
from .views import AnnouncementDestroyAPIView
from .views import MyAnnouncementListAPIView
from .views import AnnouncementCreateAPIView
from .views import FeedMapInfoListAPIView
from .views import AllMapInfoListAPIView


urlpatterns = [
    path(
        "announcement/feed/",
        FeedAnnouncementListAPIView.as_view(),
        name="feed-announcements",
    ),
    path(
        "announcement/retrieve/<int:pk>/",
        AnnouncementRetrieveAPIView.as_view(),
        name="retrieve-announcement",
    ),
    path(
        "announcement/all/",
        AllAnnouncementListAPIView.as_view(),
        name="all-announcements",
    ),
    path(
        "announcement/delete/<int:pk>/",
        AnnouncementDestroyAPIView.as_view(),
        name="delete-announcement",
    ),
    path(
        "announcement/my/", MyAnnouncementListAPIView.as_view(), name="my-announcements"
    ),
    path(
        "announcement/create/",
        AnnouncementCreateAPIView.as_view(),
        name="create-announcement",
    ),
    path("announcement/feed/map/", FeedMapInfoListAPIView.as_view(), name="feed-map"),
    path("announcement/all/map/", AllMapInfoListAPIView.as_view(), name="all-map"),
]
