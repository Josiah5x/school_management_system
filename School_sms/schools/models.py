from django.core.validators import FileExtensionValidator
from django.db import models


class School(models.Model):
    name = models.CharField(
        max_length=255,
    )

    short_name = models.CharField(
        max_length=50,
        blank=True,
    )

    address = models.TextField()

    phone = models.CharField(
        max_length=30,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    website = models.URLField(
        blank=True,
    )

    logo = models.ImageField(
        upload_to="schools/logos/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "jpg",
                    "jpeg",
                    "png",
                    "webp",
                ]
            )
        ],
    )

    motto = models.CharField(
        max_length=255,
        blank=True,
    )

    principal_name = models.CharField(
        max_length=150,
        blank=True,
    )

    principal_signature = models.ImageField(
        upload_to="schools/signatures/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "jpg",
                    "jpeg",
                    "png",
                    "webp",
                ]
            )
        ],
    )

    principal_stamp = models.ImageField(
        upload_to="schools/stamps/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "jpg",
                    "jpeg",
                    "png",
                    "webp",
                ]
            )
        ],
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


class SchoolSettings(models.Model):
    school = models.OneToOneField(
        School,
        on_delete=models.CASCADE,
        related_name="settings",
    )

    country = models.CharField(
        max_length=100,
        default="Nigeria",
    )

    state = models.CharField(
        max_length=100,
        blank=True,
    )

    lga = models.CharField(
        max_length=100,
        blank=True,
    )

    currency = models.CharField(
        max_length=10,
        default="NGN",
    )

    grading_enabled = models.BooleanField(
        default=True,
    )

    result_position_enabled = models.BooleanField(
        default=True,
    )

    show_class_average = models.BooleanField(
        default=True,
    )

    show_student_average = models.BooleanField(
        default=True,
    )

    show_affective_domain = models.BooleanField(
        default=True,
    )

    show_psychomotor_domain = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"Settings - {self.school.name}"