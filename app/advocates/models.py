from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError


# =================================================
# ADVOCATE PROFILE
# =================================================
class AdvocateProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="advocate_profile"
    )

    # -----------------------------------
    # Personal / Contact Info
    # -----------------------------------
    phone = models.CharField(max_length=15, null=True, blank=True)

    profile_photo = models.ImageField(
        upload_to="advocates/photos/",
        null=True,
        blank=True
    )

    bio = models.TextField(blank=True)

    languages_spoken = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated languages (Eg: English, Hindi, Telugu)"
    )

    # -----------------------------------
    # Official Verification
    # -----------------------------------
    official_id_card = models.FileField(
        upload_to="advocate_ids/",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(
            allowed_extensions=["pdf", "jpg", "jpeg", "png"]
        )],
        help_text="Upload Bar Council ID / Official Advocate ID"
    )

    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)

    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="verified_advocates"
    )

    # -----------------------------------
    # Specialization
    # -----------------------------------
    SPECIALIZATION_CHOICES = (
        ("CRIMINAL", "Criminal Law"),
        ("CIVIL", "Civil Law"),
        ("CORPORATE", "Corporate Law"),
        ("FAMILY", "Family Law"),
        ("CONSTITUTIONAL", "Constitutional Law"),
        ("CYBER", "Cyber Law"),
        ("OTHER", "Other"),
    )

    specialization = models.CharField(
        max_length=50,
        choices=SPECIALIZATION_CHOICES,
        default="OTHER"
    )

    # -----------------------------------
    # Professional Details
    # -----------------------------------
    experience_years = models.PositiveIntegerField(default=0)

    bar_council_id = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )

    enrollment_year = models.PositiveIntegerField(null=True, blank=True)

    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    # -----------------------------------
    # Location / Practice
    # -----------------------------------
    court_type = models.CharField(
        max_length=50,
        blank=True,
        help_text="District Court / High Court / Supreme Court"
    )

    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)

    # -----------------------------------
    # Status & Metrics
    # -----------------------------------
    is_active = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    # -----------------------------------
    # Timestamps
    # -----------------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Advocate Profile"
        verbose_name_plural = "Advocate Profiles"
        ordering = ["-is_verified", "-experience_years", "user__username"]

    def __str__(self):
        return self.user.get_full_name() or self.user.username

# =================================================
# ASSISTANT LAWYER
# =================================================
class AssistantLawyer(models.Model):
    advocate = models.ForeignKey(AdvocateProfile,on_delete=models.CASCADE,related_name="assistants")

    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="assistant_profile")

    assigned_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Assistant Lawyer"
        verbose_name_plural = "Assistant Lawyers"
        unique_together = ("advocate", "user")
        ordering = ["-assigned_at"]

    def clean(self):
        if self.user.role != "ASSISTANT":
            raise ValidationError("User must have ASSISTANT role")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} (Assistant of {self.advocate.user.username})"
