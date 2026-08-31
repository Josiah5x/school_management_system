from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Student(models.Model):
    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"

    school = models.ForeignKey(
        "schools.School",
        on_delete=models.CASCADE,
        related_name="students",
    )

    admission_number = models.CharField(
        max_length=30,
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

    birth_place = models.CharField(
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

    address = models.TextField(
        blank=True,
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    photo = models.ImageField(
        upload_to="students/photos/",
        null=True,
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
        ordering = [
            "last_name",
            "first_name",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "school",
                    "admission_number",
                ],
                name="unique_school_admission_number",
            ),
        ]

    def __str__(self):
        return (
            f"{self.admission_number} - "
            f"{self.full_name}"
        )

    @property
    def full_name(self):
        names = [
            self.first_name,
            self.middle_name,
            self.last_name,
        ]

        return " ".join(
            name for name in names if name
        )

##########################################
class Guardian(models.Model):
    class Relationship(models.TextChoices):
        FATHER = "father", "Father"
        MOTHER = "mother", "Mother"
        GUARDIAN = "guardian", "Guardian"
        UNCLE = "uncle", "Uncle"
        AUNT = "aunt", "Aunt"
        GRANDFATHER = "grandfather", "Grandfather"
        GRANDMOTHER = "grandmother", "Grandmother"
        OTHER = "other", "Other"

    school = models.ForeignKey(
        "schools.School",
        on_delete=models.CASCADE,
        related_name="guardians",
    )

    first_name = models.CharField(
        max_length=100,
    )

    last_name = models.CharField(
        max_length=100,
    )

    phone = models.CharField(
        max_length=30,
    )

    alternative_phone = models.CharField(
        max_length=30,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    address = models.TextField(
        blank=True,
    )

    occupation = models.CharField(
        max_length=150,
        blank=True,
    )

    relationship = models.CharField(
        max_length=30,
        choices=Relationship.choices,
        default=Relationship.GUARDIAN,
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
            "last_name",
            "first_name",
        ]

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return (
            f"{self.first_name} "
            f"{self.last_name}"
        )

###########################################
class StudentGuardian(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="guardians",
    )

    guardian = models.ForeignKey(
        Guardian,
        on_delete=models.CASCADE,
        related_name="students",
    )

    relationship = models.CharField(
        max_length=30,
        choices=Guardian.Relationship.choices,
    )

    is_primary = models.BooleanField(
        default=False,
    )

    can_pickup = models.BooleanField(
        default=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "guardian",
                ],
                name="unique_student_guardian",
            ),
        ]

    def __str__(self):
        return (
            f"{self.guardian} - "
            f"{self.student}"
        )

###########################################
class Enrollment(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        COMPLETED = "completed", "Completed"
        TRANSFERRED = "transferred", "Transferred"
        WITHDRAWN = "withdrawn", "Withdrawn"
        GRADUATED = "graduated", "Graduated"

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )

    session = models.ForeignKey(
        "academics.AcademicSession",
        on_delete=models.PROTECT,
        related_name="enrollments",
    )

    academic_class = models.ForeignKey(
        "academics.AcademicClass",
        on_delete=models.PROTECT,
        related_name="enrollments",
    )

    class_arm = models.ForeignKey(
        "academics.ClassArm",
        on_delete=models.PROTECT,
        related_name="enrollments",
    )

    admission_date = models.DateField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    is_boarding = models.BooleanField(
        default=False,
    )

    boarding_house = models.CharField(
        max_length=100,
        blank=True,
    )

    remark = models.TextField(
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
            "student__last_name",
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

    def clean(self):
        if (
            self.class_arm
            and self.academic_class
            and self.class_arm.academic_class_id
            != self.academic_class_id
        ):
            raise ValidationError(
                "Class arm must belong to the selected academic class."
            )

    def __str__(self):
        return (
            f"{self.student.full_name} - "
            f"{self.academic_class.name} "
            f"{self.class_arm.name} - "
            f"{self.session.name}"
        )

###############################################

########################################

# class StudentAddress(models.Model):
#     studentss = models.OneToOneField(
#         Student,
#         on_delete=models.CASCADE,
#         related_name="address",
#     )

#     house_number = models.CharField(
#         max_length=30,
#         blank=True,
#     )

#     street = models.CharField(
#         max_length=150,
#         blank=True,
#     )

#     city = models.CharField(
#         max_length=100,
#         blank=True,
#     )

#     state = models.CharField(
#         max_length=100,
#         blank=True,
#     )

#     lga = models.CharField(
#         max_length=100,
#         blank=True,
#     )

#     postal_code = models.CharField(
#         max_length=20,
#         blank=True,
#     )

#     created_at = models.DateTimeField(
#         auto_now_add=True,
#     )

#     updated_at = models.DateTimeField(
#         auto_now=True,
#     )

#     def __str__(self):
#         return f"Address - {self.student.full_name}"

# #######################################################

