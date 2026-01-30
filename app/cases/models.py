from django.db import models
from app.client.models import ClientProfile
from app.advocates.models import AdvocateProfile
from app.appointments.models import Appointment


# =================================================
# CASE MODEL
# =================================================
class Case(models.Model):
    """
    Legal Case created after an appointment
    """

    # -----------------------------
    # Status Choices
    # -----------------------------
    STATUS_OPEN = 'OPEN'
    STATUS_IN_PROGRESS = 'IN_PROGRESS'
    STATUS_CLOSED = 'CLOSED'

    STATUS_CHOICES = [
        (STATUS_OPEN, 'Open'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_CLOSED, 'Closed'),
    ]

    # -----------------------------
    # Relations
    # -----------------------------
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name='case'
    )

    client = models.ForeignKey(
        ClientProfile,
        on_delete=models.CASCADE,
        related_name='cases'
    )

    advocate = models.ForeignKey(
        AdvocateProfile,
        on_delete=models.CASCADE,
        related_name='cases'
    )

    # -----------------------------
    # Case Details
    # -----------------------------
    title = models.CharField(max_length=255)
    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN
    )

    is_active = models.BooleanField(default=True)  # soft delete support

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # -----------------------------
    # Meta
    # -----------------------------
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    # -----------------------------
    # String Representation
    # -----------------------------
    def __str__(self):
        return f"Case #{self.id} - {self.title} ({self.client.user.username})"


# =================================================
# CASE HEARING MODEL
# =================================================
class CaseHearing(models.Model):
    """
    Court hearings for a case
    """

    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='hearings'
    )

    hearing_date = models.DateField()
    hearing_time = models.TimeField()
    court_name = models.CharField(max_length=255)

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # -----------------------------
    # Meta
    # -----------------------------
    class Meta:
        ordering = ['-hearing_date', '-hearing_time']

    # -----------------------------
    # String Representation
    # -----------------------------
    def __str__(self):
        return f"{self.case.title} - {self.hearing_date} @ {self.court_name}"


# =================================================
# CASE DOCUMENT MODEL
# =================================================
class CaseDocument(models.Model):
    """
    Documents uploaded for a case
    """

    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='documents'
    )

    uploaded_by = models.ForeignKey(
        ClientProfile,
        on_delete=models.CASCADE,
        related_name='uploaded_documents'
    )

    document = models.FileField(upload_to='case_documents/')
    description = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # -----------------------------
    # Meta
    # -----------------------------
    class Meta:
        ordering = ['-created_at']

    # -----------------------------
    # String Representation
    # -----------------------------
    def __str__(self):
        return f"Document for {self.case.title}"
