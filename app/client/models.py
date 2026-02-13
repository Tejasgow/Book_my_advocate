from django.db import models
from app.accounts.models import User


class ClientProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='client_profile'
    )

    phone = models.CharField(max_length=15,blank=True,null=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
