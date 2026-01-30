from rest_framework import serializers
from django.utils import timezone
from datetime import datetime, timedelta, time

from .models import Appointment
from app.advocates.serializers import AdvocateProfileSerializer

# -----------------------------
# Read Appointment Serializer
# -----------------------------
class AppointmentSerializer(serializers.ModelSerializer):
    client = serializers.SerializerMethodField()
    advocate = AdvocateProfileSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    end_time = serializers.SerializerMethodField()
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
        read_only_fields = [
            'id',
            'client',
            'advocate',
            'status',
            'status_display',
            'end_time',
            'is_past_due',
            'created_at',
            'updated_at',
        ]

    def get_end_time(self, obj):
        return obj.end_time

    def get_is_past_due(self, obj):
        return obj.is_past_due()

    def get_client(self, obj):
        # Lazy import to avoid circular dependency
        from app.client.serializers import ClientProfileSerializer
        return ClientProfileSerializer(obj.client).data

# -----------------------------
# Create Appointment Serializer
# -----------------------------
class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            'advocate',
            'appointment_date',
            'appointment_time',
            'duration_minutes',
            'problem_description',
        ]

    def validate_appointment_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Appointment date cannot be in the past")
        return value

    def validate_appointment_time(self, value):
        if not isinstance(value, time):
            raise serializers.ValidationError("Invalid time format")
        return value

    def validate(self, data):
        advocate = data['advocate']

        if not advocate.verified:
            raise serializers.ValidationError(
                "You can book appointments only with VERIFIED advocates"
            )

        date = data['appointment_date']
        start_time = data['appointment_time']
        duration = data.get('duration_minutes', 30)

        new_start = datetime.combine(date, start_time)
        new_end = new_start + timedelta(minutes=duration)

        overlapping_appointments = Appointment.objects.filter(
            advocate=advocate,
            appointment_date=date,
            is_active=True,
            status__in=[
                Appointment.STATUS_PENDING,
                Appointment.STATUS_APPROVED,
            ],
        )

        for appointment in overlapping_appointments:
            existing_start = datetime.combine(
                appointment.appointment_date,
                appointment.appointment_time,
            )
            existing_end = datetime.combine(
                appointment.appointment_date,
                appointment.end_time,
            )

            if new_start < existing_end and new_end > existing_start:
                raise serializers.ValidationError(
                    "The advocate already has an appointment during this time"
                )

        return data

    def create(self, validated_data):
        """
        Assign client automatically from logged-in user
        """
        request = self.context['request']
        client = request.user.client_profile
        return Appointment.objects.create(client=client, **validated_data)


# -----------------------------
# Update Appointment Serializer
# -----------------------------
class AppointmentUpdateSerializer(serializers.ModelSerializer):
    reschedule_date = serializers.DateField(required=False)
    reschedule_time = serializers.TimeField(required=False)

    class Meta:
        model = Appointment
        fields = [
            'appointment_date',
            'appointment_time',
            'duration_minutes',
            'problem_description',
            'remarks',
            'reschedule_date',
            'reschedule_time',
        ]

    def validate(self, data):
        reschedule_date = data.get('reschedule_date')
        reschedule_time = data.get('reschedule_time')

        if reschedule_date and reschedule_time:
            duration = data.get(
                'duration_minutes',
                self.instance.duration_minutes,
            )

            new_start = datetime.combine(reschedule_date, reschedule_time)
            new_end = new_start + timedelta(minutes=duration)

            overlapping_appointments = Appointment.objects.filter(
                advocate=self.instance.advocate,
                appointment_date=reschedule_date,
                is_active=True,
                status__in=[
                    Appointment.STATUS_PENDING,
                    Appointment.STATUS_APPROVED,
                ],
            ).exclude(id=self.instance.id)

            for appointment in overlapping_appointments:
                existing_start = datetime.combine(
                    appointment.appointment_date,
                    appointment.appointment_time,
                )
                existing_end = datetime.combine(
                    appointment.appointment_date,
                    appointment.end_time,
                )

                if new_start < existing_end and new_end > existing_start:
                    raise serializers.ValidationError(
                        "The advocate already has an appointment during this time"
                    )

            # Apply reschedule
            data['appointment_date'] = reschedule_date
            data['appointment_time'] = reschedule_time

        return data
