from django.db import models
from app.accounts.models import User
from app.advocates.models import AdvocateProfile
from app.appointments.models import Appointment

class Review(models.Model):
    """
    Reviews written by clients for advocates
    """
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        limit_choices_to={'role': 'CLIENT'}
    )
    advocate = models.ForeignKey(
        AdvocateProfile,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviews'
    )

    rating = models.PositiveSmallIntegerField(default=5)  # 1-5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('client', 'advocate', 'appointment')  # one review per appointment

    def __str__(self):
        return f"{self.client.username} → {self.advocate.user.username} ({self.rating}⭐)"
