from django.core.exceptions import ValidationError
from django.db import models

#########################################
class SchoolTier(models.TextChoices):
    NURSERY = "nursery", "Nursery / Creche"
    PRIMARY = "primary", "Primary"
    JSS = "jss", "Junior Secondary"
    SSS = "sss", "Senior Secondary"

##########################################
class Department(models.TextChoices):
    SCIENCE = "science", "Science"
    ARTS = "arts", "Arts"
    COMMERCIAL = "commercial", "Commercial"

##############################################
class AcademicSession(models.Model):
    school = models.ForeignKey(
        "schools.School",
        on_delete=models.CASCADE,
        related_name="academic_sessions",
    )

    name = models.CharField(
        max_length=20,
        help_text="Example: 2026/2027",
    )

    start_date = models.DateField()

    end_date = models.DateField()

    is_current = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-start_date"]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "school",
                    "name",
                ],
                name="unique_school_academic_session",
            ),
        ]

    def __str__(self):
        return f"{self.school.name} - {self.name}"
    

#####################################################
class Term(models.Model):

    class TermType(models.TextChoices):
        FIRST = "first", "First Term"
        SECOND = "second", "Second Term"
        THIRD = "third", "Third Term"

    session = models.ForeignKey(
        AcademicSession,
        on_delete=models.CASCADE,
        related_name="terms",
    )

    term = models.CharField(
        max_length=10,
        choices=TermType.choices,
    )

    start_date = models.DateField()

    end_date = models.DateField()

    next_term_resumption_date = models.DateField(
        null=True,
        blank=True,
    )

    is_current = models.BooleanField(
        default=False,
    )

    result_published = models.BooleanField(
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
            "session",
            "term",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "session",
                    "term",
                ],
                name="unique_session_term",
            ),
        ]

    def __str__(self):
        return (
            f"{self.session.name} - "
            f"{self.get_term_display()}"
        )

#########################################
class AcademicClass(models.Model):
    school = models.ForeignKey(
        "schools.School",
        on_delete=models.CASCADE,
        related_name="academic_classes",
    )

    name = models.CharField(
        max_length=50,
    )

    tier = models.CharField(
        max_length=20,
        choices=SchoolTier.choices,
    )

    level = models.PositiveSmallIntegerField(
        help_text=(
            "Nursery 1-3, Basic 1-6, "
            "JSS 1-3 or SSS 1-3."
        ),
    )

    department = models.CharField(
        max_length=20,
        choices=Department.choices,
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = [
            "tier",
            "level",
            "name",
        ]

    def clean(self):
        if self.tier == SchoolTier.SSS:
            if not self.department:
                raise ValidationError(
                    "SSS classes must have a department."
                )

        elif self.department:
            raise ValidationError(
                "Only SSS classes can have a department."
            )

    def __str__(self):
        if self.department:
            return (
                f"{self.name} - "
                f"{self.get_department_display()}"
            )

        return self.name

#############################################
class ClassArm(models.Model):
    academic_class = models.ForeignKey(
        AcademicClass,
        on_delete=models.CASCADE,
        related_name="arms",
    )

    name = models.CharField(
        max_length=20,
        help_text="Example: A, B, C",
    )

    form_teacher = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="form_teacher_arms",
    )

    capacity = models.PositiveIntegerField(
        default=40,
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
        ordering = [
            "academic_class",
            "name",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "academic_class",
                    "name",
                ],
                name="unique_class_arm",
            ),
        ]

    def __str__(self):
        return (
            f"{self.academic_class.name} "
            f"{self.name}"
        )

#########################################
class Subject(models.Model):
    name = models.CharField(
        max_length=150,
    )

    code = models.CharField(
        max_length=30,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    is_core = models.BooleanField(
        default=False,
    )

    is_practical = models.BooleanField(
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

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.code} - {self.name}"

#############################################

class ClassSubject(models.Model):
    academic_class = models.ForeignKey(
        AcademicClass,
        on_delete=models.CASCADE,
        related_name="class_subjects",
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="class_subjects",
    )

    is_compulsory = models.BooleanField(
        default=True,
    )

    maximum_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=100,
    )

    display_order = models.PositiveSmallIntegerField(
        default=1,
    )

    class Meta:
        ordering = [
            "academic_class",
            "display_order",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "academic_class",
                    "subject",
                ],
                name="unique_class_subject",
            ),
        ]

    def __str__(self):
        return (
            f"{self.academic_class} - "
            f"{self.subject}"
        )

############################################

class TeacherSubjectAssignment(models.Model):
    teacher = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="subject_assignments",
    )

    class_arm = models.ForeignKey(
        ClassArm,
        on_delete=models.CASCADE,
        related_name="teacher_assignments",
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="teacher_assignments",
    )

    session = models.ForeignKey(
        AcademicSession,
        on_delete=models.CASCADE,
        related_name="teacher_assignments",
    )

    is_class_teacher = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "teacher",
                    "class_arm",
                    "subject",
                    "session",
                ],
                name="unique_teacher_subject_assignment",
            ),
        ]

    def clean(self):
        if self.teacher.role not in [
            "teacher",
            "hod",
            "principal",
            "vice_principal",
        ]:
            raise ValidationError(
                "Only academic staff can be assigned subjects."
            )

    def __str__(self):
        return (
            f"{self.teacher} - "
            f"{self.subject} - "
            f"{self.class_arm}"
        )


##########################################