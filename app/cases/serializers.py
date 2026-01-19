from rest_framework import serializers
from .models import Case, CaseHearing, CaseDocument
from app.accounts.serializers import ProfileSerializer
from app.advocates.serializers import AdvocateProfileSerializer


# -------------------------------------------------
# Case Serializer
# -------------------------------------------------
class CaseSerializer(serializers.ModelSerializer):
    client = ProfileSerializer(read_only=True)
    advocate = AdvocateProfileSerializer(read_only=True)
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )

    class Meta:
        model = Case
        fields = '__all__'


# -------------------------------------------------
# Case Create
# -------------------------------------------------
class CaseCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Case
        fields = ['appointment', 'title', 'description']

    def validate(self, data):
        appointment = data['appointment']

        if hasattr(appointment, 'case'):
            raise serializers.ValidationError("Case already exists")

        if appointment.status != 'APPROVED':
            raise serializers.ValidationError(
                "Case can be created only for APPROVED appointments"
            )

        return data

    def create(self, validated_data):
        appointment = validated_data['appointment']
        return Case.objects.create(
            appointment=appointment,
            client=appointment.user,
            advocate=appointment.advocate,
            title=validated_data['title'],
            description=validated_data['description']
        )


# -------------------------------------------------
# Case Hearing
# -------------------------------------------------
class CaseHearingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseHearing
        fields = '__all__'
        read_only_fields = ['case']


# -------------------------------------------------
# Case Document
# -------------------------------------------------
class CaseDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseDocument
        fields = '__all__'
        read_only_fields = ['case', 'uploaded_by']
