from django.core.mail import EmailMessage


class EmailMessageException(Exception):
    pass


def send_email_message(subject: str, body: str, recipient: str) -> None:
    """Функция для отправки писем"""
    email_message = EmailMessage(
        subject=subject,
        body=body,
        to=(recipient,),
    )
    email_message.send()
