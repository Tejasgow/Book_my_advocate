from rest_framework import serializers
from .models import ClientProfile
from app.accounts.serializers import ProfileSerializer

from app.appointments.models import Appointment
from app.cases.models import Case, CaseHearing, CaseDocument
from app.advocates.serializers import AdvocateProfileSerializer


# =================================================
# Client Profile (VIEW)
# =================================================
class ClientProfileViewSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = ClientProfile
        fields = [
            'id',
            'user',
            'phone',
            'address',
            'city',
            'is_verified',
            'created_at',
            'updated_at',
        ]


# =================================================
# Client Profile (UPDATE)
# =================================================
class ClientProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProfile
        fields = ['phone', 'address', 'city']


# 👉 Alias used in views (important)
ClientProfileSerializer = ClientProfileUpdateSerializer


# =================================================
# Client Appointments (READ ONLY)
# =================================================
class ClientAppointmentSerializer(serializers.ModelSerializer):
    client = ClientProfileViewSerializer(read_only=True)
    advocate = AdvocateProfileSerializer(read_only=True)
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    is_past_due = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            'id',
            'client',
            'advocate',
            'appointment_date',
            'appointment_time',
            'end_time',
            'duration_minutes',
            'problem_description',
            'remarks',
            'status',
            'status_display',
            'is_past_due',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields

    def get_is_past_due(self, obj):
        return obj.is_past_due()


# =================================================
# Client Cases (READ ONLY)
# =================================================
class ClientCaseSerializer(serializers.ModelSerializer):
    client = ClientProfileViewSerializer(read_only=True)
    advocate = serializers.SerializerMethodField()
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )

    class Meta:
        model = Case
        fields = '__all__'

    def get_advocate(self, obj):
        return {
            "id": obj.advocate.id,
            "username": obj.advocate.user.username,
            "email": obj.advocate.user.email,
            "phone": obj.advocate.phone,
        }


# =================================================
# Client Case Hearings
# =================================================
class ClientCaseHearingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseHearing
        fields = [
            'id',
            'hearing_date',
            'hearing_time',
            'court_name',
            'notes',
            'created_at',
        ]


# =================================================
# Client Case Documents
# =================================================
class ClientCaseDocumentSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(
        source='uploaded_by.username',
        read_only=True
    )

    class Meta:
        model = CaseDocument
        fields = [
            'id',
            'document',
            'description',
            'uploaded_by',
            'uploaded_by_name',
            'created_at',
        ]
        read_only_fields = [
            'uploaded_by',
            'uploaded_by_name',
            'created_at',
        ]
