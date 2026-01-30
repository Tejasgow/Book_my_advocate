from rest_framework import serializers
from .models import Case, CaseHearing, CaseDocument
from app.advocates.serializers import AdvocateProfileSerializer


# =================================================
# CASE – READ SERIALIZER
# =================================================
class CaseSerializer(serializers.ModelSerializer):
    client = serializers.SerializerMethodField()
    advocate = AdvocateProfileSerializer(read_only=True)
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    hearings = serializers.SerializerMethodField()
    documents = serializers.SerializerMethodField()

    class Meta:
        model = Case
        fields = [
            'id',
            'appointment',
            'client',
            'advocate',
            'title',
            'description',
            'status',
            'status_display',
            'is_active',
            'hearings',
            'documents',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'client',
            'advocate',
            'status',
            'status_display',
            'hearings',
            'documents',
            'created_at',
            'updated_at',
        ]

    def get_client(self, obj):
        """Lazy import to avoid circular imports."""
        from app.client.serializers import ClientProfileSerializer
        return ClientProfileSerializer(obj.client).data

    def get_hearings(self, obj):
        return CaseHearingSerializer(
            obj.hearings.all(),
            many=True
        ).data

    def get_documents(self, obj):
        return CaseDocumentSerializer(
            obj.documents.all(),
            many=True
        ).data


# =================================================
# CASE – CREATE (ADVOCATE ONLY)
# =================================================
class CaseCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Case
        fields = ['appointment', 'title', 'description']

    def validate(self, data):
        appointment = data['appointment']

        # Prevent duplicate case
        if hasattr(appointment, 'case'):
            raise serializers.ValidationError(
                "A case already exists for this appointment."
            )

        # Only approved appointments
        if appointment.status != 'APPROVED':
            raise serializers.ValidationError(
                "Case can be created only for APPROVED appointments."
            )

        return data

    def create(self, validated_data):
        appointment = validated_data['appointment']

        return Case.objects.create(
            appointment=appointment,
            client=appointment.client,
            advocate=appointment.advocate,
            title=validated_data['title'],
            description=validated_data['description']
        )


# =================================================
# CASE HEARING SERIALIZER
# =================================================
class CaseHearingSerializer(serializers.ModelSerializer):

    class Meta:
        model = CaseHearing
        fields = [
            'id',
            'case',
            'hearing_date',
            'hearing_time',
            'court_name',
            'notes',
            'created_at',
        ]
        read_only_fields = ['id', 'case', 'created_at']


# =================================================
# CASE DOCUMENT SERIALIZER
# =================================================
class CaseDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CaseDocument
        fields = [
            'id',
            'case',
            'uploaded_by',
            'document',
            'description',
            'created_at',
        ]
        read_only_fields = ['id', 'case', 'uploaded_by', 'created_at']
