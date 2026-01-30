from django.urls import path
from .views import (RegisterView,LoginView,LogoutView,ProfileView,ChangePasswordView,
    ResetPasswordView,RequestPasswordOTPView,VerifyPasswordOTPView)
from rest_framework_simplejwt.views import (TokenRefreshView,TokenVerifyView)

app_name = "accounts"

urlpatterns = [

    # =================================================
    # AUTHENTICATION
    # =================================================
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),

    # =================================================
    # PROFILE
    # =================================================
    path('profile/', ProfileView.as_view(), name='profile-self'),
    path('profile/<int:user_id>/', ProfileView.as_view(), name='profile-detail'),

    # =================================================
    # PASSWORD MANAGEMENT
    # =================================================
    path('password/change/', ChangePasswordView.as_view(), name='password-change'),

    # OTP-based password reset
    path('password/otp/request/', RequestPasswordOTPView.as_view(), name='password-otp-request'),
    path('password/otp/verify/', VerifyPasswordOTPView.as_view(), name='password-otp-verify'),
    path('password/reset/', ResetPasswordView.as_view(), name='password-reset'),

    # =================================================
    # JWT TOKEN MANAGEMENT
    # =================================================
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),
]
