from django.core.mail import EmailMessage


def sendemailmessage(subject, body, to):
    email_message = EmailMessage(subject=subject, body=body, to=to)
    email_message.send()
