# appointments/dashboard.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone
from django.db.models import Count, Q

from .models import Appointment
from app.advocates.models import AdvocateProfile
from app.client.models import ClientProfile


class AppointmentDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # =================================================
        # ADVOCATE APPOINTMENTS DASHBOARD
        # =================================================
        if user.role == "ADVOCATE":
            if not hasattr(user, "advocate_profile"):
                return Response(
                    {"error": "Advocate profile not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            advocate = user.advocate_profile
            appointments = Appointment.objects.filter(advocate=advocate)
            today = timezone.now().date()

            stats = {
                "total_appointments": appointments.count(),
                "pending": appointments.filter(status=Appointment.STATUS_PENDING).count(),
                "approved": appointments.filter(status=Appointment.STATUS_APPROVED).count(),
                "rejected": appointments.filter(status=Appointment.STATUS_REJECTED).count(),
                "completed": appointments.filter(status=Appointment.STATUS_COMPLETED).count(),
                "cancelled": appointments.filter(status=Appointment.STATUS_CANCELLED).count(),
                "today": appointments.filter(appointment_date=today).count(),
                "upcoming": appointments.filter(appointment_date__gt=today).count(),
                "past": appointments.filter(appointment_date__lt=today).count(),
            }

            recent_appointments = appointments.order_by('-appointment_date')[:5]
            recent_data = [
                {
                    "id": apt.id,
                    "client": apt.client.user.first_name,
                    "date": apt.appointment_date,
                    "time": str(apt.appointment_time),
                    "status": apt.status,
                    "mode": apt.appointment_mode if hasattr(apt, 'appointment_mode') else "N/A"
                }
                for apt in recent_appointments
            ]

            return Response({
                "role": "ADVOCATE",
                "stats": stats,
                "recent_appointments": recent_data
            }, status=status.HTTP_200_OK)

        # =================================================
        # CLIENT APPOINTMENTS DASHBOARD
        # =================================================
        elif user.role == "CLIENT":
            if not hasattr(user, "client_profile"):
                return Response(
                    {"error": "Client profile not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            client = user.client_profile
            appointments = Appointment.objects.filter(client=client)
            today = timezone.now().date()

            stats = {
                "total_appointments": appointments.count(),
                "pending": appointments.filter(status=Appointment.STATUS_PENDING).count(),
                "approved": appointments.filter(status=Appointment.STATUS_APPROVED).count(),
                "rejected": appointments.filter(status=Appointment.STATUS_REJECTED).count(),
                "completed": appointments.filter(status=Appointment.STATUS_COMPLETED).count(),
                "cancelled": appointments.filter(status=Appointment.STATUS_CANCELLED).count(),
                "upcoming": appointments.filter(appointment_date__gte=today).count(),
                "past": appointments.filter(appointment_date__lt=today).count(),
            }

            recent_appointments = appointments.order_by('-appointment_date')[:5]
            recent_data = [
                {
                    "id": apt.id,
                    "advocate": apt.advocate.user.first_name,
                    "date": apt.appointment_date,
                    "time": str(apt.appointment_time),
                    "status": apt.status,
                }
                for apt in recent_appointments
            ]

            return Response({
                "role": "CLIENT",
                "stats": stats,
                "recent_appointments": recent_data
            }, status=status.HTTP_200_OK)

        # =================================================
        # ADMIN APPOINTMENTS DASHBOARD
        # =================================================
        elif user.role == "ADMIN":
            appointments = Appointment.objects.all()
            today = timezone.now().date()

            stats = {
                "total_appointments": appointments.count(),
                "pending": appointments.filter(status=Appointment.STATUS_PENDING).count(),
                "approved": appointments.filter(status=Appointment.STATUS_APPROVED).count(),
                "rejected": appointments.filter(status=Appointment.STATUS_REJECTED).count(),
                "completed": appointments.filter(status=Appointment.STATUS_COMPLETED).count(),
                "cancelled": appointments.filter(status=Appointment.STATUS_CANCELLED).count(),
                "today": appointments.filter(appointment_date=today).count(),
            }

            return Response({
                "role": "ADMIN",
                "stats": stats
            }, status=status.HTTP_200_OK)

        return Response(
            {"error": "Role not recognized"},
            status=status.HTTP_400_BAD_REQUEST
        )
