from decimal import Decimal
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.
class AssessmentComponent(models.Model):

    class ComponentType(models.TextChoices):
        CA1 = "ca1", "Continuous Assessment 1"
        CA2 = "ca2", "Continuous Assessment 2"
        CA = "ca", "Continuous Assessment"
        EXAM = "exam", "Terminal Examination"
        PRACTICAL = "practical", "Practical"
        PROJECT = "project", "Project"

    name = models.CharField(max_length=100)

    code = models.CharField(max_length=20, unique=True)

    component_type = models.CharField(max_length=20, choices=ComponentType.choices)

    maximum_score = models.DecimalField(max_digits=5, decimal_places=2)

    display_order = models.PositiveSmallIntegerField(default=1)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


#################################


class AssessmentScheme(models.Model):

    class SchemeType(models.TextChoices):
        CA_EXAM = "ca_exam", "CA + Examination"
        CA1_CA2_EXAM = (
            "ca1_ca2_exam",
            "CA1 + CA2 + Examination",
        )
        CA_EXAM_PRACTICAL = (
            "ca_exam_practical",
            "CA + Examination + Practical",
        )

    name = models.CharField(
        max_length=100,
    )

    scheme_type = models.CharField(
        max_length=30,
        choices=SchemeType.choices,
    )

    maximum_total = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("100.00"),
    )

    is_default = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def clean(self):
        if self.maximum_total != Decimal("100.00"):
            raise ValidationError(
                "The Nigerian result engine must " "use a 100-point total."
            )

    def __str__(self):
        return self.name


##########################################


class AssessmentSchemeComponent(models.Model):
    scheme = models.ForeignKey(
        AssessmentScheme,
        on_delete=models.CASCADE,
        related_name="components",
    )

    component = models.ForeignKey(
        AssessmentComponent,
        on_delete=models.PROTECT,
        related_name="scheme_components",
    )

    maximum_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    display_order = models.PositiveSmallIntegerField(
        default=1,
    )

    class Meta:
        ordering = [
            "display_order",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "scheme",
                    "component",
                ],
                name="unique_scheme_component",
            ),
        ]

    def clean(self):
        if self.maximum_total != Decimal("100.00"):
            raise ValidationError(
                "The Nigerian result engine must " "use a 100-point total."
            )

        if self.pk:
            total = sum(component.maximum_score for component in self.components.all())

            if total != Decimal("100.00"):
                raise ValidationError("Assessment components must total 100 marks.")

    def __str__(self):
        return f"{self.scheme.name} - " f"{self.component.name}"


########################################


class StudentAssessment(models.Model):
    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="assessments",
    )

    enrollment = models.ForeignKey(
        "students.Enrollment",
        on_delete=models.PROTECT,
        related_name="assessments",
    )

    term = models.ForeignKey(
        "academics.Term",
        on_delete=models.PROTECT,
        related_name="student_assessments",
    )

    class_subject = models.ForeignKey(
        "academics.ClassSubject",
        on_delete=models.PROTECT,
        related_name="student_assessments",
    )

    assessment_scheme = models.ForeignKey(
        "assessments.AssessmentScheme",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    component = models.ForeignKey(
        AssessmentSchemeComponent,
        on_delete=models.PROTECT,
        related_name="student_assessments",
    )

    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    entered_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="entered_assessments",
    )

    approved = models.BooleanField(
        default=False,
    )

    approved_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_assessments",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "student",
            "component__display_order",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "term",
                    "class_subject",
                    "component",
                ],
                name="unique_student_assessment",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "term",
                    "class_subject",
                ],
            ),
            models.Index(
                fields=[
                    "student",
                    "term",
                ],
            ),
        ]

    def clean(self):
        if self.score < Decimal("0"):
            raise ValidationError("Score cannot be negative.")

        if self.component_id:
            if self.score > self.component.maximum_score:
                raise ValidationError(
                    "Score cannot exceed the maximum " "score for this component."
                )

        if self.enrollment_id and self.student_id:
            if self.enrollment.student_id != self.student_id:
                raise ValidationError("Student does not match enrollment.")

        if (
            self.term_id
            and self.enrollment_id
            and self.term.session_id != self.enrollment.session_id
        ):
            raise ValidationError(
                "Assessment term must belong to " "the student's enrollment session."
            )


###################################################
class SubjectResult(models.Model):
    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="subject_results",
    )

    enrollment = models.ForeignKey(
        "students.Enrollment",
        on_delete=models.PROTECT,
        related_name="subject_results",
    )

    term = models.ForeignKey(
        "academics.Term",
        on_delete=models.PROTECT,
        related_name="subject_results",
    )

    class_subject = models.ForeignKey(
        "academics.ClassSubject",
        on_delete=models.PROTECT,
        related_name="subject_results",
    )

    total_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    grade = models.CharField(
        max_length=10,
        blank=True,
    )

    grade_point = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    remark = models.CharField(
        max_length=100,
        blank=True,
    )

    position = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    class_average = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    is_published = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "class_subject",
            "position",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "term",
                    "class_subject",
                ],
                name="unique_student_subject_result",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "term",
                    "class_subject",
                    "total_score",
                ],
            ),
            models.Index(
                fields=[
                    "enrollment",
                    "term",
                ],
            ),
        ]

    def __str__(self):
        return (
            f"{self.student.full_name} - "
            f"{self.class_subject.subject.name} - "
            f"{self.total_score}"
        )

#########################################

class TraitCategory(models.TextChoices):
    AFFECTIVE = "affective", "Affective"
    PSYCHOMOTOR = "psychomotor", "Psychomotor"


class AssessmentTrait(models.Model):
    name = models.CharField(
        max_length=100,
    )

    code = models.CharField(
        max_length=50,
        unique=True,
    )

    category = models.CharField(
        max_length=20,
        choices=TraitCategory.choices,
    )

    description = models.TextField(
        blank=True,
    )

    display_order = models.PositiveSmallIntegerField(
        default=1,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = [
            "category",
            "display_order",
            "name",
        ]

    def __str__(self):
        return self.name

##################################################

class StudentTraitAssessment(models.Model):
    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="trait_assessments",
    )

    enrollment = models.ForeignKey(
        "students.Enrollment",
        on_delete=models.PROTECT,
        related_name="trait_assessments",
    )

    term = models.ForeignKey(
        "academics.Term",
        on_delete=models.PROTECT,
        related_name="trait_assessments",
    )

    trait = models.ForeignKey(
        AssessmentTrait,
        on_delete=models.PROTECT,
        related_name="student_assessments",
    )

    rating = models.PositiveSmallIntegerField()

    teacher_comment = models.CharField(
        max_length=255,
        blank=True,
    )

    assessed_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="trait_assessments_entered",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "trait__category",
            "trait__display_order",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "term",
                    "trait",
                ],
                name="unique_student_term_trait",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "term",
                    "trait",
                ],
            ),
            models.Index(
                fields=[
                    "student",
                    "term",
                ],
            ),
        ]

    def clean(self):
        if not 1 <= self.rating <= 5:
            raise ValidationError(
                "Trait rating must be between 1 and 5."
            )

        if self.enrollment_id and self.student_id:
            if (
                self.enrollment.student_id
                != self.student_id
            ):
                raise ValidationError(
                    "Student does not match enrollment."
                )

        if (
            self.term_id
            and self.enrollment_id
            and self.term.session_id
            != self.enrollment.session_id
        ):
            raise ValidationError(
                "Term must belong to the student's "
                "enrollment session."
            )

    def __str__(self):
        return (
            f"{self.student.full_name} - "
            f"{self.trait.name} - "
            f"{self.rating}"
        )


##########################################
class TermResult(models.Model):
    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="term_results",
    )

    enrollment = models.ForeignKey(
        "students.Enrollment",
        on_delete=models.PROTECT,
        related_name="term_results",
    )

    term = models.ForeignKey(
        "academics.Term",
        on_delete=models.PROTECT,
        related_name="term_results",
    )

    total_score = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    subject_count = models.PositiveIntegerField(
        default=0,
    )

    average_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    position = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    class_average = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    teacher_remark = models.TextField(
        blank=True,
    )

    principal_remark = models.TextField(
        blank=True,
    )

    principal_signature = models.ImageField(
        upload_to="school/principal/signatures/",
        null=True,
        blank=True,
    )

    next_term_resumption_date = models.DateField(
        null=True,
        blank=True,
    )

    is_published = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "term",
                ],
                name="unique_student_term_result",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "term",
                    "average_score",
                ],
            ),
            models.Index(
                fields=[
                    "enrollment",
                    "term",
                ],
            ),
        ]

    def __str__(self):
        return (
            f"{self.student.full_name} - "
            f"{self.term} - "
            f"{self.average_score}"
        )

#############################################
class GradeScale(models.Model):
    """
    Defines a grading scale for a particular school tier.

    Example:
        Secondary School -> A1, B2, B3, C4, C5, C6,
                            D7, E8, F9

        Primary School -> Merit, Credit, Pass, etc.
    """

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    code = models.CharField(
        max_length=50,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class GradeScaleItem(models.Model):
    """
    Individual grade within a grading scale.

    Example:

        A1 = 75 - 100
        B2 = 70 - 74
        B3 = 65 - 69
        ...
    """

    grade_scale = models.ForeignKey(
        GradeScale,
        on_delete=models.CASCADE,
        related_name="items",
    )

    grade = models.CharField(
        max_length=20,
    )

    min_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    max_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    grade_point = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
    )

    remark = models.CharField(
        max_length=100,
        blank=True,
    )

    display_order = models.PositiveSmallIntegerField(
        default=1,
    )

    class Meta:
        ordering = [
            "-min_score",
            "display_order",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "grade_scale",
                    "grade",
                ],
                name="unique_grade_in_scale",
            ),
        ]

    def clean(self):
        if self.min_score < 0:
            raise ValidationError(
                "Minimum score cannot be negative."
            )

        if self.max_score > 100:
            raise ValidationError(
                "Maximum score cannot exceed 100."
            )

        if self.min_score > self.max_score:
            raise ValidationError(
                "Minimum score cannot be greater than maximum score."
            )

    def __str__(self):
        return (
            f"{self.grade_scale.name} - "
            f"{self.grade} "
            f"({self.min_score}-{self.max_score})"
        )

########################################################
@admin.register(GradeScale)
class GradeScaleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "code",
    )


@admin.register(GradeScaleItem)
class GradeScaleItemAdmin(admin.ModelAdmin):
    list_display = (
        "grade_scale",
        "grade",
        "min_score",
        "max_score",
        "grade_point",
        "remark",
        "display_order",
    )

    list_filter = (
        "grade_scale",
        "grade",
    )

    search_fields = (
        "grade",
        "remark",
    )

    ordering = (
        "grade_scale",
        "-min_score",
    )