from django.urls import include
from django.urls import path

from . import views

user_urls = [
    path('<int:user_id>/announcements/',
         views.UserAnnouncementsListAPIView.as_view(),
         name='user-announcements'),
    path('<int:user_id>/feed/',
         views.FeedForUserListAPIView.as_view(),
         name='feed-for-user'),
    path('<int:user_id>/announcements_map/',
         views.AnnouncementsMapForUserListAPIView.as_view(),
         name='announcements-map-for-user'),
]

announcement_urls = [
    path("<int:pk>/", views.AnnouncementViewSet.as_view({"delete": "destroy", "get": "retrieve"}),
         name="retrieve-destroy-announcement"),
    path("", views.AnnouncementViewSet.as_view({"post": "create", "get": "list"}),
         name="create-announcement"),
]

announcements_map_urls = [
    path("", views.AnnouncementsMapListAPIView.as_view(), name="announcements-map"),
]

urlpatterns = [
    path("user/", include(user_urls)),
    path("announcement/", include(announcement_urls)),
    path("announcements_map/", include(announcements_map_urls)),
]
