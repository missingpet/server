"""
Module which contains functions and classes to work with email messages.
"""
from django.core.mail import EmailMessage


def send_message(subject: str, body: str, recipient: str) -> None:
    """Функция для отправки писем"""
    email_message = EmailMessage(
        subject=subject,
        body=body,
        to=(recipient, ),
    )
    email_message.send()