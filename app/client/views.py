from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import ClientProfile
from .serializers import (
    ClientProfileViewSerializer,
    ClientProfileSerializer,
    ClientAppointmentSerializer,
    ClientCaseSerializer,
    ClientCaseHearingSerializer,
    ClientCaseDocumentSerializer,
)

from app.appointments.models import Appointment
from app.cases.models import Case


# =================================================
# Client Profile
# =================================================
class ClientProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = get_object_or_404(ClientProfile, user=request.user)
        serializer = ClientProfileViewSerializer(profile)
        return Response({"profile": serializer.data})


class ClientProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        profile = get_object_or_404(ClientProfile, user=request.user)
        serializer = ClientProfileSerializer(
            profile,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "Profile updated ✅",
            "profile": serializer.data
        })


# =================================================
# Client Appointments
# =================================================
class ClientAppointmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        client = get_object_or_404(ClientProfile, user=request.user)
        appointments = Appointment.objects.filter(client=client)
        serializer = ClientAppointmentSerializer(appointments, many=True)
        return Response({"appointments": serializer.data})


# =================================================
# Client Cases
# =================================================
class ClientCasesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        client = get_object_or_404(ClientProfile, user=request.user)
        cases = Case.objects.filter(client=client)
        serializer = ClientCaseSerializer(cases, many=True)
        return Response({"cases": serializer.data})


class ClientCaseDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        client = get_object_or_404(ClientProfile, user=request.user)
        case = get_object_or_404(Case, pk=pk, client=client)
        serializer = ClientCaseSerializer(case)
        return Response({"case": serializer.data})


# =================================================
# Client Case Hearings
# =================================================
class ClientCaseHearingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, case_id):
        client = get_object_or_404(ClientProfile, user=request.user)
        case = get_object_or_404(Case, id=case_id, client=client)
        serializer = ClientCaseHearingSerializer(
            case.hearings.all(),
            many=True
        )
        return Response({"hearings": serializer.data})


# =================================================
# Client Case Documents
# =================================================
class ClientCaseDocumentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, case_id):
        client = get_object_or_404(ClientProfile, user=request.user)
        case = get_object_or_404(Case, id=case_id, client=client)
        serializer = ClientCaseDocumentSerializer(
            case.documents.all(),
            many=True
        )
        return Response({"documents": serializer.data})
