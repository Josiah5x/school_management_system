from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import SchoolForm
from .forms import SchoolSettingsForm
from .models import School
from .models import SchoolSettings


def is_school_admin(user):
    """Check whether the user can manage school settings."""

    return (
        user.is_authenticated
        and (
            user.is_superuser
            or user.role in [
                "super_admin",
                "school_admin",
                "principal",
            ]
        )
    )


@login_required
def school_detail(request):
    """Display the active school."""

    school = (
        School.objects
        .prefetch_related()
        .filter(is_active=True)
        .first()
    )

    if school is None:
        return redirect("schools:create")

    settings = getattr(
        school,
        "settings",
        None,
    )

    return render(
        request,
        "schools/school_detail.html",
        {
            "school": school,
            "school_settings": settings,
        },
    )


@login_required
def school_create(request):
    """Create the school profile."""

    if not is_school_admin(request.user):
        return render(
            request,
            "403.html",
            status=403,
        )

    if request.method == "POST":
        form = SchoolForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            school = form.save()

            SchoolSettings.objects.create(
                school=school,
            )

            messages.success(
                request,
                "School profile created successfully.",
            )

            return redirect(
                "schools:detail",
            )

    else:
        form = SchoolForm()

    return render(
        request,
        "schools/school_form.html",
        {
            "form": form,
            "title": "Create School",
            "is_create": True,
        },
    )


@login_required
def school_update(request):
    """Update the school profile."""

    if not is_school_admin(request.user):
        return render(
            request,
            "403.html",
            status=403,
        )

    school = get_object_or_404(
        School,
        is_active=True,
    )

    if request.method == "POST":
        form = SchoolForm(
            request.POST,
            request.FILES,
            instance=school,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "School information updated successfully.",
            )

            return redirect(
                "schools:detail",
            )

    else:
        form = SchoolForm(
            instance=school,
        )

    return render(
        request,
        "schools/school_form.html",
        {
            "form": form,
            "school": school,
            "title": "Edit School",
            "is_create": False,
        },
    )


@login_required
def school_settings(request):
    """Update school academic/result settings."""

    if not is_school_admin(request.user):
        return render(
            request,
            "403.html",
            status=403,
        )

    school = get_object_or_404(
        School,
        is_active=True,
    )

    settings, created = (
        SchoolSettings.objects.get_or_create(
            school=school,
        )
    )

    if request.method == "POST":
        form = SchoolSettingsForm(
            request.POST,
            instance=settings,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "School settings updated successfully.",
            )

            return redirect(
                "schools:settings",
            )

    else:
        form = SchoolSettingsForm(
            instance=settings,
        )

    return render(
        request,
        "schools/settings_form.html",
        {
            "form": form,
            "school": school,
            "school_settings": settings,
        },
    )