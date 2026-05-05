from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .services import create_tokens_for_user
from rest_framework import status
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ProfileSerializer,
    ChangePasswordSerializer,
    RequestOTPSerializer,
    VerifyOTPSerializer,
    ResetPasswordSerializer,
)

from .services import (
    register_user,
    login_user,
    update_profile,
    change_password,
    request_password_otp,
    verify_password_otp,
    reset_password,
    logout_user,
)
from django.contrib.auth import get_user_model
User = get_user_model()


# =================================================
# COOKIE UTILITIES
# =================================================

ACCESS_COOKIE_NAME = "access_token"
REFRESH_COOKIE_NAME = "refresh_token"


def set_auth_cookies(response, tokens):
    """
    Store JWT tokens securely in HttpOnly cookies
    """
    response.set_cookie(
        key=ACCESS_COOKIE_NAME,
        value=tokens["access"],
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="Lax",
        path="/",
        max_age=60 * 60 * 24,  # 24 hours
    )
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=tokens["refresh"],
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="Lax",
        path="/",
        max_age=60 * 60 * 24 * 7,  # 7 days
    )


def clear_auth_cookies(response):
    response.delete_cookie(ACCESS_COOKIE_NAME)
    response.delete_cookie(REFRESH_COOKIE_NAME)


# =================================================
# AUTH
# =================================================
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        tokens = create_tokens_for_user(user)

        response = Response(
            {
                "message": "User registered successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "middle_name": user.middle_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "role": user.role,
                },
                "tokens": tokens,  # Include tokens in response for frontend
            },
            status=status.HTTP_201_CREATED,
        )
        set_auth_cookies(response, tokens)
        return response

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        tokens = login_user(user)

        response = Response(
            {
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "middle_name": user.middle_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "role": user.role,
                },
                "tokens": tokens,
            },
            status=status.HTTP_200_OK,
        )

        set_auth_cookies(response, tokens)
        return response


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token:
            logout_user(refresh_token)

        response = Response(
            {"message": "Logout successful"},
            status=status.HTTP_205_RESET_CONTENT,
        )

        clear_auth_cookies(response)
        return response

# =================================================
# PROFILE
# =================================================

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = ProfileSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        update_profile(request.user, serializer)

        return Response(
            {"message": "Profile updated successfully"},
            status=status.HTTP_200_OK,
        )


# =================================================
# PASSWORD MANAGEMENT
# =================================================

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        change_password(
            request.user,
            serializer.validated_data["new_password"],
        )

        return Response(
            {"message": "Password changed successfully"},
            status=status.HTTP_200_OK,
        )


class RequestPasswordOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request_password_otp(serializer.validated_data["phone"])

        return Response(
            {"message": "OTP sent successfully"},
            status=status.HTTP_200_OK,
        )

class VerifyPasswordOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data["phone"]
        entered_otp = serializer.validated_data["otp"]

        user = User.objects.get(phone=phone)

        success, message = verify_password_otp(user, entered_otp)

        if not success:
            return Response(
                {"error": message},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"message": message},
            status=status.HTTP_200_OK
        )


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reset_password(
            user=serializer.validated_data["user"],
            otp_obj=serializer.validated_data["otp_obj"],
            new_password=serializer.validated_data["new_password"],
        )

        return Response(
            {"message": "Password reset successfully"},
            status=status.HTTP_200_OK,
        )


# =================================================
# TOKEN REFRESH
# =================================================

class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Get refresh token from request body or cookies
        refresh_token = request.data.get("refresh") or request.COOKIES.get("refresh_token")
        
        if not refresh_token:
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            refresh = RefreshToken(refresh_token)
            tokens = {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
            
            response = Response({
                "access": tokens["access"],
                "refresh": tokens["refresh"],
            })
            
            # Also set cookies
            set_auth_cookies(response, tokens)
            
            return response
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )

