from django import forms

from .models import (
    Enrollment,
    Guardian,
    Student,
    StudentGuardian
)


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student

        fields = [
            "school",
            "admission_number",
            "first_name",
            "middle_name",
            "last_name",
            "gender",
            "date_of_birth",
            "birth_place",
            "nationality",
            "state_of_origin",
            "lga_of_origin",
            "address",
            "phone",
            "email",
            "photo",
            "is_active",
        ]

        widgets = {
            "school": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "admission_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ADM/2026/001",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "middle_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "gender": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "date_of_birth": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "birth_place": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "nationality": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "state_of_origin": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "lga_of_origin": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "photo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

class BootstrapFormMixin:
    """
    Automatically applies Bootstrap 5 classes to form fields.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            widget = field.widget

            if isinstance(
                widget,
                forms.CheckboxInput,
            ):
                widget.attrs["class"] = "form-check-input"

            elif isinstance(
                widget,
                (
                    forms.Select,
                    forms.SelectMultiple,
                ),
            ):
                widget.attrs["class"] = "form-select"

            else:
                widget.attrs["class"] = "form-control"


class GuardianForm(
    BootstrapFormMixin,
    forms.ModelForm,
):
    class Meta:
        model = Guardian

        fields = [
            "school",
            "first_name",
            "last_name",
            "phone",
            "alternative_phone",
            "email",
            "address",
            "occupation",
            "relationship",
            "is_active",
        ]

        widgets = {
            "school": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "First name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "placeholder": "Last name",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "080XXXXXXXX",
                }
            ),
            "alternative_phone": forms.TextInput(
                attrs={
                    "placeholder": "Alternative phone",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "guardian@example.com",
                }
            ),
            "address": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Residential address",
                }
            ),
            "occupation": forms.TextInput(
                attrs={
                    "placeholder": "Occupation",
                }
            ),
            "relationship": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }


class StudentGuardianForm(
    BootstrapFormMixin,
    forms.ModelForm,
):
    class Meta:
        model = StudentGuardian

        fields = [
            "guardian",
            "relationship",
            "is_primary",
            "can_pickup",
        ]

        widgets = {
            "guardian": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "relationship": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "is_primary": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "can_pickup": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

class EnrollmentForm(forms.ModelForm):

    class Meta:
        model = Enrollment

        fields = [
            "student",
            "session",
            "academic_class",
            "class_arm",
            "admission_date",
            "status",
            "is_boarding",
            "boarding_house",
            "remark",
        ]

        widgets = {
            "student": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "session": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "academic_class": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "class_arm": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "admission_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "is_boarding": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "boarding_house": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "remark": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
        }