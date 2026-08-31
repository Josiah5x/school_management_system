from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        SUPER_ADMIN = "super_admin", "Super Administrator"
        SCHOOL_ADMIN = "school_admin", "School Administrator"
        PRINCIPAL = "principal", "Principal"
        VICE_PRINCIPAL = "vice_principal", "Vice Principal"
        HEAD_TEACHER = "head_teacher", "Head Teacher"
        TEACHER = "teacher", "Teacher"
        FORM_TEACHER = "form_teacher", "Form Teacher"
        BURSAR = "bursar", "Bursar"
        ACCOUNTANT = "accountant", "Accountant"
        REGISTRAR = "registrar", "Registrar"
        STUDENT = "student", "Student"
        PARENT = "parent", "Parent/Guardian"

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
        unique=True,
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

    class Meta:
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def display_name(self):
        return self.get_full_name() or self.username

    @property
    def role_name(self):
        return self.get_role_display()