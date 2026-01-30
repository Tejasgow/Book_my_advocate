from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta

from app.advocates.models import AdvocateProfile
from app.client.models import ClientProfile


class Appointment(models.Model):
    """
    Appointment model representing booking between a Client and Advocate.
    """

    # =============================
    # STATUS CHOICES
    # =============================
    STATUS_PENDING = 'PENDING'
    STATUS_APPROVED = 'APPROVED'
    STATUS_REJECTED = 'REJECTED'
    STATUS_COMPLETED = 'COMPLETED'
    STATUS_CANCELLED = 'CANCELLED'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELLED, 'Cancelled'),
    )

    # =============================
    # RELATIONSHIPS
    # =============================
    client = models.ForeignKey(
        ClientProfile,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    advocate = models.ForeignKey(
        AdvocateProfile,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    # =============================
    # APPOINTMENT DETAILS
    # =============================
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField(default=30)

    problem_description = models.TextField()
    remarks = models.TextField(blank=True, null=True)
    cancellation_reason = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )

    # =============================
    # SYSTEM FIELDS
    # =============================
    is_active = models.BooleanField(default=True)  # soft delete
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # =============================
    # META
    # =============================
    class Meta:
        ordering = ['-appointment_date', '-appointment_time']
        unique_together = ('advocate', 'appointment_date', 'appointment_time')
        indexes = [
            models.Index(fields=['advocate', 'appointment_date']),
            models.Index(fields=['client']),
            models.Index(fields=['status']),
        ]

    # =============================
    # STRING REPRESENTATION
    # =============================
    def __str__(self):
        return f"{self.client.user.username} → {self.advocate.user.username} ({self.status})"

    # =============================
    # HELPER METHODS
    # =============================
    @property
    def start_datetime(self):
        return datetime.combine(self.appointment_date, self.appointment_time)

    @property
    def end_time(self):
        return (self.start_datetime + timedelta(minutes=self.duration_minutes)).time()

    def is_past_due(self):
        return timezone.now() > timezone.make_aware(self.start_datetime)

    def can_be_cancelled(self):
        return self.status in [self.STATUS_PENDING, self.STATUS_APPROVED]
