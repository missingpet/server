from django.urls import include
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from . import views

token_urls = [
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("verify/", TokenVerifyView.as_view(), name="verify"),
]

auth_urls = [
    path("signup/", views.SignUpAPIView.as_view(), name="sign-up"),
    path("signin/", views.SignInAPIView.as_view(), name="sign-in"),
    path("token/", include(token_urls)),
]

urlpatterns = [
    path("auth/", include(auth_urls)),
]
