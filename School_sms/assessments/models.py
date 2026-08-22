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


######################################


class AssessmentScheme(models.Model):

    name = models.CharField(max_length=100)

    maximum_total = models.DecimalField(max_digits=5, decimal_places=2, default=100)

    is_default = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


###########################################


class AssessmentScheme(models.Model):

    name = models.CharField(max_length=100)

    maximum_total = models.DecimalField(max_digits=5, decimal_places=2, default=100)

    is_default = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


##########################################


class AssessmentSchemeComponent(models.Model):

    scheme = models.ForeignKey(
        AssessmentScheme, on_delete=models.CASCADE, related_name="components"
    )

    component = models.ForeignKey(
        AssessmentComponent, on_delete=models.PROTECT, related_name="scheme_components"
    )

    maximum_score = models.DecimalField(max_digits=5, decimal_places=2)

    display_order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "scheme",
                    "component",
                ],
                name="unique_scheme_component",
            )
        ]

        ordering = [
            "display_order",
        ]

    def __str__(self):
        return f"{self.scheme.name} - " f"{self.component.name}"


########################################
