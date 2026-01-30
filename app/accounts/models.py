from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import random
from django.contrib.auth.hashers import make_password, check_password


# =================================================
# USER MODEL
# =================================================

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    Supports Client, Advocate, and Admin roles
    """

    ROLE_CHOICES = (
        ('CLIENT', 'Client'),
        ('ADVOCATE', 'Advocate'),
        ('ADMIN', 'Admin'),
    )

    # ---------- Personal Information ----------
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, unique=True, blank=True)
    address = models.TextField(blank=True)

    # ---------- Role Management ----------
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CLIENT')

    # ---------- Helper Methods ----------
    def is_client(self):
        return self.role == 'CLIENT'

    def is_advocate(self):
        return self.role == 'ADVOCATE'

    def is_admin(self):
        return self.role == 'ADMIN'

    def __str__(self):
        return f"{self.username} ({self.role})"


# =================================================
# PASSWORD RESET OTP MODEL
# =================================================

class PasswordResetOTP(models.Model):
    """
    Stores hashed OTP for secure password reset
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='password_otps'
    )
    otp = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    OTP_EXPIRY_MINUTES = 10

    # ---------- OTP Logic ----------
    def is_expired(self):
        """
        Check if OTP has expired
        """
        return timezone.now() > self.created_at + timedelta(
            minutes=self.OTP_EXPIRY_MINUTES
        )

    def set_otp(self):
        """
        Generate and hash OTP
        """
        raw_otp = str(random.randint(100000, 999999))
        self.otp = make_password(raw_otp)
        return raw_otp

    def verify_otp(self, raw_otp):
        """
        Verify raw OTP with hashed OTP
        """
        return check_password(raw_otp, self.otp)

    def save(self, *args, **kwargs):
        """
        Auto-generate OTP on save if not present
        """
        if not self.otp:
            self.set_otp()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"PasswordResetOTP(user={self.user.username}, used={self.is_used})"

    class Meta:
        ordering = ['-created_at']
