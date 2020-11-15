from .views import SignInAPIView
from .views import SignUpAPIView
from .views import SignOutAPIView

from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path(
        'signup/',
        SignUpAPIView.as_view(),
        name='signup'
    ),
    path(
        'signin/',
        SignInAPIView.as_view(),
        name='login'
    ),
    path(
        'signout/',
        SignOutAPIView.as_view(),
        name='logout'
    ),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='refresh-token'
    ),
]
