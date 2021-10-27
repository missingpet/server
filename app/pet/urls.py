"""
Module which contains api urls.
"""
from django.urls import include
from django.urls import path

from . import views

users_urls = [
    path('new/', views.UserCreateView.as_view(), name='register'),
    path('me/', views.AuthView.as_view(), name='login'),
    path(
        "<int:user_id>/announcements/",
        views.UserAnnouncementsListView.as_view(),
        name="user-announcements",
    ),
    path(
        "<int:user_id>/feed/",
        views.FeedForUserListView.as_view(),
        name="feed-for-user",
    ),
    path(
        "<int:user_id>/map/",
        views.MapForUserListView.as_view(),
        name="map-for-user",
    ),
    path(
        "nickname/",
        views.UserNicknameChangeView.as_view(),
        name="change-user-nickname",
    ),
]

announcements_urls = [
    path(
        "<int:pk>/",
        views.AnnouncementViewSet.as_view({
            "get": "retrieve",
            "delete": "destroy"
        }),
        name="retrieve-destroy-announcement",
    ),
    path(
        "",
        views.AnnouncementViewSet.as_view({
            "get": "list",
            "post": "create"
        }),
        name="list-create-announcement",
    ),
]

map_urls = [
    path("", views.MapListView.as_view(), name="map"),
]

settings_urls = [
    path("", views.SettingsView.as_view(), name="settings"),
]

urlpatterns = [
    path("users/", include(users_urls)),
    path("announcements/", include(announcements_urls)),
    path("map/", include(map_urls)),
    path("settings/", include(settings_urls)),
]
