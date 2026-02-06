from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    ordering = ('username',)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ('role',)
        return ()

    def save_model(self, request, obj, form, change):
        if obj.is_superuser:
            obj.role = 'admin'
        super().save_model(request, obj, form, change)
