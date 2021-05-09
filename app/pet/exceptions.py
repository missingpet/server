from functools import wraps
from smtplib import SMTPException

from ratelimit.exceptions import Ratelimited
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST


def catch_smtp_exception_for_view(func):
    """
    Декоратор для отлавливания ошибок при обращению к smtp сервису.
    Оборачивает исключение в 400 ответ во view.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SMTPException as ex:
            message = {"smtp_error": str(ex)}
            return Response(status=HTTP_400_BAD_REQUEST, data=message)

    return wrapper


def catch_rate_limit_exceeded_exception_for_view(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Ratelimited:
            message = {
                "rate_limit_exceeded_error":
                "Превышен лимит запросов к серверу. Повторите попытку позднее."
            }
            return Response(status=HTTP_400_BAD_REQUEST, data=message)

    return wrapper
