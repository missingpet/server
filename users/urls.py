from django.urls import path

from .views import SignInAPIView
from .views import SignOutAPIView
from .views import SignUpAPIView
from .views import TokenRefreshAPIView

urlpatterns = [
    path("signup/", SignUpAPIView.as_view(), name="sign-up"),
    path("signin/", SignInAPIView.as_view(), name="sign-in"),
    path("signout/", SignOutAPIView.as_view(), name="sign-out"),
    path("token/refresh/", TokenRefreshAPIView.as_view(),
         name="refresh-token"),
]
