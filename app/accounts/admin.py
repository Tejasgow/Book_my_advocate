from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    model = User

    # Fields to display in the admin user list
    list_display = (
        'id',
        'username',
        'email',
        'role',
        'is_active',
        'is_staff',
        'is_superuser'
    )

    # Filters in the right sidebar
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')

    # Search fields
    search_fields = ('username', 'email', 'role')

    # Ordering by ID
    ordering = ('id',)

    # Fields shown when editing a user
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('role', 'phone', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields shown when adding a new user via admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2', 
                'role', 'phone', 'address',
                'is_active', 'is_staff', 'is_superuser'
            )
        }),
    )


# Register the User model with custom admin
admin.site.register(User, UserAdmin)
