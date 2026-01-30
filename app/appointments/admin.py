from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    # ----------------------------------
    # List View
    # ----------------------------------
    list_display = ('id','client','advocate','appointment_date','appointment_time',
        'duration_minutes','status','is_active','created_at')

    list_filter = ('status','is_active','appointment_date','advocate')

    search_fields = ('client__user__username','client__user__email','advocate__user__username',
        'advocate__user__email','problem_description')

    ordering = ('-created_at',)

    # ----------------------------------
    # Read-only Fields
    # ----------------------------------
    readonly_fields = ('created_at', 'updated_at',)

    # ----------------------------------
    # Form Layout
    # ----------------------------------
    fieldsets = (
        ('Appointment Info', {
            'fields': ('client','advocate','appointment_date','appointment_time',
                'duration_minutes','status','is_active',)
        }),
        ('Client Details', {
            'fields': ('problem_description', 'remarks')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    # ----------------------------------
    # Admin UX Improvements
    # ----------------------------------
    list_per_page = 25
    date_hierarchy = 'appointment_date'
