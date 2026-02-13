from datetime import datetime, timedelta

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from .models import Appointment
from app.advocates.serializers import AdvocateProfileSerializer
# -----------------------------
# Read Appointment Serializer
# -----------------------------
class AppointmentSerializer(serializers.ModelSerializer):
    client = serializers.SerializerMethodField()
    advocate = AdvocateProfileSerializer(read_only=True)
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True
    )
    end_time = serializers.SerializerMethodField()
    is_past_due = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            "id",
            "client",
            "advocate",
            "appointment_date",
            "appointment_time",
            "end_time",
            "duration_minutes",
            "problem_description",
            "remarks",
            "status",
            "status_display",
            "is_past_due",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "client",
            "advocate",
            "status",
            "status_display",
            "end_time",
            "is_past_due",
            "created_at",
            "updated_at",
        ]

    def get_client(self, obj):
        from app.client.serializers import ClientProfileSerializer
        return ClientProfileSerializer(obj.client).data

    def get_end_time(self, obj):
        return obj.end_time

    def get_is_past_due(self, obj):
        return obj.is_past_due()
# -----------------------------
# Create Appointment Serializer
# -----------------------------
class AppointmentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = [
            "advocate",
            "appointment_date",
            "appointment_time",
            "duration_minutes",
            "problem_description",
        ]

    def validate_appointment_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError(
                "Appointment date cannot be in the past"
            )
        return value

    def validate(self, data):
        advocate = data["advocate"]

        if not advocate.is_verified:
            raise serializers.ValidationError(
                "You can book appointments only with VERIFIED advocates"
            )

        date = data["appointment_date"]
        start_time = data["appointment_time"]
        duration = data.get("duration_minutes", 30)

        new_start = timezone.make_aware(
            datetime.combine(date, start_time)
        )
        new_end = new_start + timedelta(minutes=duration)

        conflicts = Appointment.objects.filter(
            advocate=advocate,
            appointment_date=date,
            is_active=True,
            status__in=[
                Appointment.STATUS_PENDING,
                Appointment.STATUS_APPROVED,
            ],
        )

        for appt in conflicts:
            existing_start = timezone.make_aware(
                datetime.combine(
                    appt.appointment_date,
                    appt.appointment_time,
                )
            )
            existing_end = timezone.make_aware(
                datetime.combine(
                    appt.appointment_date,
                    appt.end_time,
                )
            )

            if new_start < existing_end and new_end > existing_start:
                raise serializers.ValidationError(
                    "The advocate already has an appointment during this time"
                )

        return data

    def create(self, validated_data):
        request = self.context["request"]

        try:
            client = request.user.client_profile
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                "Client profile not found. Please complete your profile."
            )

        return Appointment.objects.create(
            client=client,
            **validated_data
        )

# -----------------------------
# Update Appointment Serializer
# -----------------------------
class AppointmentUpdateSerializer(serializers.ModelSerializer):
    reschedule_date = serializers.DateField(required=False)
    reschedule_time = serializers.TimeField(required=False)

    class Meta:
        model = Appointment
        fields = [
            "appointment_date",
            "appointment_time",
            "duration_minutes",
            "problem_description",
            "remarks",
            "reschedule_date",
            "reschedule_time",
        ]

    def validate(self, data):
        date = data.get("reschedule_date")
        time = data.get("reschedule_time")

        if date and time:
            duration = data.get(
                "duration_minutes",
                self.instance.duration_minutes,
            )

            new_start = timezone.make_aware(
                datetime.combine(date, time)
            )
            new_end = new_start + timedelta(minutes=duration)

            conflicts = Appointment.objects.filter(
                advocate=self.instance.advocate,
                appointment_date=date,
                is_active=True,
                status__in=[
                    Appointment.STATUS_PENDING,
                    Appointment.STATUS_APPROVED,
                ],
            ).exclude(id=self.instance.id)

            for appt in conflicts:
                existing_start = timezone.make_aware(
                    datetime.combine(
                        appt.appointment_date,
                        appt.appointment_time,
                    )
                )
                existing_end = timezone.make_aware(
                    datetime.combine(
                        appt.appointment_date,
                        appt.end_time,
                    )
                )

                if new_start < existing_end and new_end > existing_start:
                    raise serializers.ValidationError(
                        "The advocate already has an appointment during this time"
                    )

            data["appointment_date"] = date
            data["appointment_time"] = time

        return data
