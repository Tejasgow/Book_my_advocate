from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Appointment
from .serializers import AppointmentSerializer
from .permissions import IsAdvocateUser, IsClientUser, IsOwnerOrAdvocate
from . import services


# -----------------------------
# Create Appointment
# -----------------------------
class AppointmentCreateView(APIView):
    permission_classes = [IsAuthenticated, IsClientUser]

    def post(self, request):
        appointment = services.create_appointment(request)
        return Response(
            {
                "message": "Appointment booked successfully ✅",
                "data": AppointmentSerializer(appointment).data
            },
            status=status.HTTP_201_CREATED
        )


# -----------------------------
# Client Appointment List
# -----------------------------
class ClientAppointmentListView(APIView):
    permission_classes = [IsAuthenticated, IsClientUser]

    def get(self, request):
        appointments = services.list_client_appointments(request.user)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response({"message": "Appointments fetched ✅", "data": serializer.data})


# -----------------------------
# Advocate Status Update
# -----------------------------
class AppointmentStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdvocateUser]

    def patch(self, request, pk):
        try:
            appointment = services.update_appointment_status(
                request.user,
                pk,
                request.data.get('status')
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        return Response(
            {
                "message": "Status updated ✅",
                "data": AppointmentSerializer(appointment).data
            }
        )


# -----------------------------
# Cancel Appointment
# -----------------------------
class AppointmentCancelView(APIView):
    permission_classes = [IsAuthenticated, IsClientUser]

    def post(self, request, pk):
        try:
            appointment = services.cancel_appointment(request.user, pk)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        return Response(
            {
                "message": "Appointment cancelled ✅",
                "data": AppointmentSerializer(appointment).data
            }
        )


# -----------------------------
# Appointment Detail
# -----------------------------
class AppointmentDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdvocate]

    def get(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        self.check_object_permissions(request, appointment)
        return Response(
            {
                "message": "Appointment fetched ✅",
                "data": AppointmentSerializer(appointment).data
            }
        )


# -----------------------------
# Update Appointment
# -----------------------------
class AppointmentUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdvocate]

    def put(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        self.check_object_permissions(request, appointment)

        appointment = services.update_appointment(appointment, request.data)

        return Response(
            {
                "message": "Appointment updated ✅",
                "data": AppointmentSerializer(appointment).data
            }
        )
