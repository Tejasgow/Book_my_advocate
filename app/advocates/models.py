from django.db import models
from django.conf import settings

class AdvocateProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='advocate_profile'
    )

    specialization_choices = (
        ('CRIMINAL', 'Criminal'),
        ('CIVIL', 'Civil'),
        ('CORPORATE', 'Corporate'),
        ('FAMILY', 'Family'),
        ('CONSTITUTIONAL', 'Constitutional'),
        ('OTHER', 'Other'),
    )
    specialization = models.CharField(max_length=50, choices=specialization_choices, default='OTHER')
    experience_years = models.PositiveIntegerField(default=0)
    bar_council_id = models.CharField(max_length=100, unique=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    verified = models.BooleanField(default=False)  # Admin verifies the advocate
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_specialization_display()}"
