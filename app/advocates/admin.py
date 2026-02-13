from django.contrib import admin
from .models import AdvocateProfile, AssistantLawyer


# -----------------------------
# AdvocateProfile Admin
# -----------------------------
@admin.register(AdvocateProfile)
class AdvocateProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "specialization",
        "experience_years",
        "bar_council_id",
        "consultation_fee",
        "is_verified",
        "created_at",
    )

    list_filter = (
        "specialization",
        "is_verified",
        "experience_years",
       
    )

    search_fields = (
        "user__username",
        "user__email",
        "bar_council_id",
         "languages_spoken",
    )

    ordering = (
        "-is_verified",
        "-experience_years",
        "user__username",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "verified_at",
        "verified_by",
    )

    fieldsets = (
        (
            "Advocate Details",
            {
                "fields": (
                    "user",
                    "profile_photo",
                    "specialization",
                    "experience_years",
                    "bar_council_id",
                    "consultation_fee",
                     "languages_spoken",
                    "bio",
                    "official_id_card",
                )
            },
        ),
        (
            "Verification",
            {
                "fields": (
                    "is_verified",
                    "verified_at",
                    "verified_by",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


# -----------------------------
# AssistantLawyer Admin
# -----------------------------
@admin.register(AssistantLawyer)
class AssistantLawyerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "advocate",
        "assigned_at",
        "is_active",
    )

    list_filter = (
        "is_active",
        "advocate",
    )

    search_fields = (
        "user__username",
        "user__email",
        "advocate__user__username",
    )

    ordering = ("-assigned_at",)

    readonly_fields = ("assigned_at",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "advocate",
                    "user",
                    "is_active",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("assigned_at",)
            },
        ),
    )
