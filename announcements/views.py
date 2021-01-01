from drf_yasg.openapi import IN_PATH
from drf_yasg.openapi import IN_QUERY
from drf_yasg.openapi import Parameter
from drf_yasg.openapi import TYPE_INTEGER
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

from .models import Announcement
from .permissions import IsAnnouncementAuthorOrReadOnly
from .serializers import AnnouncementCreateSerializer
from .serializers import AnnouncementSerializer
from .serializers import MapInfoSerializer


class AllAnnouncementsListAPIView(ListAPIView):
    """Все объявления."""

    permission_classes = (AllowAny,)
    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.all()
    url_kwargs = ("page",)

    @swagger_auto_schema(
        operation_summary="Список всех объявлений.",
        operation_description="Возвращает список всех объявлений.",
        manual_parameters=[
            Parameter(
                url_kwargs[0],
                IN_QUERY,
                type=TYPE_INTEGER,
                description="Номер страницы в наборе результатов с пагинацией.",
            ),
        ],
        responses={"200": AnnouncementSerializer, "404": "Неправильная страница."},
    )
    def get(self, request, *args, **kwargs):
        return super(AllAnnouncementsListAPIView, self).get(request, *args, **kwargs)


class UserAnnouncementsListAPIView(ListAPIView):
    """Объявления пользователя."""

    permission_classes = (AllowAny,)
    serializer_class = AnnouncementSerializer
    url_kwargs = ("user_id", "page")

    @swagger_auto_schema(
        operation_summary="Список объявлений пользователя.",
        operation_description="""
        Возвращает список объявлений пользователя по указанному id пользователя.
        Сюда входят только те объявления, которые были созданы указанным пользователем.
        """,
        manual_parameters=[
            Parameter(
                url_kwargs[0],
                IN_PATH,
                type=TYPE_INTEGER,
                description="Уникальный идентификатор пользователя.",
            ),
            Parameter(
                url_kwargs[1],
                IN_QUERY,
                type=TYPE_INTEGER,
                description="Номер страницы в наборе результатов с пагинацией.",
            ),
        ],
        responses={"200": AnnouncementSerializer, "404": "Неправильная страница."},
    )
    def get(self, request, *args, **kwargs):
        return super(UserAnnouncementsListAPIView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return Announcement.objects.filter(user_id=self.kwargs.get(self.url_kwargs[0]))


class FeedAnnouncementsListAPIView(ListAPIView):
    """Лента объявлений."""

    permission_classes = (AllowAny,)
    serializer_class = AnnouncementSerializer
    url_kwargs = ("user_id", "page")

    @swagger_auto_schema(
        operation_summary="Лента объявлений.",
        operation_description="""
        Возвращает ленту объявлений для пользователя с указанным id.
        Сюда не входят объявления, созданные указанным пользователем.
        """,
        manual_parameters=[
            Parameter(
                url_kwargs[0],
                IN_PATH,
                type=TYPE_INTEGER,
                description="Уникальный идентификатор пользователя.",
            ),
            Parameter(
                url_kwargs[1],
                IN_QUERY,
                type=TYPE_INTEGER,
                description="Номер страницы в наборе результатов с пагинацией.",
            ),
        ],
        responses={"200": AnnouncementSerializer, "404": "Неправильная страница."},
    )
    def get(self, request, *args, **kwargs):
        return super(FeedAnnouncementsListAPIView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return Announcement.objects.exclude(
            user_id=self.kwargs.get(self.lookup_url_kwarg)
        )


class AnnouncementCreateAPIView(CreateAPIView):
    """Создание объявления."""

    permission_classes = (IsAuthenticated,)
    serializer_class = AnnouncementCreateSerializer
    queryset = Announcement.objects.all()

    @swagger_auto_schema(
        operation_summary="Создание объявления.",
        operation_description="Создаёт новое объявление.",
        responses={
            "201": AnnouncementSerializer,
            "400": "Не заполнено обязательное поле.",
            "403": "Учетные данные не были предоставлены.",
        },
    )
    def post(self, request, *args, **kwargs):
        return super(AnnouncementCreateAPIView, self).post(request, *args, **kwargs)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class AnnouncementRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    """Получение/удаление объявления."""

    serializer_class = AnnouncementSerializer
    permission_classes = (IsAnnouncementAuthorOrReadOnly,)
    queryset = Announcement.objects.all()
    url_kwargs = ("id",)

    @swagger_auto_schema(
        operation_summary="Получение объявления.",
        operation_description="Возвращает объявление с указанным идентификатором.",
        manual_parameters=[
            Parameter(
                url_kwargs[0],
                IN_PATH,
                type=TYPE_INTEGER,
                description="Уникальный идентификатор объявления.",
            )
        ],
        responses={"200": AnnouncementSerializer, "404": "Объявление не найдено."},
    )
    def get(self, request, *args, **kwargs):
        return super(AnnouncementRetrieveDestroyAPIView, self).get(
            request, *args, **kwargs
        )

    @swagger_auto_schema(
        operation_summary="Удаление объявления.",
        operation_description="Удаляет объявление с указанным идентификатором.",
        manual_parameters=[
            Parameter(
                "id",
                IN_PATH,
                type=TYPE_INTEGER,
                description="Уникальный идентификатор объявления.",
            )
        ],
        responses={
            "204": "Объявление успешно удалено.",
            "403": """
                Учетные данные не были предоставлены.

                У вас недостаточно прав для выполнения данного действия.
                """,
            "404": "Объявление не найдено.",
        },
    )
    def delete(self, request, *args, **kwargs):
        return super(AnnouncementRetrieveDestroyAPIView, self).delete(
            request, *args, **kwargs
        )


class AllMapInfoListAPIView(ListAPIView):
    """
    Список всех объектов вида "id, широта, долгота".
    Это нужно для маркеров на карте объявлений.
    """

    permission_classes = (AllowAny,)
    serializer_class = MapInfoSerializer
    queryset = Announcement.objects.all()
    pagination_class = None

    @swagger_auto_schema(
        operation_summary='Список всех объектов вида "id, широта, долгота".',
        operation_description='Возвращает список всех объектов вида "id, широта, долгота".',
    )
    def get(self, request, *args, **kwargs):
        return super(AllMapInfoListAPIView, self).get(request, *args, **kwargs)


class FeedMapInfoListAPIView(ListAPIView):
    """
    Список объектов ленты вида "id, широта, долгота" для заданного пользователя.
    Это нужно для маркеров на карте объявлений.
    """

    permission_classes = (AllowAny,)
    serializer_class = MapInfoSerializer
    pagination_class = None
    url_kwargs = ("user_id",)

    @swagger_auto_schema(
        operation_summary='Список всех объектов вида "id, широта, долгота" для заданного пользователя.',
        operation_description='Возвращает список всех объектов вида "id, широта, долгота" кроме созданных самим пользователем.',
        manual_parameters=[
            Parameter(
                url_kwargs[0],
                IN_PATH,
                type=TYPE_INTEGER,
                description="Уникальный идентификатор пользователя.",
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        return super(FeedMapInfoListAPIView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return Announcement.objects.exclude(user_id=self.kwargs.get(self.url_kwargs[0]))
