from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone

from app.accounts.models import User
from .models import AdvocateProfile, AssistantLawyer

# -----------------------------
# Dummy SMS function
# -----------------------------
def send_sms(phone, message):
    if phone:
        print(f"SMS to {phone}: {message}")
        # Integrate Twilio or another SMS API here


# ======================================================
# ADVOCATE PROFILE SERVICES
# ======================================================

def create_advocate_profile(user, data):
    """
    Create advocate profile and send notifications
    """
    if hasattr(user, "advocate_profile"):
        raise ValueError("Profile already exists for this user")

    advocate = AdvocateProfile.objects.create(user=user, **data)

    # Notify the advocate
    if user.email:
        send_mail(
            "Advocate Profile Created ✅",
            f"Hi {user.username}, your advocate profile has been created successfully!",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )
    if hasattr(user, "phone") and user.phone:
        send_sms(user.phone, "Your advocate profile has been created successfully ✅")

    # Notify admins
    admins = User.objects.filter(role="ADMIN", is_active=True)
    admin_emails = [admin.email for admin in admins if admin.email]
    admin_phones = [admin.phone for admin in admins if admin.phone]

    if admin_emails:
        send_mail(
            "New Advocate Profile Created",
            f"Advocate {user.username} has created a profile and is awaiting verification.",
            settings.DEFAULT_FROM_EMAIL,
            admin_emails,
        )
    for phone in admin_phones:
        send_sms(phone, f"New advocate profile created by {user.username} ✅")

    return advocate


def list_verified_advocates(specialization=None):
    """
    List all verified advocates, optionally filter by specialization
    """
    queryset = AdvocateProfile.objects.filter(is_verified=True)
    if specialization:
        queryset = queryset.filter(specialization__iexact=specialization.upper())
    return queryset


def get_advocate_by_id(pk):
    """
    Fetch a verified advocate by ID
    """
    return get_object_or_404(AdvocateProfile, pk=pk, is_verified=True)


def update_advocate_profile(advocate, validated_data):
    """
    Update advocate profile and send notifications
    """
    for key, value in validated_data.items():
        setattr(advocate, key, value)
    advocate.save()

    # Notify the advocate
    user = advocate.user
    if user.email:
        send_mail(
            "Advocate Profile Updated ✅",
            f"Hi {user.username}, your advocate profile has been updated successfully!",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )
    if hasattr(user, "phone") and user.phone:
        send_sms(user.phone, "Your advocate profile has been updated successfully ✅")

    return advocate


def verify_advocate(advocate, admin_user=None):
    """
    Admin verifies advocate profile
    """
    advocate.is_verified = True
    advocate.verified_at = timezone.now()
    if admin_user:
        advocate.verified_by = admin_user
    advocate.save()

    # Notify the advocate
    user = advocate.user
    if user.email:
        send_mail(
            "Your Advocate Profile is Verified ✅",
            f"Hi {user.username}, your advocate profile has been verified by admin.",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )
    if hasattr(user, "phone") and user.phone:
        send_sms(user.phone, "Your advocate profile is now verified ✅")

    return advocate


# ======================================================
# ASSISTANT LAWYER SERVICES
# ======================================================

def assign_assistant(advocate, assistant_user_id):
    """
    Assign assistant lawyer to advocate
    """
    assistant_user = get_object_or_404(User, id=assistant_user_id)

    if hasattr(assistant_user, "assistant_profile"):
        raise ValueError("User is already assigned as assistant")

    assistant = AssistantLawyer.objects.create(advocate=advocate, user=assistant_user)

    # Notify the assistant
    if assistant_user.email:
        send_mail(
            "You have been assigned as Assistant Lawyer ✅",
            f"Hi {assistant_user.username}, you have been assigned as assistant to Advocate {advocate.user.username}.",
            settings.DEFAULT_FROM_EMAIL,
            [assistant_user.email],
        )
    if hasattr(assistant_user, "phone") and assistant_user.phone:
        send_sms(
            assistant_user.phone,
            f"You are now assistant of Advocate {advocate.user.username} ✅",
        )

    return assistant


def list_assistants(advocate):
    """
    List all active assistants for an advocate
    """
    return advocate.assistants.filter(is_active=True)
