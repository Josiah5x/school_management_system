from django.contrib import admin

from .models import (
    AssessmentComponent,
    AssessmentScheme,
    AssessmentSchemeComponent,
    AssessmentTrait,
    GradeScale,
    GradeScaleItem,
    StudentAssessment,
    StudentTraitAssessment,
    SubjectResult,
    TermResult,
)


@admin.register(AssessmentTrait)
class AssessmentTraitAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "category",
        "display_order",
        "is_active",
    )

    list_filter = (
        "category",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
    )


@admin.register(StudentTraitAssessment)
class StudentTraitAssessmentAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "term",
        "trait",
        "rating",
        "assessed_by",
    )

    list_filter = (
        "term",
        "trait__category",
        "rating",
    )

    search_fields = (
        "student__admission_number",
        "student__first_name",
        "student__last_name",
        "trait__name",
    )


########################################
@admin.register(TermResult)
class TermResultAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "term",
        "average_score",
        "position",
        "class_average",
        "is_published",
    )

    list_filter = (
        "term",
        "is_published",
    )

    search_fields = (
        "student__admission_number",
        "student__first_name",
        "student__last_name",
    )