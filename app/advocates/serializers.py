from rest_framework import serializers
from .models import AdvocateProfile
from app.accounts.serializers import ProfileSerializer

# -----------------------------
# Advocate Profile Serializer (for reading)
# -----------------------------
class AdvocateProfileSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    specialization_display = serializers.CharField(
        source='get_specialization_display', read_only=True
    )

    class Meta:
        model = AdvocateProfile
        fields = [
            'id', 'user', 'specialization', 'specialization_display',
            'experience_years', 'bar_council_id', 'consultation_fee',
            'verified', 'created_at'
        ]
        read_only_fields = [
            'id', 'user', 'verified', 'created_at', 'specialization_display'
        ]


# -----------------------------
# Advocate Create Serializer (for creating profile)
# -----------------------------
class AdvocateCreateSerializer(serializers.ModelSerializer):
    # Accept human-readable labels
    specialization = serializers.CharField()

    class Meta:
        model = AdvocateProfile
        fields = ['specialization', 'experience_years', 'bar_council_id', 'consultation_fee']

    def to_internal_value(self, data):
        # Map human-readable specialization to DB key
        specialization_input = data.get('specialization', '').strip().upper()
        mapping = {v.upper(): k for k, v in AdvocateProfile.specialization_choices}

        if specialization_input in mapping:
            data['specialization'] = mapping[specialization_input]
        elif specialization_input in [k for k, v in AdvocateProfile.specialization_choices]:
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

        # Prevent duplicate profile creation
        if hasattr(user, 'advocate_profile'):
            raise serializers.ValidationError({"detail": "Profile already exists for this user"})

        advocate_profile = AdvocateProfile.objects.create(user=user, **validated_data)
        return advocate_profile
