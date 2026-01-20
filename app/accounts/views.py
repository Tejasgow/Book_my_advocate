from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings

from .models import User, PasswordResetOTP
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ProfileSerializer,
    ChangePasswordSerializer,
    RequestOTPSerializer,
    VerifyOTPSerializer,
    ResetPasswordSerializer
)

# -----------------------------
# REGISTER
# -----------------------------
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "message": "User registered successfully 🎉",
                    "tokens": {
                        "access": str(refresh.access_token),
                        "refresh": str(refresh)
                    },
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "role": user.role
                    }
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------
# LOGIN
# -----------------------------
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "Login successful ✅",
                "tokens": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                },
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role
                }
            },
            status=status.HTTP_200_OK
        )


# -----------------------------
# PROFILE
# -----------------------------
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id=None):
        user = request.user if not user_id else User.objects.filter(id=user_id).first()

        if not user:
            return Response({"error": "User not found"}, status=404)

        serializer = ProfileSerializer(user)
        return Response(
            {"message": "Profile fetched successfully ✅", "data": serializer.data}
        )

    def put(self, request, user_id=None):
        user = request.user if not user_id else User.objects.filter(id=user_id).first()

        if not user:
            return Response({"error": "User not found"}, status=404)

        serializer = ProfileSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Profile updated successfully ✨", "data": serializer.data}
        )


# -----------------------------
# CHANGE PASSWORD
# -----------------------------
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()

        return Response({"message": "Password changed successfully 🔐"})


# -----------------------------
# REQUEST OTP
# -----------------------------
class RequestPasswordOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data["phone"]
        user = User.objects.filter(phone=phone).first()

        if not user:
            return Response({"error": "User not found"}, status=404)

        PasswordResetOTP.objects.filter(user=user).delete()
        otp_obj = PasswordResetOTP.objects.create(user=user)

        if user.email:
            send_mail(
                subject="Password Reset OTP",
                message=f"Your OTP is {otp_obj.otp}. Valid for 5 minutes.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )

        return Response({"message": "OTP sent successfully ✅"})


# -----------------------------
# VERIFY OTP
# -----------------------------
class VerifyPasswordOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data["phone"]
        otp = serializer.validated_data["otp"]

        user = User.objects.filter(phone=phone).first()
        if not user:
            return Response({"error": "User not found"}, status=404)

        otp_obj = PasswordResetOTP.objects.filter(
            user=user, otp=otp, is_used=False
        ).last()

        if not otp_obj or otp_obj.is_expired():
            return Response({"error": "Invalid or expired OTP"}, status=400)

        otp_obj.is_used = True
        otp_obj.save()

        return Response({"message": "OTP verified successfully ✅"})


# -----------------------------
# RESET PASSWORD
# -----------------------------
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data["phone"]
        otp = serializer.validated_data["otp"]
        new_password = serializer.validated_data["new_password"]

        user = User.objects.filter(phone=phone).first()
        if not user:
            return Response({"error": "User not found"}, status=404)

        otp_obj = PasswordResetOTP.objects.filter(
            user=user, otp=otp, is_used=False
        ).last()

        if not otp_obj or otp_obj.is_expired():
            return Response({"error": "Invalid or expired OTP"}, status=400)

        user.set_password(new_password)
        user.save()

        otp_obj.is_used = True
        otp_obj.save()

        return Response({"message": "Password reset successfully 🔐"})


# -----------------------------
# LOGOUT
# -----------------------------
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"error": "Refresh token required"}, status=400)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful 👋"}, status=205)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
