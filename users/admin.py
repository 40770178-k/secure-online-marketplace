from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for CustomUser.

    We extend Django's UserAdmin instead of reinventing the wheel.
    This gives us secure password handling, permissions, and groups
    out of the box.
    """

    model = CustomUser

    # What columns are visible in the admin user list
    list_display = (
        'username',
        'email',
        'role',
        'is_staff',
        'is_superuser',
        'is_active',
    )

    # Enables filtering users by power level
    list_filter = (
        'role',
        'is_staff',
        'is_superuser',
        'is_active',
    )

    # Default ordering in admin list view
    ordering = ('username',)

    def get_readonly_fields(self, request, obj=None):
        """
        Prevent privilege escalation.

        Non-superusers MUST NOT be able to:
        - Change roles
        - Grant staff/superuser status
        - Modify groups or permissions

        Only superusers control power.
        """
        if not request.user.is_superuser:
            return (
                'role',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        return ()

    def save_model(self, request, obj, form, change):

        if obj.is_superuser:
            obj.role = 'admin'
        elif obj.is_staff:
            obj.role = 'staff'
        else:
            obj.role = 'user'

        super().save_model(request, obj, form, change)
