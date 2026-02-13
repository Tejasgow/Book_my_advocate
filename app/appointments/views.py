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
# CREATE APPOINTMENT (CLIENT)
# -----------------------------
class AppointmentCreateView(APIView):
    permission_classes = [IsAuthenticated, IsClientUser]

    def post(self, request):
        try:
            appointment = services.create_appointment(request)
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "message": "Appointment booked successfully ✅",
                "data": AppointmentSerializer(appointment).data
            },
            status=status.HTTP_201_CREATED
        )


# -----------------------------
# CLIENT APPOINTMENT LIST
# -----------------------------
class ClientAppointmentListView(APIView):
    permission_classes = [IsAuthenticated, IsClientUser]

    def get(self, request):
        appointments = services.list_client_appointments(request.user)
        serializer = AppointmentSerializer(appointments, many=True)

        return Response({
            "message": "Appointments fetched successfully ✅",
            "data": serializer.data
        })


# -----------------------------
# ADVOCATE STATUS UPDATE
# -----------------------------
class AppointmentStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdvocateUser]

    def patch(self, request, pk):
        status_value = request.data.get("status")
        if not status_value:
            return Response(
                {"error": "status field is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            appointment = services.update_appointment_status(
                request.user,
                pk,
                status_value
            )
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            "message": "Appointment status updated successfully ✅",
            "data": AppointmentSerializer(appointment).data
        })


# -----------------------------
# CANCEL APPOINTMENT (CLIENT)
# -----------------------------
class AppointmentCancelView(APIView):
    permission_classes = [IsAuthenticated, IsClientUser]

    def patch(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)

        # 🔐 Ownership check
        if appointment.client.user != request.user:
            return Response(
                {"error": "You are not allowed to cancel this appointment."},
                status=status.HTTP_403_FORBIDDEN
            )

        # ❌ Prevent cancelling already cancelled
        if appointment.status == "CANCELLED":
            return Response(
                {"error": "Appointment is already cancelled."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ❌ Prevent cancelling completed appointment
        if appointment.status == "COMPLETED":
            return Response(
                {"error": "Completed appointment cannot be cancelled."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ Update status
        appointment.status = "CANCELLED"
        appointment.save()

        return Response(
            {
                "message": "Appointment cancelled successfully ✅",
                "data": AppointmentSerializer(appointment).data,
            },
            status=status.HTTP_200_OK,
        )



# -----------------------------
# APPOINTMENT DETAIL
# -----------------------------
class AppointmentDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdvocate]

    def get(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        self.check_object_permissions(request, appointment)

        return Response({
            "message": "Appointment fetched successfully ✅",
            "data": AppointmentSerializer(appointment).data
        })


# -----------------------------
# UPDATE APPOINTMENT
# -----------------------------
class AppointmentUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdvocate]

    def put(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        self.check_object_permissions(request, appointment)

        try:
            appointment = services.update_appointment(
                appointment,
                request.data
            )
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            "message": "Appointment updated successfully ✅",
            "data": AppointmentSerializer(appointment).data
        })
