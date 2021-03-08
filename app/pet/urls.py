from django.urls import include
from django.urls import path

from . import views

auth_urls = [
    path("register/", views.UserCreateView.as_view(), name="register"),
    path("login/", views.AuthView.as_view(), name="login"),
]

user_urls = [
    path(
        "<int:user_id>/announcements/",
        views.UserAnnouncementsListView.as_view(),
        name="user-announcements",
    ),
    path(
        "<int:user_id>/feed/", views.FeedForUserListView.as_view(), name="feed-for-user"
    ),
    path("<int:user_id>/map/", views.MapForUserListView.as_view(), name="map-for-user"),
]

announcement_urls = [
    path(
        "<int:pk>/",
        views.AnnouncementViewSet.as_view({"get": "retrieve", "delete": "destroy"}),
        name="retrieve-destroy-announcement",
    ),
    path(
        "",
        views.AnnouncementViewSet.as_view({"get": "list", "post": "create"}),
        name="list-create-announcement",
    ),
]

map_urls = [
    path("", views.MapListView.as_view(), name="map"),
]

urlpatterns = [
    path("user/", include(user_urls)),
    path("announcement/", include(announcement_urls)),
    path("map/", include(map_urls)),
    path("auth/", include(auth_urls)),
]
