from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdvocate
from app.advocates.models import AdvocateProfile
from app.cases.models import Case
from django.utils import timezone


# =================================================
# ADVOCATE PERSONAL DASHBOARD
# =================================================
class AdvocateDashboardView(APIView):
    """
    Personal Dashboard for Logged-in Advocate
    """
    permission_classes = [IsAuthenticated, IsAdvocate]

    def get(self, request):

        advocate = getattr(request.user, "advocate_profile", None)

        if not advocate:
            return Response(
                {"error": "Advocate profile not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # ================================
        # ASSISTANT COUNT
        # ================================
        total_assistants = advocate.assistants.count()

        # ================================
        # CASE STATISTICS
        # ================================
        cases = Case.objects.filter(advocate=advocate)

        total_cases = cases.count()
        open_cases = cases.filter(status="OPEN").count()
        in_progress_cases = cases.filter(status="IN_PROGRESS").count()
        closed_cases = cases.filter(status="CLOSED").count()

        # Upcoming Hearings (next 7 days)
        today = timezone.now().date()
        upcoming_hearings = cases.filter(
            hearing_date__gte=today
        ).order_by("hearing_date")[:5]

        # Client Count (distinct clients)

        total_clients = cases.values("client").distinct().count()

        # Profile Completion Logic
        fields_to_check = [
            advocate.bio,
            advocate.profile_photo,
            advocate.languages_spoken,
            advocate.official_id_card,
            advocate.bar_council_id,
            advocate.city,
            advocate.state,
            advocate.court_type,
        ]

        filled_fields = sum(1 for field in fields_to_check if field)
        profile_completion = int((filled_fields / len(fields_to_check)) * 100)

        return Response(
            {
                "dashboard": {
                    "username": request.user.username,
                    "specialization": advocate.specialization,
                    "experience_years": advocate.experience_years,
                    "consultation_fee": advocate.consultation_fee,
                    "rating": advocate.rating,
                    "verification_status": advocate.is_verified,
                    "active_status": advocate.is_active,
                    "bar_council_id": advocate.bar_council_id,
                    "enrollment_year": advocate.enrollment_year,
                    "court_type": advocate.court_type,
                    "city": advocate.city,
                    "state": advocate.state,
                    "joined_on": advocate.created_at,
                },
                "case_stats": {
                    "total_cases": total_cases,
                    "open_cases": open_cases,
                    "in_progress_cases": in_progress_cases,
                    "closed_cases": closed_cases,
                },
                "client_stats": {
                    "total_clients": total_clients
                },
                "assistant_stats": {
                    "total_assistants": total_assistants
                },
                "upcoming_hearings": [
                    {
                        "case_id": case.id,
                        "case_title": case.title,
                        "hearing_date": case.hearing_date,
                        "status": case.status,
                    }
                    for case in upcoming_hearings
                ],
                "profile_completion_percentage": profile_completion,
            },
            status=status.HTTP_200_OK,
        )
