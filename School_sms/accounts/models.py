from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    class Role(models.TextChoices):
        SUPER_ADMIN = "super_admin", "Super Administrator"
        SCHOOL_ADMIN = "school_admin", "School Administrator"
        PRINCIPAL = "principal", "Principal"
        VICE_PRINCIPAL = "vice_principal", "Vice Principal"
        HOD = "hod", "Head of Department"
        TEACHER = "teacher", "Teacher"
        BURSAR = "bursar", "Bursar"
        ACCOUNTANT = "accountant", "Accountant"
        LIBRARIAN = "librarian", "Librarian"
        PARENT = "parent", "Parent"
        STUDENT = "student", "Student"

    email = models.EmailField(
        unique=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.TEACHER,
    )

    profile_photo = models.ImageField(
        upload_to="users/profile_photos/",
        blank=True,
        null=True,
    )

    is_active_staff = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def is_school_admin(self):
        return self.role == self.Role.SCHOOL_ADMIN

    @property
    def is_principal(self):
        return self.role == self.Role.PRINCIPAL

    @property
    def is_teacher(self):
        return self.role == self.Role.TEACHER

    @property
    def is_hod(self):
        return self.role == self.Role.HOD

    @property
    def is_parent(self):
        return self.role == self.Role.PARENT
