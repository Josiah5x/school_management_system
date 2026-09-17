from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class User(AbstractUser):

    class Role(models.TextChoices):
        SUPER_ADMIN = (
            "super_admin",
            "Super Administrator",
        )
        SCHOOL_ADMIN = (
            "school_admin",
            "School Administrator",
        )
        PRINCIPAL = (
            "principal",
            "Principal",
        )
        VICE_PRINCIPAL = (
            "vice_principal",
            "Vice Principal",
        )
        HEAD_TEACHER = (
            "head_teacher",
            "Head Teacher",
        )
        TEACHER = (
            "teacher",
            "Teacher",
        )
        FORM_TEACHER = (
            "form_teacher",
            "Form Teacher",
        )
        BURSAR = (
            "bursar",
            "Bursar",
        )
        ACCOUNTANT = (
            "accountant",
            "Accountant",
        )
        REGISTRAR = (
            "registrar",
            "Registrar",
        )
        STUDENT = (
            "student",
            "Student",
        )
        PARENT = (
            "parent",
            "Parent/Guardian",
        )

    school = models.ForeignKey(
        "schools.School",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )

    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.TEACHER,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    staff_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    profile_photo = models.ImageField(
        upload_to="accounts/profiles/",
        blank=True,
        null=True,
    )

    address = models.TextField(
        blank=True,
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )

    is_verified = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def clean(self):
        super().clean()

        if (
            self.role != self.Role.SUPER_ADMIN
            and self.school_id is None
        ):
            raise ValidationError(
                "Every non-super-admin user must "
                "belong to a school."
            )

        if (
            self.role == self.Role.SUPER_ADMIN
            and self.school_id is not None
        ):
            raise ValidationError(
                "Super Administrator must not "
                "be assigned to a school."
            )

    class Meta:
        ordering = [
            "first_name",
            "last_name",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "school",
                    "staff_id",
                ],
                condition=Q(
                    staff_id__isnull=False,
                ),
                name="unique_staff_id_per_school",
            ),
        ]

    def __str__(self):
        return (
            self.get_full_name()
            or self.username
        )

    @property
    def display_name(self):
        return (
            self.get_full_name()
            or self.username
        )

    @property
    def role_name(self):
        return self.get_role_display()

    @property
    def school_name(self):
        if self.school_id:
            return self.school.name

        return "All Schools"