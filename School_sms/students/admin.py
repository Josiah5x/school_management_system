from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Student, Guardian, StudentGuardian, Enrollment


class StudentGuardianInline(admin.TabularInline):
    """Allows linking guardians directly on the Student detail screen."""
    model = StudentGuardian
    extra = 1
    autocomplete_fields = ["guardian"]


class EnrollmentInline(admin.TabularInline):

    """Allows tracking or creating class placement history inside the Student profile."""
    model = Enrollment
    extra = 0
    raw_id_fields = ["session", "academic_class", "class_arm"]


class PrimaryGuardianFormSet(BaseInlineFormSet):

    """Validates that a student has no more than one primary guardian assigned."""
    def clean(self):
        super().clean()
        primary_count = 0
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_primary'):
                    primary_count += 1
        if primary_count > 1:
            raise ValidationError("A student can only have one primary guardian assigned.")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        "admission_number", 
        "last_name", 
        "first_name", 
        "gender", 
        "school", 
        "is_active"
    ]

    list_filter = ["school", "gender", "is_active", "state_of_origin"]
    search_fields = ["admission_number", "first_name", "last_name", "phone", "email"]
    ordering = ["last_name", "first_name"]
    inlines = [StudentGuardianInline, EnrollmentInline]
    
    fieldsets = [
        ("Institutional Metadata", {
            "fields": ["school", "admission_number", "is_active"]
        }),
        ("Personal Bio Information", {
            "fields": [
                ("first_name", "middle_name", "last_name"),
                ("gender", "date_of_birth"),
                "photo"
            ]
        }),
        ("Demographics & Origin", {
            "fields": [("nationality", "state_of_origin", "lga_of_origin"), "birth_place"]
        }),
        ("Contact Metrics", {
            "fields": [("phone", "email"), "address"]
        }),
    ]


@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = ["full_name", "phone", "relationship", "school", "is_active"]
    list_filter = ["school", "relationship", "is_active"]
    search_fields = ["first_name", "last_name", "phone", "email"]
    ordering = ["last_name", "first_name"]
    inlines = [StudentGuardianInline]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ["student", "academic_class", "class_arm", "session", "status", "is_boarding"]
    list_filter = ["session", "academic_class", "status", "is_boarding"]
    search_fields = [
        "student__first_name", 
        "student__last_name", 
        "student__admission_number"
    ]
    autocomplete_fields = ["student"]

    def save_model(self, request, obj, form, change):
        """Triggers model clean() checks explicitly when modified through admin actions."""
        try:
            obj.clean()
        except ValidationError as e:
            form.add_error(None, e)
            return
        super().save_model(request, obj, form, change)


# @admin.register(StudentAddress)
# class StudentAddressAdmin(admin.ModelAdmin):
#     list_display = (
#         "studentss",
#         "city",
#         "state",
#         "lga",
#     )

#     search_fields = (
#         "student__admission_number",
#         "student__first_name",
#         "student__last_name",
#         "city",
#         "state",
#     )

