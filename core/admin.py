from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("추가 정보", {
            "fields": ("full_name", "user_type", "status", "is_deleted")

        }),
    )
    readonly_fields = ("updated_at", "created_at")
    list_display = ("username", "full_name", "user_type", "status", "is_active", "is_deleted")
    list_filter = ("user_type", "status", "is_active", "is_deleted")
