from django import forms

from .models import AcademicSession
from .models import Term


class BootstrapFormMixin:
    """Apply Bootstrap classes to form widgets."""

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

            else:
                widget.attrs.setdefault(
                    "class",
                    "form-control",
                )


class AcademicSessionForm(
    BootstrapFormMixin,
    forms.ModelForm,
):
    """Form for creating and editing academic sessions."""

    class Meta:
        model = AcademicSession

        fields = [
            "school",
            "name",
            "start_date",
            "end_date",
            "is_current",
        ]

        widgets = {
            "school": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Example: 2026/2027",
                }
            ),
            "start_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "end_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }

        labels = {
            "school": "School",
            "name": "Academic Session",
            "start_date": "Session Start Date",
            "end_date": "Session End Date",
            "is_current": "Current Session",
        }

        help_texts = {
            "name": "Example: 2026/2027",
            "is_current": (
                "Set this as the active academic session."
            ),
        }


class TermForm(
    BootstrapFormMixin,
    forms.ModelForm,
):
    """Form for creating and editing academic terms."""

    class Meta:
        model = Term

        fields = [
            "session",
            "term",
            "start_date",
            "end_date",
            "next_term_resumption_date",
            "is_current",
            "result_published",
        ]

        widgets = {
            "session": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "term": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "start_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "end_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "next_term_resumption_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }

        labels = {
            "session": "Academic Session",
            "term": "Term",
            "start_date": "Term Start Date",
            "end_date": "Term End Date",
            "next_term_resumption_date": (
                "Next Term Resumption Date"
            ),
            "is_current": "Current Term",
            "result_published": "Results Published",
        }

from django import forms

from .models import AcademicClass
from .models import ClassArm
from .models import Subject


class BootstrapFormMixin:
    """Apply Bootstrap classes to form widgets."""

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

            else:
                widget.attrs.setdefault(
                    "class",
                    "form-control",
                )


class AcademicClassForm(
    BootstrapFormMixin,
    forms.ModelForm,
):
    """Create and update an academic class."""

    class Meta:
        model = AcademicClass

        fields = [
            "school",
            "name",
            "tier",
            "level",
            "department",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Example: JSS 1",
                }
            ),
            "level": forms.NumberInput(
                attrs={
                    "min": 1,
                    "max": 10,
                    "placeholder": "Enter class level",
                }
            ),
        }

        labels = {
            "school": "School",
            "name": "Class Name",
            "tier": "School Tier",
            "level": "Level",
            "department": "Department",
            "is_active": "Active",
        }

    def clean(self):
        cleaned_data = super().clean()

        tier = cleaned_data.get("tier")
        level = cleaned_data.get("level")
        department = cleaned_data.get("department")

        if tier and level:
            if tier == "nursery" and not 1 <= level <= 3:
                self.add_error(
                    "level",
                    "Nursery level must be between 1 and 3.",
                )

            elif tier == "primary" and not 1 <= level <= 6:
                self.add_error(
                    "level",
                    "Primary level must be between 1 and 6.",
                )

            elif tier == "jss" and not 1 <= level <= 3:
                self.add_error(
                    "level",
                    "JSS level must be between 1 and 3.",
                )

            elif tier == "sss" and not 1 <= level <= 3:
                self.add_error(
                    "level",
                    "SSS level must be between 1 and 3.",
                )

        if tier == "sss" and not department:
            self.add_error(
                "department",
                "SSS classes must have a department.",
            )

        if tier != "sss" and department:
            self.add_error(
                "department",
                "Only SSS classes can have a department.",
            )

        return cleaned_data


class ClassArmForm(
    BootstrapFormMixin,
    forms.ModelForm,
):
    """Create and update a class arm."""

    class Meta:
        model = ClassArm

        fields = [
            "academic_class",
            "name",
            "form_teacher",
            "capacity",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Example: A",
                }
            ),
            "capacity": forms.NumberInput(
                attrs={
                    "min": 1,
                    "max": 200,
                }
            ),
        }

        labels = {
            "academic_class": "Academic Class",
            "name": "Arm",
            "form_teacher": "Form Teacher",
            "capacity": "Student Capacity",
            "is_active": "Active",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["form_teacher"].queryset = (
            self.fields["form_teacher"]
            .queryset
            .filter(is_active=True)
        )


class SubjectForm(
    BootstrapFormMixin,
    forms.ModelForm,
):
    """Create and update a subject."""

    class Meta:
        model = Subject

        fields = [
            "name",
            "code",
            "description",
            "is_core",
            "is_practical",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Example: Mathematics",
                }
            ),
            "code": forms.TextInput(
                attrs={
                    "placeholder": "Example: MATH",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": (
                        "Describe the subject..."
                    ),
                }
            ),
        }

        labels = {
            "name": "Subject Name",
            "code": "Subject Code",
            "description": "Description",
            "is_core": "Core Subject",
            "is_practical": "Practical Subject",
            "is_active": "Active",
        }

    def clean_code(self):
        code = self.cleaned_data["code"]

        return code.strip().upper()


##########################################

from django import forms

from .models import (
    AcademicClass,
    ClassArm,
    ClassSubject,
    Subject,
    TeacherSubjectAssignment,
)


class ClassSubjectForm(forms.ModelForm):
    """Assign a subject to an academic class."""

    class Meta:
        model = ClassSubject

        fields = [
            "academic_class",
            "subject",
            "is_compulsory",
            "maximum_score",
            "display_order",
        ]

        widgets = {
            "academic_class": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "subject": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "is_compulsory": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "maximum_score": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                    "step": "0.01",
                }
            ),
            "display_order": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["academic_class"].queryset = (
            AcademicClass.objects
            .select_related("school")
            .filter(is_active=True)
        )

        self.fields["subject"].queryset = (
            Subject.objects
            .filter(is_active=True)
            .order_by("name")
        )

    def clean_maximum_score(self):
        maximum_score = self.cleaned_data["maximum_score"]

        if maximum_score <= 0:
            raise forms.ValidationError(
                "Maximum score must be greater than zero."
            )

        return maximum_score


class TeacherSubjectAssignmentForm(forms.ModelForm):
    """Assign a teacher to a subject and class arm."""

    class Meta:
        model = TeacherSubjectAssignment

        fields = [
            "teacher",
            "class_arm",
            "subject",
            "session",
            "is_class_teacher",
            "is_active",
        ]

        widgets = {
            "teacher": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "class_arm": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "subject": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "session": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "is_class_teacher": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["teacher"].queryset = (
            self.fields["teacher"]
            .queryset
            .filter(
                role__in=[
                    "teacher",
                    "hod",
                    "principal",
                    "vice_principal",
                ],
                is_active=True,
            )
            .order_by("first_name", "last_name")
        )

        self.fields["class_arm"].queryset = (
            ClassArm.objects
            .select_related("academic_class")
            .filter(is_active=True)
            .order_by(
                "academic_class__name",
                "name",
            )
        )

        self.fields["subject"].queryset = (
            Subject.objects
            .filter(is_active=True)
            .order_by("name")
        )

        self.fields["session"].queryset = (
            self.fields["session"]
            .queryset
            .order_by("-start_date")
        )

    def clean(self):
        cleaned_data = super().clean()

        class_arm = cleaned_data.get("class_arm")
        subject = cleaned_data.get("subject")

        if class_arm and subject:

            exists = ClassSubject.objects.filter(
                academic_class=class_arm.academic_class,
                subject=subject,
            ).exists()

            if not exists:
                raise forms.ValidationError(
                    (
                        f"{subject.name} is not assigned to "
                        f"{class_arm.academic_class.name}."
                    )
                )

        return cleaned_data