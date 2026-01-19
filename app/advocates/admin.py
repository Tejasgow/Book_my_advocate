from django.contrib import admin
from .models import AdvocateProfile


@admin.register(AdvocateProfile)
class AdvocateProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'specialization',
        'experience_years',
        'consultation_fee',
        'verified',
        'created_at'
    )

    list_filter = ('verified', 'specialization')
    search_fields = ('user__username', 'bar_council_id')
    ordering = ('-created_at',)

    actions = ['mark_as_verified', 'mark_as_unverified']

    @admin.action(description="Mark selected advocates as VERIFIED")
    def mark_as_verified(self, request, queryset):
        queryset.update(verified=True)

    @admin.action(description="Mark selected advocates as UNVERIFIED")
    def mark_as_unverified(self, request, queryset):
        queryset.update(verified=False)
