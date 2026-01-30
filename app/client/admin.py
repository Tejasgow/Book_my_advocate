from django.contrib import admin
from .models import ClientProfile


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    # -----------------------------
    # List View
    # -----------------------------
    list_display = (
        'id',
        'user',
        'phone',
        'is_verified',
        'created_at',
    )

    list_filter = (
        'is_verified',
        'created_at',
    )

    search_fields = (
        'user__username',
        'user__email',
        'phone',
    )

    ordering = ('-created_at',)

    # -----------------------------
    # Detail View
    # -----------------------------
    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fieldsets = (
        ('User Info', {
            'fields': ('user',)
        }),
        ('Client Details', {
            'fields': (
                'phone',
                'address',
                'is_verified',
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )
