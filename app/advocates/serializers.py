from rest_framework import serializers
from .models import AdvocateProfile, AssistantLawyer
from app.accounts.serializers import ProfileSerializer


# ======================================================
# ADVOCATE PROFILE SERIALIZERS
# ======================================================

class AdvocateProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for reading Advocate Profile details
    """
    user = ProfileSerializer(read_only=True)
    specialization_display = serializers.CharField(
        source='get_specialization_display', read_only=True
    )

    class Meta:
        model = AdvocateProfile
        fields = [
            'id', 'user', 'specialization', 'specialization_display',
            'experience_years', 'bar_council_id', 'consultation_fee',
            'verified', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'verified', 'created_at', 'updated_at', 'specialization_display'
        ]


class AdvocateCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating Advocate Profile
    Accepts human-readable specialization names
    """
    specialization = serializers.CharField()

    class Meta:
        model = AdvocateProfile
        fields = ['specialization', 'experience_years', 'bar_council_id', 'consultation_fee']

    def to_internal_value(self, data):
        """
        Convert human-readable specialization to internal DB value
        """
        specialization_input = data.get('specialization', '').strip().upper()
        mapping = {v.upper(): k for k, v in AdvocateProfile.SPECIALIZATION_CHOICES}

        if specialization_input in mapping:
            data['specialization'] = mapping[specialization_input]
        elif specialization_input in [k for k, v in AdvocateProfile.SPECIALIZATION_CHOICES]:
            data['specialization'] = specialization_input
        else:
            raise serializers.ValidationError({'specialization': 'Invalid specialization'})

        return super().to_internal_value(data)

    def validate_experience_years(self, value):
        if value < 0:
            raise serializers.ValidationError("Experience years must be a positive number")
        return value

    def create(self, validated_data):
        user = self.context['request'].user

        if user.role != 'ADVOCATE':
            raise serializers.ValidationError({"detail": "Only advocates can create an advocate profile"})

        if hasattr(user, 'advocate_profile'):
            raise serializers.ValidationError({"detail": "Profile already exists for this user"})

        return AdvocateProfile.objects.create(user=user, **validated_data)


class AdvocateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating Advocate Profile
    """
    class Meta:
        model = AdvocateProfile
        fields = ['specialization', 'experience_years', 'consultation_fee']

    def validate_experience_years(self, value):
        if value < 0:
            raise serializers.ValidationError("Experience years must be a positive number")
        return value

    def validate_specialization(self, value):
        choices = [k for k, v in AdvocateProfile.SPECIALIZATION_CHOICES]
        if value not in choices:
            raise serializers.ValidationError("Invalid specialization")
        return value


# ======================================================
# ASSISTANT LAWYER SERIALIZERS
# ======================================================

class AssistantLawyerSerializer(serializers.ModelSerializer):
    """
    Serializer for reading / assigning Assistant Lawyer
    """
    user = ProfileSerializer(read_only=True)
    advocate_name = serializers.CharField(source='advocate.user.username', read_only=True)

    class Meta:
        model = AssistantLawyer
        fields = ['id', 'user', 'advocate', 'advocate_name', 'assigned_at', 'is_active']
        read_only_fields = ['id', 'user', 'advocate_name', 'assigned_at']

    def validate(self, attrs):
        """
        Ensure only advocates can have assistants assigned
        """
        advocate = attrs.get('advocate')
        if not advocate or advocate.user.role != 'ADVOCATE':
            raise serializers.ValidationError("Assistants can only be assigned to advocates")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user

        # Ensure assistant is an advocate themselves (or your rule)
        if user.role != 'ADVOCATE':
            raise serializers.ValidationError({"detail": "Only advocate users can be assigned as assistants"})

        return AssistantLawyer.objects.create(user=user, **validated_data)
