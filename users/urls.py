from .views import *

from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('signup/', SignUpAPIView.as_view(), name='signup'),
    path('signin/', SignInAPIView.as_view(), name='login'),
    path('signout/', SignOutAPIView.as_view(), name='logout'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh-token'),
]