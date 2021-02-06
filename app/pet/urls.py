from django.urls import include
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView

from . import views

token_urls = [
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("verify/", TokenVerifyView.as_view(), name="verify"),
]

auth_urls = [
    path("register/", views.UserCreateView.as_view(), name="register"),
    path("login/", views.AuthView.as_view(), name="login"),
    path("token/", include(token_urls)),
]

user_urls = [
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
        "<int:user_id>/announcements_map/",
        views.AnnouncementsMapForUserListView.as_view(),
        name="announcements-map-for-user",
    ),
]

announcement_urls = [
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

announcements_map_urls = [
    path("",
         views.AnnouncementsMapListView.as_view(),
         name="announcements-map"),
]

urlpatterns = [
    path("user/", include(user_urls)),
    path("announcement/", include(announcement_urls)),
    path("announcements_map/", include(announcements_map_urls)),
    path("auth/", include(auth_urls)),
]
