from django.core.exceptions import ValidationError
from django.db import models


class Guardian(models.Model):
    class Relationship(models.TextChoices):
        FATHER = "father", "Father"
        MOTHER = "mother", "Mother"
        GUARDIAN = "guardian", "Guardian"
        GRANDPARENT = "grandparent", "Grandparent"
        OTHER = "other", "Other"

    first_name = models.CharField(
        max_length=100,
    )

    last_name = models.CharField(
        max_length=100,
    )

    relationship = models.CharField(
        max_length=20,
        choices=Relationship.choices,
    )

    phone = models.CharField(
        max_length=30,
    )

    alternate_phone = models.CharField(
        max_length=30,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    occupation = models.CharField(
        max_length=150,
        blank=True,
    )

    address = models.TextField(
        blank=True,
    )

    is_primary = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name

###############################################

class Student(models.Model):

    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        GRADUATED = "graduated", "Graduated"
        WITHDRAWN = "withdrawn", "Withdrawn"
        EXPELLED = "expelled", "Expelled"

    admission_number = models.CharField(
        max_length=50,
        unique=True,
    )

    first_name = models.CharField(
        max_length=100,
    )

    middle_name = models.CharField(
        max_length=100,
        blank=True,
    )

    last_name = models.CharField(
        max_length=100,
    )

    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    place_of_birth = models.CharField(
        max_length=150,
        blank=True,
    )

    nationality = models.CharField(
        max_length=100,
        default="Nigerian",
    )

    state_of_origin = models.CharField(
        max_length=100,
        blank=True,
    )

    lga_of_origin = models.CharField(
        max_length=100,
        blank=True,
    )

    religion = models.CharField(
        max_length=100,
        blank=True,
    )

    blood_group = models.CharField(
        max_length=10,
        blank=True,
    )

    genotype = models.CharField(
        max_length=10,
        blank=True,
    )

    photo = models.ImageField(
        upload_to="students/photos/",
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    admission_date = models.DateField(
        null=True,
        blank=True,
    )

    previous_school = models.CharField(
        max_length=255,
        blank=True,
    )

    previous_school_address = models.TextField(
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    guardians = models.ManyToManyField(
        Guardian,
        related_name="students",
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "last_name",
            "first_name",
        ]

        indexes = [
            models.Index(
                fields=[
                    "last_name",
                    "first_name",
                ],
            ),
            models.Index(
                fields=[
                    "status",
                ],
            ),
        ]

    @property
    def full_name(self):
        return " ".join(
            part
            for part in [
                self.first_name,
                self.middle_name,
                self.last_name,
            ]
            if part
        )

    def __str__(self):
        return (
            f"{self.admission_number} - "
            f"{self.full_name}"
        )

#############################################
class Enrollment(models.Model):

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        COMPLETED = "completed", "Completed"
        TRANSFERRED = "transferred", "Transferred"
        WITHDRAWN = "withdrawn", "Withdrawn"

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )

    session = models.ForeignKey(
        "academics.AcademicSession",
        on_delete=models.PROTECT,
        related_name="student_enrollments",
    )

    class_arm = models.ForeignKey(
        "academics.ClassArm",
        on_delete=models.PROTECT,
        related_name="student_enrollments",
    )

    admission_date = models.DateField(
        null=True,
        blank=True,
    )

    roll_number = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    is_current = models.BooleanField(
        default=False,
    )

    remarks = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "-session__start_date",
            "class_arm",
            "roll_number",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "session",
                ],
                name="unique_student_session_enrollment",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "session",
                    "class_arm",
                ],
            ),
            models.Index(
                fields=[
                    "student",
                    "is_current",
                ],
            ),
        ]

    def clean(self):
        if (
            self.class_arm_id
            and self.session_id
            and self.class_arm.academic_class.school_id
            != self.session.school_id
        ):
            raise ValidationError(
                "Student enrollment class must belong "
                "to the same school as the academic session."
            )

    def __str__(self):
        return (
            f"{self.student.full_name} - "
            f"{self.class_arm} - "
            f"{self.session.name}"
        )

########################################

class StudentAddress(models.Model):
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name="address",
    )

    house_number = models.CharField(
        max_length=30,
        blank=True,
    )

    street = models.CharField(
        max_length=150,
        blank=True,
    )

    city = models.CharField(
        max_length=100,
        blank=True,
    )

    state = models.CharField(
        max_length=100,
        blank=True,
    )

    lga = models.CharField(
        max_length=100,
        blank=True,
    )

    postal_code = models.CharField(
        max_length=20,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"Address - {self.student.full_name}"

#######################################################

