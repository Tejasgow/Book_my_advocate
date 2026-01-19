from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Appointment
from .serializers import (
    AppointmentSerializer,
    AppointmentCreateSerializer
)
from .permissions import IsAdvocateUser


# -----------------------------
# Create Appointment (USER)
# -----------------------------
class AppointmentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AppointmentCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            appointment = serializer.save()
            return Response({
                "message": "Appointment booked successfully ✅",
                "data": AppointmentSerializer(appointment).data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------
# User Appointments
# -----------------------------
class UserAppointmentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        appointments = Appointment.objects.filter(user=request.user)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response({
            "message": "Your appointments fetched successfully ✅",
            "data": serializer.data
        })


# -----------------------------
# Advocate Appointments
# -----------------------------
class AdvocateAppointmentListView(APIView):
    permission_classes = [IsAuthenticated, IsAdvocateUser]

    def get(self, request):
        appointments = Appointment.objects.filter(
            advocate__user=request.user
        )
        serializer = AppointmentSerializer(appointments, many=True)
        return Response({
            "message": "Advocate appointments fetched successfully ✅",
            "data": serializer.data
        })


# -----------------------------
# Advocate Update Appointment Status
# -----------------------------
class AppointmentStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdvocateUser]

    def patch(self, request, pk):
        appointment = get_object_or_404(
            Appointment,
            pk=pk,
            advocate__user=request.user
        )

        status_value = request.data.get('status')
        allowed_status = ['APPROVED', 'REJECTED', 'COMPLETED']

        if status_value not in allowed_status:
            return Response(
                {"error": "Invalid status"},
                status=status.HTTP_400_BAD_REQUEST
            )

        appointment.status = status_value
        appointment.save()

        return Response({
            "message": "Appointment status updated ✅",
            "data": AppointmentSerializer(appointment).data
        })



