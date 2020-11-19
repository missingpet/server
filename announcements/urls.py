from django.urls import path

from .views import *


urlpatterns = [
    path(
        'announcement/feed/',
        FeedAnnouncementListAPIView.as_view(),
        name='feed-announcements'
    ),
    path(
        'announcement/create/',
        AnnouncementCreateAPIView.as_view(),
        name='create-announcement'
    ),
    path(
        'announcement/delete/<int:pk>/',
        AnnouncementDestroyAPIView.as_view(),
        name='delete-announcement'
    ),
    path(
        'announcement/my/',
        MyAnnouncementListAPIView.as_view(),
        name='my-announcements'
    ),
    path(
        'announcement/retrieve/<int:pk>/',
        AnnouncementRetrieveAPIView.as_view(),
        name='retrieve-announcement'
    ),
    path(
        'announcement/feed/map/',
        FeedMapInfoListAPIView.as_view(),
        name='feed-map'
    ),
]
