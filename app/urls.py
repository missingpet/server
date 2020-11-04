from .views import *
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('auth/signup/', SignUpAPIView.as_view(), name='signup'),
    path('auth/signin/', SignInAPIView.as_view(), name='login'),
    path('auth/signout/', SignOutAPIView.as_view(), name='logout'),
    path('auth/refresh-token/', TokenRefreshView.as_view(), name='refresh-token'),
    path('auth/confirm-email/', ConfirmEmailAPIView.as_view(), name='confirm-email'),
    path('auth/request-password-reset/', RequestPasswordResetAPIView.as_view(), name='request-password-reset'),
    path(
        'auth/confirm-password-reset/<uidb64>/<token>/',
        ConfirmPasswordResetAPIView.as_view(),
        name='confirm-password-reset'
    ),
    path('auth/complete-password-reset/', CompletePasswordResetAPIView.as_view(), name='complete-reset-password'),

    path('announcement/feed/', FeedAnnouncementListAPIView.as_view(), name='announcements-feed'),
    path('announcement/create/', AnnouncementCreateAPIView.as_view(), name='create-announcement'),
    path('announcement/delete/<int:pk>/', AnnouncementDeleteAPIView.as_view(), name='delete-announcement'),
    path('announcement/my/', MyAnnouncementListAPIView.as_view(), name='my-announcements'),
    path('announcement/mapinfo/', AnnouncementMapInfoListAPIView.as_view(), name='map-info'),
    path('announcement/retrieve/<int:pk>/', AnnouncementRetrieveAPIView.as_view(), name='retrieve-announcement'),
]