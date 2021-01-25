from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import SignInAPIView, SignOutAPIView, SignUpAPIView

token_urls = [
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('verify/', TokenVerifyView.as_view(), name='verify'),
]

auth_urls = [
    path('signup/', SignUpAPIView.as_view(), name='sign-up'),
    path('signin/', SignInAPIView.as_view(), name='sign-in'),
    path('signout/', SignOutAPIView.as_view(), name='sign-out'),
    path('token/', include(token_urls)),
]

urlpatterns = [
    path('auth/', include(auth_urls)),
]
