from django import forms

from .models import School, SchoolSettings


class BootstrapFormMixin:
    """Apply Bootstrap classes to Django form widgets."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            widget = field.widget

            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault(
                    "class",
                    "form-check-input",
                )

            elif isinstance(widget, forms.Select):
                widget.attrs.setdefault(
                    "class",
                    "form-select",
                )

            elif isinstance(widget, forms.Textarea):
                widget.attrs.setdefault(
                    "class",
                    "form-control",
                )
                widget.attrs.setdefault(
                    "rows",
                    3,
                )

            else:
                widget.attrs.setdefault(
                    "class",
                    "form-control",
                )


class SchoolForm(BootstrapFormMixin, forms.ModelForm):
    """Create and update school information."""

    class Meta:
        model = School

        fields = [
            "name",
            "short_name",
            "address",
            "phone",
            "email",
            "website",
            "logo",
            "motto",
            "principal_name",
            "principal_signature",
            "principal_stamp",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Enter full school name",
                }
            ),
            "short_name": forms.TextInput(
                attrs={
                    "placeholder": "e.g. GSS",
                }
            ),
            "address": forms.Textarea(
                attrs={
                    "placeholder": "School address",
                    "rows": 3,
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "e.g. 08012345678",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "school@example.com",
                }
            ),
            "website": forms.URLInput(
                attrs={
                    "placeholder": "https://www.example.com",
                }
            ),
            "motto": forms.TextInput(
                attrs={
                    "placeholder": "School motto",
                }
            ),
            "principal_name": forms.TextInput(
                attrs={
                    "placeholder": "Principal's full name",
                }
            ),
            "logo": forms.ClearableFileInput(
                attrs={
                    "accept": "image/*",
                }
            ),
            "principal_signature": forms.ClearableFileInput(
                attrs={
                    "accept": "image/*",
                }
            ),
            "principal_stamp": forms.ClearableFileInput(
                attrs={
                    "accept": "image/*",
                }
            ),
        }

        labels = {
            "name": "School Name",
            "short_name": "Short Name",
            "address": "School Address",
            "phone": "Phone Number",
            "email": "Email Address",
            "website": "Website",
            "logo": "School Logo",
            "motto": "School Motto",
            "principal_name": "Principal Name",
            "principal_signature": "Principal Signature",
            "principal_stamp": "Principal Stamp",
            "is_active": "School is Active",
        }

        help_texts = {
            "logo": (
                "Recommended: PNG or JPG with a square or "
                "transparent background."
            ),
            "principal_signature": (
                "Upload the principal's signature for report cards."
            ),
            "principal_stamp": (
                "Upload the official school/principal stamp."
            ),
        }


class SchoolSettingsForm(
    BootstrapFormMixin,
    forms.ModelForm,
):
    """Configure school academic and result settings."""

    class Meta:
        model = SchoolSettings

        fields = [
            "country",
            "state",
            "lga",
            "currency",
            "grading_enabled",
            "result_position_enabled",
            "show_class_average",
            "show_student_average",
            "show_affective_domain",
            "show_psychomotor_domain",
        ]

        widgets = {
            "country": forms.TextInput(
                attrs={
                    "placeholder": "Country",
                }
            ),
            "state": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Nasarawa",
                }
            ),
            "lga": forms.TextInput(
                attrs={
                    "placeholder": "Local Government Area",
                }
            ),
            "currency": forms.TextInput(
                attrs={
                    "placeholder": "NGN",
                }
            ),
        }

        labels = {
            "country": "Country",
            "state": "State",
            "lga": "LGA",
            "currency": "Currency",
            "grading_enabled": "Enable Grading",
            "result_position_enabled": (
                "Enable Result Position"
            ),
            "show_class_average": (
                "Show Class Average"
            ),
            "show_student_average": (
                "Show Student Average"
            ),
            "show_affective_domain": (
                "Show Affective Domain"
            ),
            "show_psychomotor_domain": (
                "Show Psychomotor Domain"
            ),
        }