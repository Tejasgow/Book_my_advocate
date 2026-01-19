from rest_framework import serializers
from .models import Appointment
from app.advocates.serializers import AdvocateProfileSerializer
from app.accounts.serializers import ProfileSerializer

# -----------------------------
# Appointment Read Serializer
# -----------------------------
class AppointmentSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    advocate = AdvocateProfileSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'user', 'advocate',
            'appointment_date', 'appointment_time',
            'problem_description',
            'status', 'status_display',
            'created_at'
        ]


# -----------------------------
# Appointment Create Serializer
# -----------------------------
class AppointmentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = [
            'advocate',
            'appointment_date',
            'appointment_time',
            'problem_description'
        ]

    def validate(self, data):
        advocate = data['advocate']

        if not advocate.verified:
            raise serializers.ValidationError("You can book only VERIFIED advocates")

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        return Appointment.objects.create(user=user, **validated_data)
