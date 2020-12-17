from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import SignInAPIView
from .views import SignUpAPIView
from .views import SignOutAPIView


urlpatterns = [
    path(
        "signup/",
        SignUpAPIView.as_view(),
        name='sign-up'
    ),
    path(
        'signin/',
        SignInAPIView.as_view(),
        name='sign-in'
    ),
    path(
        'signout/',
        SignOutAPIView.as_view(),
        name='sign-out'
    ),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='refresh-token'
    ),
]
