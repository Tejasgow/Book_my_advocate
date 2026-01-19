from django.db import models
from app.accounts.models import User
from app.advocates.models import AdvocateProfile
from app.appointments.models import Appointment


class Case(models.Model):

    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('CLOSED', 'Closed'),
    ]

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name='case'
    )

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cases'
    )

    advocate = models.ForeignKey(
        AdvocateProfile,
        on_delete=models.CASCADE,
        related_name='cases'
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='OPEN'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# -------------------------------------------------
# Case Hearings
# -------------------------------------------------
class CaseHearing(models.Model):
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


# -------------------------------------------------
# Case Documents
# -------------------------------------------------
class CaseDocument(models.Model):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.FileField(upload_to='case_documents/')
    description = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
