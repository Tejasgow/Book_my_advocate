from rest_framework import serializers
from .models import AdvocateProfile, AssistantLawyer
from app.accounts.serializers import ProfileSerializer
from app.accounts.models import User


# ======================================================
# ADVOCATE PROFILE READ SERIALIZER
# ======================================================

class AdvocateProfileSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    advocate_id = serializers.SerializerMethodField()
    specialization_display = serializers.CharField(source="get_specialization_display",read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    class Meta:
        model = AdvocateProfile
        fields = [
            "id",
            "advocate_id",
            "user",
            # Profile
            "phone",
            "profile_photo",
            "bio",
            # Professional
            "specialization",
            "specialization_display",
            "experience_years",
            "enrollment_year",
            "languages_spoken",
            "court_type",
            "consultation_fee",
            # Location
            "city",
            "state",
            # Verification
            "is_verified",
            "verified_at",
            "verified_by",
            # Status
            "is_active",
            "rating",
            # Timestamps
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "advocate_id",
            "user",
            "is_verified",
            "verified_at",
            "rating",
            "created_at",
            "updated_at",
            "specialization_display",
        ]

    def get_advocate_id(self, obj):
        return f"ADV-{obj.id:05d}"


# ======================================================
# ADVOCATE PROFILE CREATE SERIALIZER
# ======================================================

class AdvocateCreateSerializer(serializers.ModelSerializer):
    """
    Used ONLY for creating advocate profile
    (Permissions handled in view)
    """
    specialization = serializers.CharField()

    class Meta:
        model = AdvocateProfile
        fields = [
            "phone",
            "bio",
            "specialization",
            "experience_years",
            "bar_council_id",
            "enrollment_year",
            "languages_spoken",
            "court_type",
            "city",
            "state",
            "consultation_fee",
        ]

    # -----------------------------
    # SPECIALIZATION MAPPING
    # -----------------------------
    def to_internal_value(self, data):
        data = data.copy()
        specialization_input = data.get("specialization", "").strip().upper()
        mapping = {label.upper(): key for key, label in AdvocateProfile.SPECIALIZATION_CHOICES }
        if specialization_input in mapping:
            data["specialization"] = mapping[specialization_input]
        elif specialization_input in dict(AdvocateProfile.SPECIALIZATION_CHOICES):
            data["specialization"] = specialization_input
        else:
            raise serializers.ValidationError({"specialization": "Invalid specialization"})
        return super().to_internal_value(data)

    # -----------------------------
    # FIELD VALIDATIONS
    # -----------------------------
    def validate_experience_years(self, value):
        if value < 0:
            raise serializers.ValidationError("Experience years must be a positive number")
        return value

    def validate_bar_council_id(self, value):
        if AdvocateProfile.objects.filter(bar_council_id=value).exists():
            raise serializers.ValidationError("This Bar Council ID already exists")
        return value

    # -----------------------------
    # CREATE PROFILE
    # -----------------------------
    def create(self, validated_data):
        return AdvocateProfile.objects.create(
            user=self.context["request"].user,
            **validated_data
        )


# ======================================================
# ADVOCATE PROFILE SELF UPDATE SERIALIZER
# ======================================================

class AdvocateUpdateSerializer(serializers.ModelSerializer):
    """
    Used for advocate self-update ONLY
    """

    class Meta:
        model = AdvocateProfile
        fields = [
            "phone",
            "bio",
            "specialization",
            "experience_years",
            "languages_spoken",
            "court_type",
            "city",
            "state",
            "consultation_fee",
        ]

    def validate_experience_years(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Experience years must be a positive number"
            )
        return value

    def validate_specialization(self, value):
        valid_choices = dict(AdvocateProfile.SPECIALIZATION_CHOICES).keys()
        if value not in valid_choices:
            raise serializers.ValidationError("Invalid specialization")
        return value


# ======================================================
# ADVOCATE ID CARD UPLOAD SERIALIZER
# ======================================================

class AdvocateIDUploadSerializer(serializers.ModelSerializer):
    """
    Used ONLY for uploading official ID card
    """

    class Meta:
        model = AdvocateProfile
        fields = ["official_id_card"]

    def validate_official_id_card(self, value):
        if not value:
            raise serializers.ValidationError("ID card file is required")
        return value


# ======================================================
# ASSISTANT LAWYER READ SERIALIZER
# ======================================================

class AssistantLawyerSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    advocate_name = serializers.CharField(
        source="advocate.user.username",
        read_only=True
    )

    class Meta:
        model = AssistantLawyer
        fields = [
            "id",
            "user",
            "advocate_name",
            "assigned_at",
            "is_active",
        ]
        read_only_fields = fields


# ======================================================
# ASSISTANT LAWYER CREATE SERIALIZER
# ======================================================

class AssistantLawyerCreateSerializer(serializers.Serializer):
    """
    Used for assigning assistant lawyer
    (Ownership + permission handled in view)
    """
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")

        if user.role != "ASSISTANT":
            raise serializers.ValidationError(
                "User must have ASSISTANT role"
            )

        if hasattr(user, "assistant_profile"):
            raise serializers.ValidationError(
                "This user is already assigned as an assistant"
            )

        return value
