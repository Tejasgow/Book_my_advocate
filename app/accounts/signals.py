from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import User
from app.notifications.models import Notification


@receiver(post_save, sender=User)
def user_created_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance,
            title="Welcome to Book My Advocate 🎉",
            message="Your account has been created successfully. You can now book appointments and chat with advocates.",
            notification_type="SYSTEM"
        )
