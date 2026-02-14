# client/dashboard.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone
from django.db.models import Count, Q, Sum

from .models import ClientProfile
from app.appointments.models import Appointment
from app.cases.models import Case
from app.payments.models import Payment


class ClientDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # =================================================
        # CLIENT PROFILE DASHBOARD
        # =================================================
        if user.role == "CLIENT":
            if not hasattr(user, "client_profile"):
                return Response(
                    {"error": "Client profile not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            client = user.client_profile
            today = timezone.now().date()

            # Appointments stats
            appointments = Appointment.objects.filter(client=client)
            
            # Cases stats
            cases = Case.objects.filter(client=client)
            
            # Payments stats
            payments = Payment.objects.filter(client=client)

            stats = {
                "profile": {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "phone": client.phone,
                    "city": client.city,
                    "is_verified": client.is_verified,
                    "joined_on": client.created_at,
                },
                "appointments": {
                    "total": appointments.count(),
                    "pending": appointments.filter(status=Appointment.STATUS_PENDING).count(),
                    "approved": appointments.filter(status=Appointment.STATUS_APPROVED).count(),
                    "completed": appointments.filter(status=Appointment.STATUS_COMPLETED).count(),
                    "cancelled": appointments.filter(status=Appointment.STATUS_CANCELLED).count(),
                    "upcoming": appointments.filter(appointment_date__gte=today).count(),
                },
                "cases": {
                    "total": cases.count(),
                    "open": cases.filter(status=Case.STATUS_OPEN).count(),
                    "in_progress": cases.filter(status=Case.STATUS_IN_PROGRESS).count(),
                    "closed": cases.filter(status=Case.STATUS_CLOSED).count(),
                },
                "payments": {
                    "total_paid": payments.filter(status='SUCCESS').aggregate(
                        total=Sum('amount')
                    )['total'] or 0,
                    "total_transactions": payments.count(),
                    "successful": payments.filter(status='SUCCESS').count(),
                    "failed": payments.filter(status='FAILED').count(),
                    "pending": payments.filter(status='CREATED').count(),
                },
                "advocates_connected": appointments.values('advocate').distinct().count(),
            }

            return Response({
                "role": "CLIENT",
                "dashboard": stats
            }, status=status.HTTP_200_OK)

        # =================================================
        # ADMIN CLIENT DASHBOARD
        # =================================================
        elif user.role == "ADMIN":
            clients = ClientProfile.objects.all()
            all_appointments = Appointment.objects.all()
            all_cases = Case.objects.all()
            all_payments = Payment.objects.all()

            stats = {
                "total_clients": clients.count(),
                "verified_clients": clients.filter(is_verified=True).count(),
                "unverified_clients": clients.filter(is_verified=False).count(),
                "total_appointments": all_appointments.count(),
                "total_cases": all_cases.count(),
                "total_payments_collected": all_payments.filter(
                    status='SUCCESS'
                ).aggregate(total=Sum('amount'))['total'] or 0,
                "total_payment_transactions": all_payments.count(),
            }

            return Response({
                "role": "ADMIN",
                "stats": stats
            }, status=status.HTTP_200_OK)

        return Response(
            {"error": "Role not recognized"},
            status=status.HTTP_400_BAD_REQUEST
        )
