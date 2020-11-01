from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('auth/signup/', SignUpAPIView.as_view(), name='signup'),
    path('auth/confirm-email/', ConfirmEmailAPIView.as_view(), name='confirm-email'),
    path('auth/login/', LoginAPIView.as_view(), name='login'),
    path('auth/refresh-token/', TokenRefreshView.as_view(), name='refresh-token'),
    path('auth/request-password-reset/', RequestPasswordResetAPIView.as_view(), name='request-password-reset'),
    path('auth/confirm-password-reset/<uidb64>/<token>/', ConfirmPasswordResetAPIView.as_view(), name='confirm-password-reset'),
    path('auth/reset-password/', CompletePasswordResetAPIView.as_view(), name='reset-password'),
    path('auth/logout/', LogoutAPIView.as_view(), name='logout'),

    path('announcement/all/', AnnouncementListAPIView.as_view(), name='all-announcements'),
    path('announcement/create/', AnnouncementCreateAPIView.as_view(), name='create-announcement'),
    path('announcement/delete/<int:pk>/', AnnouncementDeleteAPIView.as_view(), name='delete-announcement'),
    path('announcement/myannouncement/', MyAnnouncementListAPIView.as_view(), name='user-announcement'),
    path('announcement/mapinfo/', MapAnnouncementInfoListAPIView.as_view(), name='map-info'),
]