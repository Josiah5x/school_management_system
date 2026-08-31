from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "role",
        "is_active",
        "is_verified",
    )

    list_filter = (
        "role",
        "is_active",
        "is_verified",
        "is_staff",
    )

    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "staff_id",
        "phone",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "School Information",
            {
                "fields": (
                    "role",
                    "staff_id",
                    "phone",
                    "profile_photo",
                    "address",
                    "date_of_birth",
                    "is_verified",
                ),
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "School Information",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "role",
                    "phone",
                    "staff_id",
                ),
            },
        ),
    )