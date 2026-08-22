from django.contrib import admin

from .models import (
    AcademicClass,
    AcademicSession,
    ClassArm,
    ClassSubject,
    Subject,
    TeacherSubjectAssignment,
    Term,
)


@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "school",
        "start_date",
        "end_date",
        "is_current",
    )

    list_filter = (
        "is_current",
    )

    search_fields = (
        "name",
        "school__name",
    )


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = (
        "session",
        "term",
        "start_date",
        "end_date",
        "is_current",
        "result_published",
    )

    list_filter = (
        "term",
        "is_current",
        "result_published",
    )


@admin.register(AcademicClass)
class AcademicClassAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "tier",
        "level",
        "department",
        "school",
        "is_active",
    )

    list_filter = (
        "tier",
        "department",
        "is_active",
    )

    search_fields = (
        "name",
        "school__name",
    )


@admin.register(ClassArm)
class ClassArmAdmin(admin.ModelAdmin):
    list_display = (
        "academic_class",
        "name",
        "form_teacher",
        "capacity",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "academic_class__name",
        "name",
        "form_teacher__username",
    )


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "is_core",
        "is_practical",
        "is_active",
    )

    list_filter = (
        "is_core",
        "is_practical",
        "is_active",
    )

    search_fields = (
        "code",
        "name",
    )


@admin.register(ClassSubject)
class ClassSubjectAdmin(admin.ModelAdmin):
    list_display = (
        "academic_class",
        "subject",
        "is_compulsory",
        "maximum_score",
        "display_order",
    )

    list_filter = (
        "is_compulsory",
    )

    search_fields = (
        "academic_class__name",
        "subject__name",
        "subject__code",
    )


@admin.register(TeacherSubjectAssignment)
class TeacherSubjectAssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "teacher",
        "class_arm",
        "subject",
        "session",
        "is_class_teacher",
        "is_active",
    )

    list_filter = (
        "is_class_teacher",
        "is_active",
        "session",
    )

    search_fields = (
        "teacher__username",
        "teacher__first_name",
        "teacher__last_name",
        "subject__name",
        "class_arm__name",
    )


