from .models import Notification
from django.core.mail import send_mail
from django.conf import settings

def send_notification(user, title, message, type, send_email=False):
    """
    Create a notification and optionally send email.
    """
    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message,
        type=type
    )

    if send_email and user.email:
        send_mail(
            subject=title,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

    return notification
