from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdvocate
from app.advocates.models import AdvocateProfile


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

        # Assistant Count
        total_assistants = advocate.assistants.count()

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
                "assistant_stats": {
                    "total_assistants": total_assistants
                },
                "profile_completion_percentage": profile_completion,
            },
            status=status.HTTP_200_OK,
        )
