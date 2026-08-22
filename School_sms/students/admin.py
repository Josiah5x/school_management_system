from django.contrib import admin

from .models import (
    Enrollment,
    Guardian,
    Student,
    StudentAddress,
)


@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "relationship",
        "phone",
        "email",
        "is_primary",
    )

    list_filter = (
        "relationship",
        "is_primary",
    )

    search_fields = (
        "first_name",
        "last_name",
        "phone",
        "email",
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "admission_number",
        "full_name",
        "gender",
        "status",
        "admission_date",
    )

    list_filter = (
        "gender",
        "status",
    )

    search_fields = (
        "admission_number",
        "first_name",
        "middle_name",
        "last_name",
    )

    filter_horizontal = (
        "guardians",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(StudentAddress)
class StudentAddressAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "city",
        "state",
        "lga",
    )

    search_fields = (
        "student__admission_number",
        "student__first_name",
        "student__last_name",
        "city",
        "state",
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "session",
        "class_arm",
        "roll_number",
        "status",
        "is_current",
    )

    list_filter = (
        "session",
        "status",
        "is_current",
        "class_arm",
    )

    search_fields = (
        "student__admission_number",
        "student__first_name",
        "student__last_name",
    )