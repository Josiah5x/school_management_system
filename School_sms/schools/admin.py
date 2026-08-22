from django.contrib import admin

from .models import School, SchoolSettings


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "short_name",
        "phone",
        "email",
        "is_active",
    )

    search_fields = (
        "name",
        "short_name",
        "email",
    )


@admin.register(SchoolSettings)
class SchoolSettingsAdmin(admin.ModelAdmin):
    list_display = (
        "school",
        "country",
        "state",
        "currency",
    )

    list_filter = (
        "country",
        "currency",
    )