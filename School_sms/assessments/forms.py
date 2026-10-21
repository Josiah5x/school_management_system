from django import forms

from .models import (
    AssessmentComponent,
    AssessmentScheme,
    AssessmentSchemeComponent,
    AssessmentTrait,
    GradeScale,
    GradeScaleItem,
    StudentAssessment,
    StudentTraitAssessment,
)


class BootstrapMixin:
    """
    Automatically applies Bootstrap 5 classes to form widgets.
    """

    def apply_bootstrap(self):
        for field in self.fields.values():
            widget = field.widget

            if isinstance(widget, forms.CheckboxInput):
                widget.attrs["class"] = "form-check-input"

            elif isinstance(widget, forms.Select):
                widget.attrs["class"] = "form-select"

            elif isinstance(widget, forms.Textarea):
                widget.attrs["class"] = "form-control"
                widget.attrs.setdefault("rows", 3)

            else:
                existing = widget.attrs.get("class", "")
                widget.attrs["class"] = (
                    f"{existing} form-control"
                ).strip()


class AssessmentComponentForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = AssessmentComponent
        fields = [
            "name",
            "code",
            "component_type",
            "maximum_score",
            "display_order",
            "is_active",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()


class AssessmentSchemeForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = AssessmentScheme
        fields = [
            "name",
            "scheme_type",
            "maximum_total",
            "is_default",
            "is_active",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()

        self.fields["maximum_total"].widget.attrs[
            "readonly"
        ] = True


class AssessmentSchemeComponentForm(forms.ModelForm):
    class Meta:
        model = AssessmentSchemeComponent
        fields = [
            "component",
            "maximum_score",
            "display_order",
        ]

        widgets = {
            "component": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "maximum_score": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "max": "100",
                }
            ),
            "display_order": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                }
            ),
        }


class StudentAssessmentForm(
    BootstrapMixin,
    forms.ModelForm,
):
    class Meta:
        model = StudentAssessment
        fields = [
            "student",
            "enrollment",
            "term",
            "class_subject",
            "assessment_scheme",
            "component",
            "score",
            "approved",
        ]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

        self.fields["student"].queryset = (
            self.fields["student"].queryset
            .select_related()
        )

        self.fields["enrollment"].queryset = (
            self.fields["enrollment"].queryset
            .select_related("student", "session")
        )

        self.fields["term"].queryset = (
            self.fields["term"].queryset
            .select_related("session")
        )

        self.fields["class_subject"].queryset = (
            self.fields["class_subject"].queryset
            .select_related(
                "academic_class",
                "subject",
            )
        )

        self.fields["component"].queryset = (
            self.fields["component"].queryset
            .select_related(
                "scheme",
                "component",
            )
        )

        self.apply_bootstrap()

    def clean(self):
        cleaned_data = super().clean()

        score = cleaned_data.get("score")
        component = cleaned_data.get("component")

        if score is not None and component:
            if score < 0:
                self.add_error(
                    "score",
                    "Score cannot be negative.",
                )

            elif score > component.maximum_score:
                self.add_error(
                    "score",
                    (
                        "Score cannot exceed "
                        f"{component.maximum_score}."
                    ),
                )

        return cleaned_data


class AssessmentTraitForm(
    BootstrapMixin,
    forms.ModelForm,
):
    class Meta:
        model = AssessmentTrait
        fields = [
            "name",
            "code",
            "category",
            "description",
            "display_order",
            "is_active",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()


class StudentTraitAssessmentForm(
    BootstrapMixin,
    forms.ModelForm,
):
    class Meta:
        model = StudentTraitAssessment
        fields = [
            "student",
            "enrollment",
            "term",
            "trait",
            "rating",
            "teacher_comment",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["trait"].queryset = (
            AssessmentTrait.objects.filter(
                is_active=True
            )
        )

        self.fields["rating"].widget = forms.Select(
            choices=[
                (1, "1 - Poor"),
                (2, "2 - Fair"),
                (3, "3 - Good"),
                (4, "4 - Very Good"),
                (5, "5 - Excellent"),
            ],
            attrs={
                "class": "form-select",
            },
        )

        self.apply_bootstrap()


class GradeScaleForm(
    BootstrapMixin,
    forms.ModelForm,
):
    class Meta:
        model = GradeScale
        fields = [
            "name",
            "code",
            "description",
            "is_active",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()


class GradeScaleItemForm(
    BootstrapMixin,
    forms.ModelForm,
):
    class Meta:
        model = GradeScaleItem
        fields = [
            "grade_scale",
            "grade",
            "min_score",
            "max_score",
            "grade_point",
            "remark",
            "display_order",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["grade_scale"].queryset = (
            GradeScale.objects.filter(
                is_active=True
            )
        )

        self.apply_bootstrap()