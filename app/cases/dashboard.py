# cases/dashboard.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone
from django.db.models import Count, Q

from .models import Case


class CaseDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # =================================================
        # ADVOCATE CASES DASHBOARD
        # =================================================
        if user.role == "ADVOCATE":
            if not hasattr(user, "advocate_profile"):
                return Response(
                    {"error": "Advocate profile not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            advocate = user.advocate_profile
            cases = Case.objects.filter(advocate=advocate)
            today = timezone.now().date()

            stats = {
                "total_cases": cases.count(),
                "open": cases.filter(status=Case.STATUS_OPEN).count(),
                "in_progress": cases.filter(status=Case.STATUS_IN_PROGRESS).count(),
                "closed": cases.filter(status=Case.STATUS_CLOSED).count(),
                "active_cases": cases.filter(
                    Q(status=Case.STATUS_OPEN) | Q(status=Case.STATUS_IN_PROGRESS)
                ).count(),
            }

            # Upcoming hearings
            upcoming_hearings = cases.filter(
                hearing_date__gte=today,
                status__in=[Case.STATUS_OPEN, Case.STATUS_IN_PROGRESS]
            ).order_by('hearing_date')[:5]

            hearing_data = [
                {
                    "id": case.id,
                    "case_number": case.case_number if hasattr(case, 'case_number') else "N/A",
                    "hearing_date": case.hearing_date if hasattr(case, 'hearing_date') else None,
                    "status": case.status,
                }
                for case in upcoming_hearings
            ]

            return Response({
                "role": "ADVOCATE",
                "stats": stats,
                "upcoming_hearings": hearing_data
            }, status=status.HTTP_200_OK)

        # =================================================
        # CLIENT CASES DASHBOARD
        # =================================================
        elif user.role == "CLIENT":
            if not hasattr(user, "client_profile"):
                return Response(
                    {"error": "Client profile not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            client = user.client_profile
            cases = Case.objects.filter(client=client)
            today = timezone.now().date()

            stats = {
                "total_cases": cases.count(),
                "open": cases.filter(status=Case.STATUS_OPEN).count(),
                "in_progress": cases.filter(status=Case.STATUS_IN_PROGRESS).count(),
                "closed": cases.filter(status=Case.STATUS_CLOSED).count(),
                "active_cases": cases.filter(
                    Q(status=Case.STATUS_OPEN) | Q(status=Case.STATUS_IN_PROGRESS)
                ).count(),
            }

            # Upcoming hearings
            upcoming_hearings = cases.filter(
                hearing_date__gte=today,
                status__in=[Case.STATUS_OPEN, Case.STATUS_IN_PROGRESS]
            ).order_by('hearing_date')[:5]

            hearing_data = [
                {
                    "id": case.id,
                    "case_number": case.case_number if hasattr(case, 'case_number') else "N/A",
                    "advocate": case.advocate.user.first_name,
                    "hearing_date": case.hearing_date if hasattr(case, 'hearing_date') else None,
                    "status": case.status,
                }
                for case in upcoming_hearings
            ]

            return Response({
                "role": "CLIENT",
                "stats": stats,
                "upcoming_hearings": hearing_data
            }, status=status.HTTP_200_OK)

        # =================================================
        # ADMIN CASES DASHBOARD
        # =================================================
        elif user.role == "ADMIN":
            cases = Case.objects.all()

            stats = {
                "total_cases": cases.count(),
                "open": cases.filter(status=Case.STATUS_OPEN).count(),
                "in_progress": cases.filter(status=Case.STATUS_IN_PROGRESS).count(),
                "closed": cases.filter(status=Case.STATUS_CLOSED).count(),
                "advocates_count": cases.values('advocate').distinct().count(),
                "clients_count": cases.values('client').distinct().count(),
            }

            return Response({
                "role": "ADMIN",
                "stats": stats
            }, status=status.HTTP_200_OK)

        return Response(
            {"error": "Role not recognized"},
            status=status.HTTP_400_BAD_REQUEST
        )
