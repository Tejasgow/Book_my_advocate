from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings

from app.appointments.models import Appointment
from app.cases.models import Case, CaseHearing, CaseDocument
from .models import ClientProfile
from app.appointments.serializers import AppointmentSerializer
from app.cases.serializers import CaseSerializer, CaseHearingSerializer, CaseDocumentSerializer
from .serializers import (
    ClientProfileViewSerializer,
    ClientProfileSerializer,
)

# -----------------------------
# Dummy SMS function
# -----------------------------
def send_sms(phone, message):
    if phone:
        print(f"SMS to {phone}: {message}")
        # Integrate Twilio or any SMS API here


# -----------------------------
# Client Profile
# -----------------------------
class ClientProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = get_object_or_404(ClientProfile, user=request.user)
        serializer = ClientProfileSerializer(profile)
        return Response({"profile": serializer.data})


class ClientProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        profile = get_object_or_404(ClientProfile, user=request.user)
        serializer = ClientProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Profile updated ✅", "profile": serializer.data})


# -----------------------------
# Client Dashboard
# -----------------------------
class ClientDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        client = get_object_or_404(ClientProfile, user=request.user)
        appointments = Appointment.objects.filter(client=client)
        cases = Case.objects.filter(client=client)
        return Response({
            "appointments_count": appointments.count(),
            "cases_count": cases.count()
        })


# -----------------------------
# Client Appointments
# -----------------------------
class ClientAppointmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        client = get_object_or_404(ClientProfile, user=request.user)
        appointments = Appointment.objects.filter(client=client)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response({"appointments": serializer.data})


# -----------------------------
# Client Cases
# -----------------------------
class ClientCasesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        client = get_object_or_404(ClientProfile, user=request.user)
        cases = Case.objects.filter(client=client)
        serializer = CaseSerializer(cases, many=True)
        return Response({"cases": serializer.data})


class ClientCaseDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        client = get_object_or_404(ClientProfile, user=request.user)
        case = get_object_or_404(Case, pk=pk, client=client)
        serializer = CaseSerializer(case)
        return Response({"case": serializer.data})


# -----------------------------
# Client Case Hearings
# -----------------------------
class ClientCaseHearingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, case_id):
        client = get_object_or_404(ClientProfile, user=request.user)
        case = get_object_or_404(Case, id=case_id, client=client)
        hearings = case.hearings.all()
        serializer = CaseHearingSerializer(hearings, many=True)
        return Response({"hearings": serializer.data})


# -----------------------------
# Client Case Documents
# -----------------------------
class ClientCaseDocumentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, case_id):
        client = get_object_or_404(ClientProfile, user=request.user)
        case = get_object_or_404(Case, id=case_id, client=client)
        documents = case.documents.all()
        serializer = CaseDocumentSerializer(documents, many=True)
        return Response({"documents": serializer.data})
