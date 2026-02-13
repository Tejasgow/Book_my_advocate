# accounts/dashboard.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone
from django.db.models import Count

from .models import User
from app.appointments.models import Appointment


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # =================================================
        # ADMIN DASHBOARD
        # =================================================
        if user.role == "ADMIN":

            stats = {
                "total_users": User.objects.count(),
                "total_clients": User.objects.filter(role="CLIENT").count(),
                "total_advocates": User.objects.filter(role="ADVOCATE").count(),

                "total_appointments": Appointment.objects.count(),
                "pending": Appointment.objects.filter(status="PENDING").count(),
                "approved": Appointment.objects.filter(status="APPROVED").count(),
                "completed": Appointment.objects.filter(status="COMPLETED").count(),
                "cancelled": Appointment.objects.filter(status="CANCELLED").count(),
            }

            return Response({
                "role": "ADMIN",
                "stats": stats
            }, status=status.HTTP_200_OK)

        # =================================================
        # ADVOCATE DASHBOARD
        # =================================================
        elif user.role == "ADVOCATE":

            if not hasattr(user, "advocate_profile"):
                return Response(
                    {"error": "Advocate profile not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            appointments = Appointment.objects.filter(
                advocate=user.advocate_profile
            )

            stats = {
                "total_appointments": appointments.count(),
                "pending": appointments.filter(status="PENDING").count(),
                "approved": appointments.filter(status="APPROVED").count(),
                "completed": appointments.filter(status="COMPLETED").count(),
                "cancelled": appointments.filter(status="CANCELLED").count(),
                "today": appointments.filter(
                    appointment_date=timezone.now().date()
                ).count(),
                "upcoming": appointments.filter(
                    appointment_date__gt=timezone.now().date()
                ).count(),
            }

            return Response({
                "role": "ADVOCATE",
                "stats": stats
            }, status=status.HTTP_200_OK)

        # =================================================
        # CLIENT DASHBOARD
        # =================================================
        elif user.role == "CLIENT":

            if not hasattr(user, "client_profile"):
                return Response(
                    {"error": "Client profile not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            appointments = Appointment.objects.filter(
                client=user.client_profile
            )

            stats = {
                "total_appointments": appointments.count(),
                "pending": appointments.filter(status="PENDING").count(),
                "approved": appointments.filter(status="APPROVED").count(),
                "completed": appointments.filter(status="COMPLETED").count(),
                "cancelled": appointments.filter(status="CANCELLED").count(),
                "upcoming": appointments.filter(
                    appointment_date__gte=timezone.now().date()
                ).count(),
                "past": appointments.filter(
                    appointment_date__lt=timezone.now().date()
                ).count(),
            }

            return Response({
                "role": "CLIENT",
                "stats": stats
            }, status=status.HTTP_200_OK)

        return Response(
            {"error": "Invalid role"},
            status=status.HTTP_400_BAD_REQUEST
        )
