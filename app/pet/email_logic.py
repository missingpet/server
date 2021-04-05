from django.core.mail import EmailMessage


def send_email_message(subject, body, to):
    """Функция для отправки писем"""
    email_message = EmailMessage(
        subject=subject,
        body=body,
        to=to,
    )
    email_message.send()
