from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, PasswordResetOTP
import re

# =================================================
# VALIDATORS
# =================================================

def password_validator(password):
    if len(password) < 8:
        raise serializers.ValidationError("Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        raise serializers.ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise serializers.ValidationError("Password must contain at least one lowercase letter.")
    if not re.search(r"\d", password):
        raise serializers.ValidationError("Password must contain at least one number.")
    return password


def username_validator(username):
    if not re.search(r"[A-Z]", username):
        raise serializers.ValidationError("Username must contain at least one uppercase letter.")
    return username


# =================================================
# REGISTER
# =================================================

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[password_validator])
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'phone',
            'password',
            'confirm_password',
            'role',
            'address',
        )

    def validate_phone(self, value):
        value = value.strip()
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Phone number already registered")
        return value

    def validate_email(self, value):
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match"}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)


# =================================================
# LOGIN
# =================================================

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            username=attrs.get('username'),
            password=attrs.get('password')
        )

        if not user:
            raise serializers.ValidationError("Invalid username or password")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")

        attrs['user'] = user
        return attrs


# =================================================
# PROFILE
# =================================================

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'phone',
            'role',
            'address',
        )
        read_only_fields = ('id', 'username', 'email', 'role')


# =================================================
# CHANGE PASSWORD
# =================================================

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[password_validator])
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match"}
            )
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value


# =================================================
# OTP / RESET PASSWORD
# =================================================

class RequestOTPSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate_phone(self, value):
        value = value.strip()
        if not User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("User with this phone does not exist")
        return value


class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField()
    otp = serializers.CharField(max_length=6)

    def validate(self, attrs):
        user = User.objects.filter(phone=attrs['phone']).first()
        if not user:
            raise serializers.ValidationError("Invalid phone number")

        otp_obj = PasswordResetOTP.objects.filter(
            user=user,
            is_used=False
        ).last()

        if not otp_obj or otp_obj.is_expired():
            raise serializers.ValidationError("OTP is invalid or expired")

        if not otp_obj.verify_otp(attrs['otp']):
            raise serializers.ValidationError("Invalid OTP")

        attrs['user'] = user
        attrs['otp_obj'] = otp_obj
        return attrs

class ResetPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField()
    otp = serializers.CharField()
    new_password = serializers.CharField(
        write_only=True,
        validators=[password_validator]
    )
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        # 1️⃣ Password match
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match"
            })

        # 2️⃣ User check
        user = User.objects.filter(phone=attrs["phone"]).first()
        if not user:
            raise serializers.ValidationError("Invalid phone number")

        # 3️⃣ Latest unused OTP
        otp_obj = (
            PasswordResetOTP.objects
            .filter(user=user, is_used=False)
            .order_by("-created_at")
            .first()
        )

        if not otp_obj or otp_obj.is_expired():
            raise serializers.ValidationError("OTP is invalid or expired")

        # 4️⃣ OTP verify (hashed)
        if not otp_obj.verify_otp(str(attrs["otp"])):
            raise serializers.ValidationError("OTP is invalid or expired")

        attrs["user"] = user
        attrs["otp_obj"] = otp_obj
        return attrs