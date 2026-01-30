from django.contrib import admin
from .models import AdvocateProfile, AssistantLawyer

# -----------------------------
# AdvocateProfile Admin
# -----------------------------
@admin.register(AdvocateProfile)
class AdvocateProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'specialization', 'experience_years', 
        'bar_council_id', 'consultation_fee', 'verified', 'created_at'
    )
    list_filter = ('specialization', 'verified', 'experience_years')
    search_fields = ('user__username', 'bar_council_id', 'user__email')
    ordering = ('-verified', '-experience_years', 'user__username')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {'fields': ('user', 'specialization', 'experience_years', 'bar_council_id', 'consultation_fee')}),
        ('Verification', {'fields': ('verified',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

# -----------------------------
# AssistantLawyer Admin
# -----------------------------
@admin.register(AssistantLawyer)
class AssistantLawyerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'advocate', 'assigned_at', 'is_active')
    list_filter = ('is_active', 'advocate')
    search_fields = ('user__username', 'advocate__user__username', 'user__email')
    ordering = ('-assigned_at',)
    readonly_fields = ('assigned_at',)

    fieldsets = (
        (None, {'fields': ('advocate', 'user', 'is_active')}),
        ('Timestamps', {'fields': ('assigned_at',)}),
    )
