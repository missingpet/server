from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from .email_logic import EmailMessageException


def catch_email_message_exception_for_views(func):
    """
    Декоратор для отлавливания ошибок при обращения к почтовому сервису.
    Оборачивает исключение в 400 ответ во view.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except EmailMessageException as ex:
            message = {'email_send_error': str(ex)}
            return Response(status=HTTP_400_BAD_REQUEST, data=message)

    return wrapper