from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    # =========================
    # LIST VIEW
    # =========================
    list_display = (
        'id',
        'username',
        'first_name',
        'middle_name',
        'last_name',
        'email',
        'role',
        'is_active',
        'is_staff'
    )

    list_filter = (
        'role',
        'is_staff',
        'is_active',
    )

    search_fields = (
        'username',
        'first_name',
        'middle_name',
        'last_name',
        'email',
        'phone'
    )

    ordering = ('id',)

    # =========================
    # DETAIL / EDIT VIEW
    # =========================
    fieldsets = (
        (None, {
            'fields': (
                'username',
                'password'
            )
        }),
        ('Personal Information', {
            'fields': (
                'first_name',
                'middle_name',
                'last_name',
                'email',
                'phone',
                'address',
                'role',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Important Dates', {
            'fields': (
                'last_login',
                'date_joined',
            )
        }),
    )

    readonly_fields = (
        'last_login',
        'date_joined',
    )

    # =========================
    # ADD USER FORM (ADMIN)
    # =========================
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'first_name',
                'middle_name',
                'last_name',
                'email',
                'phone',
                'address',
                'role',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )
