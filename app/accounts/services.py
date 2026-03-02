from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, PasswordResetOTP
from django.contrib.auth.hashers import make_password
import random
from django.contrib.auth.hashers import check_password
from django.utils import timezone

from rest_framework_simplejwt.tokens import RefreshToken

def create_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    tokens = {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

    return tokens

# =========================
# NOTIFICATION SERVICES
# =========================

def send_email(subject, message, email):
    if email:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=True
        )


def send_sms(phone, message):
    if phone:
        print(f"SMS to {phone}: {message}")


# =========================
# TOKEN SERVICES
# =========================

def generate_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }


def logout_user(refresh_token):
    token = RefreshToken(refresh_token)
    token.blacklist()


# =========================
# AUTH SERVICES
# =========================

def register_user(serializer):
    user = serializer.save()
    tokens = generate_tokens(user)

    send_email(
        "Welcome 🎉",
        f"Hi {user.username}, your account has been created successfully!",
        user.email
    )

    send_sms(
        user.phone,
        "Your account has been created successfully!"
    )

    return user, tokens


def login_user(user):
    tokens = generate_tokens(user)

    send_email(
        "Login Alert",
        f"Hi {user.username}, you logged in successfully!",
        user.email
    )

    send_sms(
        user.phone,
        "Login successful ✅"
    )

    return tokens


# =========================
# PROFILE SERVICES
# =========================

def get_user(request_user, user_id=None):
    if user_id:
        return User.objects.filter(id=user_id).first()
    return request_user


def update_profile(user, serializer):
    serializer.save()

    send_email(
        "Profile Updated",
        "Your profile has been updated successfully.",
        user.email
    )

    send_sms(
        user.phone,
        "Profile updated successfully ✅"
    )


# =========================
# PASSWORD SERVICES
# =========================

def change_password(user, new_password):
    user.set_password(new_password)
    user.save()

    send_email(
        "Password Changed",
        "Your password has been changed successfully.",
        user.email
    )

    send_sms(
        user.phone,
        "Password changed successfully ✅"
    )


# =========================
# OTP SERVICES
# =========================
def request_password_otp(phone):
    user = User.objects.filter(phone=phone).first()
    if not user:
        raise ValueError("User not found")

    # Remove previous unused OTPs
    PasswordResetOTP.objects.filter(
        user=user,
        is_used=False
    ).delete()

    # Create OTP object
    otp_obj = PasswordResetOTP(user=user)

    # Explicitly generate OTP
    raw_otp = otp_obj.set_otp()
    otp_obj.save()

    # Send raw OTP
    send_sms(
        user.phone,
        f"Your OTP is {raw_otp}. Valid for 10 minutes."
    )

    send_email(
        "Password Reset OTP",
        f"Your OTP is {raw_otp}. Valid for 10 minutes.",
        user.email
    )

    return otp_obj


def verify_password_otp(user, entered_otp):
    try:
        otp_obj = PasswordResetOTP.objects.get(
            user=user,
            is_used=False
        )
    except PasswordResetOTP.DoesNotExist:
        return False, "OTP not found or already used"

    # Verify OTP
    if not check_password(entered_otp, otp_obj.otp):
        return False, "Invalid OTP"

    # Mark OTP as used
    otp_obj.is_used = True
    otp_obj.verified_at = timezone.now()
    otp_obj.save()

    send_email(
        "OTP Verified",
        "OTP verified successfully ✅",
        user.email
    )

    send_sms(
        user.phone,
        "OTP verified successfully ✅"
    )

    return True, "OTP verified successfully"


def reset_password(user, otp_obj, new_password):
    user.set_password(new_password)
    user.save()

    otp_obj.is_used = True
    otp_obj.save()

    send_email(
        "Password Reset Successful",
        "Your password has been reset successfully 🔐",
        user.email
    )

    send_sms(
        user.phone,
        "Password reset successfully ✅"
    )
