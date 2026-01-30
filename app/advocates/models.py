from django.db import models
from django.conf import settings


# =================================================
# ADVOCATE PROFILE
# =================================================

class AdvocateProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='advocate_profile'
    )

    # -----------------------------
    # Specialization
    # -----------------------------
    SPECIALIZATION_CHOICES = (
        ('CRIMINAL', 'Criminal Law'),
        ('CIVIL', 'Civil Law'),
        ('CORPORATE', 'Corporate Law'),
        ('FAMILY', 'Family Law'),
        ('CONSTITUTIONAL', 'Constitutional Law'),
        ('OTHER', 'Other'),
    )

    specialization = models.CharField(
        max_length=50,
        choices=SPECIALIZATION_CHOICES,
        default='OTHER'
    )

    # -----------------------------
    # Professional Details
    # -----------------------------
    experience_years = models.PositiveIntegerField(
        default=0,
        help_text="Total years of legal experience"
    )

    bar_council_id = models.CharField(
        max_length=100,
        unique=True,
        help_text="Official Bar Council Registration Number"
    )

    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    verified = models.BooleanField(
        default=False,
        help_text="Verified by Admin"
    )

    # -----------------------------
    # Timestamps
    # -----------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # -----------------------------
    # Meta
    # -----------------------------
    class Meta:
        verbose_name = "Advocate Profile"
        verbose_name_plural = "Advocate Profiles"
        ordering = ['-verified', '-experience_years', 'user__username']

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.get_specialization_display()}"


# =================================================
# ASSISTANT LAWYER
# =================================================

class AssistantLawyer(models.Model):
    advocate = models.ForeignKey(
        AdvocateProfile,
        on_delete=models.CASCADE,
        related_name='assistants'
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assistant_profile'
    )

    assigned_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Assistant Lawyer"
        verbose_name_plural = "Assistant Lawyers"
        ordering = ['-assigned_at']
        unique_together = ('advocate', 'user')

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} (Assistant of {self.advocate.user.username})"
