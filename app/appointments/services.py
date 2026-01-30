from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings

from .models import Appointment
from .serializers import (
    AppointmentCreateSerializer,
    AppointmentUpdateSerializer
)

# -----------------------------
# Dummy SMS function
# -----------------------------
def send_sms(phone, message):
    if phone:
        print(f"SMS to {phone}: {message}")


# -----------------------------
# Create Appointment
# -----------------------------
def create_appointment(request):
    serializer = AppointmentCreateSerializer(
        data=request.data,
        context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    appointment = serializer.save()

    client_user = appointment.client.user
    advocate_user = appointment.advocate.user

    send_mail(
        "New Appointment Booked ✅",
        f"Appointment with {advocate_user.username} on "
        f"{appointment.appointment_date} at {appointment.appointment_time}",
        settings.DEFAULT_FROM_EMAIL,
        [client_user.email, advocate_user.email]
    )

    send_sms(client_user.phone, "Appointment booked successfully ✅")
    send_sms(advocate_user.phone, "New appointment received ✅")

    return appointment


# -----------------------------
# List Client Appointments
# -----------------------------
def list_client_appointments(user):
    client = user.client_profile
    return Appointment.objects.filter(client=client)


# -----------------------------
# Update Appointment Status
# -----------------------------
def update_appointment_status(user, pk, status_value):
    allowed_status = ['APPROVED', 'REJECTED', 'COMPLETED']
    if status_value not in allowed_status:
        raise ValueError("Invalid status")

    appointment = get_object_or_404(
        Appointment,
        pk=pk,
        advocate__user=user
    )

    appointment.status = status_value
    appointment.save()

    client_user = appointment.client.user

    send_mail(
        "Appointment Status Updated ✅",
        f"Your appointment status is now {status_value}",
        settings.DEFAULT_FROM_EMAIL,
        [client_user.email]
    )

    send_sms(client_user.phone, f"Appointment status updated to {status_value}")

    return appointment


# -----------------------------
# Cancel Appointment
# -----------------------------
def cancel_appointment(user, pk):
    appointment = get_object_or_404(
        Appointment,
        pk=pk,
        client=user.client_profile
    )

    if appointment.status in ['CANCELLED', 'COMPLETED']:
        raise ValueError("Cannot cancel this appointment")

    appointment.status = 'CANCELLED'
    appointment.save()

    client_user = appointment.client.user
    advocate_user = appointment.advocate.user

    send_mail(
        "Appointment Cancelled ✅",
        f"Your appointment with {advocate_user.username} was cancelled",
        settings.DEFAULT_FROM_EMAIL,
        [client_user.email, advocate_user.email]
    )

    send_sms(client_user.phone, "Appointment cancelled ✅")
    send_sms(advocate_user.phone, "Appointment cancelled by client ❌")

    return appointment


# -----------------------------
# Update Appointment (Reschedule)
# -----------------------------
def update_appointment(appointment, data):
    serializer = AppointmentUpdateSerializer(
        appointment,
        data=data,
        partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    client_user = appointment.client.user
    advocate_user = appointment.advocate.user

    reschedule_date = serializer.validated_data.get('reschedule_date')
    reschedule_time = serializer.validated_data.get('reschedule_time')

    msg = "Your appointment details have been updated"
    if reschedule_date and reschedule_time:
        msg += f" to {reschedule_date} at {reschedule_time}"

    send_mail(
        "Appointment Updated ✅",
        msg,
        settings.DEFAULT_FROM_EMAIL,
        [client_user.email, advocate_user.email]
    )

    send_sms(client_user.phone, msg)
    send_sms(advocate_user.phone, msg)

    return appointment
