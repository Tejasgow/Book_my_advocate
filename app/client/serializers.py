from rest_framework import serializers
from .models import ClientProfile
from app.accounts.serializers import ProfileSerializer


# -----------------------------
# Client Profile
# -----------------------------
class ClientProfileViewSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = ClientProfile
        fields = ['id', 'user', 'phone', 'address', 'created_at', 'updated_at']


# -----------------------------
# Client Profile Update
# -----------------------------
class ClientProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProfile
        fields = ['phone', 'address']


# Alias for backwards compatibility
ClientProfileSerializer = ClientProfileUpdateSerializer


# -----------------------------
# Dashboard Serializer
# -----------------------------
class ClientDashboardSerializer(serializers.Serializer):
    total_appointments = serializers.IntegerField()
    upcoming_appointments = serializers.SerializerMethodField()
    total_cases = serializers.IntegerField()
    open_cases = serializers.SerializerMethodField()

    def get_upcoming_appointments(self, obj):
        """Lazy import to avoid circular imports."""
        from app.appointments.serializers import AppointmentSerializer
        if isinstance(obj, dict) and 'upcoming_appointments' in obj:
            return AppointmentSerializer(obj['upcoming_appointments'], many=True).data
        return []

    def get_open_cases(self, obj):
        """Lazy import to avoid circular imports."""
        from app.cases.serializers import CaseSerializer
        if isinstance(obj, dict) and 'open_cases' in obj:
            return CaseSerializer(obj['open_cases'], many=True).data
        return []


# -----------------------------
# Client Appointments
# -----------------------------
class ClientAppointmentSerializer(serializers.ModelSerializer):
    """Read-only serializer for client's appointments"""
    client = ClientProfileViewSerializer(source='client', read_only=True)

    class Meta:
        from app.appointments.models import Appointment
        model = Appointment
        fields = [
            'id', 'client', 'advocate', 'appointment_date', 'appointment_time',
            'end_time', 'duration_minutes', 'problem_description', 'remarks',
            'status', 'status_display', 'is_past_due', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'client', 'advocate', 'status', 'status_display',
            'end_time', 'is_past_due', 'created_at', 'updated_at'
        ]

    def get_is_past_due(self, obj):
        """Check if the appointment is past its scheduled time."""
        return obj.is_past_due()

    def get_advocate(self, obj):
        """Serialize advocate data."""
        from app.advocates.serializers import AdvocateProfileSerializer
        return AdvocateProfileSerializer(obj.advocate, read_only=True).data


# -----------------------------
# Client Cases
# -----------------------------
class ClientCaseSerializer(serializers.ModelSerializer):
    """Read-only serializer for client's cases"""
    client = ClientProfileViewSerializer(source='client', read_only=True)
    advocate = serializers.SerializerMethodField()
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )

    class Meta:
        from app.cases.models import Case
        model = Case
        fields = '__all__'

    def get_advocate(self, obj):
        return {
            "id": obj.advocate.id,
            "name": obj.advocate.user.username,
            "email": obj.advocate.user.email,
            "phone": obj.advocate.phone
        }


# -----------------------------
# Client Case Hearing
# -----------------------------
class ClientCaseHearingSerializer(serializers.ModelSerializer):
    class Meta:
        from app.cases.models import CaseHearing
        model = CaseHearing
        fields = ['id', 'hearing_date', 'hearing_time', 'court_name', 'notes', 'created_at']


# -----------------------------
# Client Case Document
# -----------------------------
class ClientCaseDocumentSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(source='uploaded_by.username', read_only=True)

    class Meta:
        from app.cases.models import CaseDocument
        model = CaseDocument
        fields = ['id', 'document', 'description', 'uploaded_by', 'uploaded_by_name', 'created_at']
