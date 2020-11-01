from rest_framework import generics, status, permissions
from rest_framework.generics import get_object_or_404
from .serializers import *
from rest_framework.response import Response
from .models import User, Announcement
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import *
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
import jwt
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsAnnouncementAuthor


class SignUpAPIView(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request):
        user = request.data
        serializer=self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])
        access_token = RefreshToken.for_user(user).access_token

        current_site_domain = get_current_site(request).domain
        relative_link = reverse('confirm-email')
        absolute_url = f'http://{current_site_domain}{relative_link}?token={access_token}'

        email_body = f'Здравствуйте, {user.username}! ' \
                     f'Для подтверждения адреса электронной почты перейдите по ссылке: \n{absolute_url}'
        data = {
            'email_subject': 'Подтверждение адреса электронной почты.',
            'email_body': email_body,
            'email_to': user.email
        }

        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)


class ConfirmEmailAPIView(generics.GenericAPIView):

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.save()
            else:
                return Response(
                    {
                        'detail': 'Вы ранее уже подтверждали адрес электронной почты.'
                    },
                    status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
                )

            return Response({'success': 'Адрес электронной почты успешно подтверждён.'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Данная ссылка больше недействительна.'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError:
            return Response({'error': 'Неверный токен.'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer= self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': 'Выход из профиля произведен успешно.'}, status=status.HTTP_204_NO_CONTENT)


class RequestPasswordResetAPIView(generics.GenericAPIView):
    serializer_class = RequestPasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=serializer.data['email'])
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)

        current_site_domain = get_current_site(request=request).domain
        relative_link = reverse('confirm-password-reset', kwargs={'uidb64': uidb64, 'token': token})
        absolute_url = f'http://{current_site_domain}{relative_link}?token={token}'

        email_body = f'Для сброса пароля перейдите по ссылке: \n{absolute_url}\n\n'\
                     f'Проигнорируйте это сообщение, если вы не запрашивали сброс пароля.'

        data = {'email_subject': 'Сброс пароля.', 'email_body': email_body, 'email_to': user.email}

        Util.send_email(data)

        return Response(
            {
                'success': f'На адрес {user.email} отправлено письмо для сброса пароля.'
            },
            status=status.HTTP_200_OK
        )


class ConfirmPasswordResetAPIView(generics.GenericAPIView):

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user=user, token=token):
                return Response({'error': 'Неверный токен.'}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success': 'Адрес электронной почты успешно подтверждён.'}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError:
            return Response({'error': 'Неверный токен.'}, status=status.HTTP_401_UNAUTHORIZED)


class CompletePasswordResetAPIView(generics.GenericAPIView):
    serializer_class = CompletePasswordResetSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': 'Пароль успешно сброшен.'}, status=status.HTTP_200_OK)


class AnnouncementListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = AnnouncementRetrieveSerializer

    def get_queryset(self):
        user = self.request.user
        return Announcement.objects.all().exclude(user=user)


class MyAnnouncementListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsAnnouncementAuthor, )
    serializer_class = AnnouncementRetrieveSerializer

    def get_queryset(self):
        user = self.request.user
        return Announcement.objects.filter(user=user)


class AnnouncementCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = AnnouncementCreateSerializer
    queryset = Announcement.objects.all()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class AnnouncementDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, IsAnnouncementAuthor, )
    queryset = Announcement.objects.all()


class AnnouncementUpdateAPIView(generics.UpdateAPIView):
    pass


class AnnouncementMapInfoListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = MapAnnouncementInfoSerializer

    def get_queryset(self):
        return Announcement.objects.all().exclude(place__isnull=True)


class AnnouncementByIdAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementRetrieveSerializer
