from django.db.models.signals import post_save
from django.dispatch import receiver
from app.accounts.models import User
from .models import ClientProfile


@receiver(post_save, sender=User)
def create_client_profile(sender, instance, created, **kwargs):
    """
    Auto-create ClientProfile when a User with role='CLIENT' is created
    """
    if created and instance.role == "CLIENT":
        ClientProfile.objects.get_or_create(
            user=instance,
            defaults={'phone': instance.phone}
        )
