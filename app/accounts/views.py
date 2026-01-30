from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .serializers import (RegisterSerializer,LoginSerializer,ProfileSerializer,
    ChangePasswordSerializer,RequestOTPSerializer,VerifyOTPSerializer,
    ResetPasswordSerializer)

from .services import (register_user,login_user,get_user,update_profile,change_password,
    request_password_otp,verify_password_otp,reset_password,logout_user)


# =====================
# REGISTER
# =====================
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, tokens = register_user(serializer)

        return Response({
            "message": "User registered successfully 🎉",
            "tokens": tokens,
            "user": {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "middle_name": user.middle_name ,
                "last_name": user.last_name,
                "email": user.email,
                "role": user.role,
            }
        }, status=201)

# =====================
# LOGIN
# =====================
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        tokens = login_user(user)

        return Response({
            "message": "Login successful ✅",
            "tokens": tokens
        })


# =====================
# PROFILE
# =====================
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id=None):
        user = get_user(request.user, user_id)
        if not user:
            return Response({"error": "User not found"}, status=404)

        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request, user_id=None):
        user = get_user(request.user, user_id)
        if not user:
            return Response({"error": "User not found"}, status=404)

        serializer = ProfileSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        update_profile(user, serializer)
        return Response({"message": "Profile updated successfully ✨"})


# =====================
# CHANGE PASSWORD
# =====================
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        change_password(
            request.user,
            serializer.validated_data["new_password"]
        )

        return Response({"message": "Password changed successfully 🔐"})


# =====================
# REQUEST OTP
# =====================
class RequestPasswordOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request_password_otp(serializer.validated_data["phone"])
        return Response({"message": "OTP sent successfully ✅"})


# =====================
# VERIFY OTP
# =====================
class VerifyPasswordOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        verify_password_otp(serializer.validated_data["otp_obj"])
        return Response({"message": "OTP verified successfully ✅"})


# =====================
# RESET PASSWORD
# =====================
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reset_password(
            serializer.validated_data["user"],
            serializer.validated_data["otp_obj"],
            serializer.validated_data["new_password"]
        )

        return Response({"message": "Password reset successfully 🔐"})


# =====================
# LOGOUT
# =====================
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh = request.data.get("refresh")
        if not refresh:
            return Response({"error": "Refresh token required"}, status=400)

        logout_user(refresh)
        return Response({"message": "Logout successful 👋"}, status=205)
