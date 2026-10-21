from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import EnrollmentForm
from .forms import GuardianForm
from .forms import StudentForm
from .forms import StudentGuardianForm
from .models import Enrollment
from .models import Guardian
from .models import Student
from .models import StudentGuardian


@login_required
def dashboard(request):
    return render(request, 'students/dashboard.html',{})

@login_required
def student_list(request):
    students = (
        Student.objects
        .select_related("school")
        .prefetch_related(
            "enrollments__session",
            "enrollments__academic_class",
            "enrollments__class_arm",
        )
        .filter(is_active=True)
        .order_by(
            "last_name",
            "first_name",
        )
    )

    query = request.GET.get("q", "").strip()

    if query:
        students = students.filter(
            admission_number__icontains=query
        ) | students.filter(
            first_name__icontains=query
        ) | students.filter(
            last_name__icontains=query
        )

    return render(
        request,
        "students/student_list.html",
        {
            "students": students,
            "query": query,
        },
    )


@login_required
def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)

        if form.is_valid():
            student = form.save()

            messages.success(
                request,
                "Student registered successfully.",
            )

            return redirect(
                "students:student_detail",
                pk=student.pk,
            )

    else:
        form = StudentForm()

    return render(
        request,
        "students/student_form.html",
        {
            "form": form,
            "title": "Register Student",
        },
    )

@property
def current_enrollment(self):
    return (
        self.enrollments
        .select_related(
            "session",
            "academic_class",
            "class_arm",
        )
        .filter(
            status=Enrollment.Status.ACTIVE,
            session__is_current=True,
        )
        .first()
    )

@login_required
def student_update(request, pk):
    student = get_object_or_404(
        Student.objects.select_related("school"),
        pk=pk,
    )

    if request.method == "POST":
        form = StudentForm(
            request.POST,
            request.FILES,
            instance=student,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Student information updated successfully.",
            )

            return redirect(
                "students:student_detail",
                pk=student.pk,
            )

    else:
        form = StudentForm(instance=student)

    return render(
        request,
        "students/student_form.html",
        {
            "form": form,
            "student": student,
            "title": "Edit Student",
        },
    )


@login_required
def student_detail(request, pk):
    student = get_object_or_404(
        Student.objects
        .select_related("school")
        .prefetch_related(
            "guardians__guardian",
            "enrollments__session",
            "enrollments__academic_class",
            "enrollments__class_arm",
        ),
        pk=pk,
    )

    return render(
        request,
        "students/student_detail.html",
        {
            "student": student,
        },
    )


@login_required
def student_delete(request, pk):
    student = get_object_or_404(
        Student,
        pk=pk,
    )

    if request.method == "POST":
        student.is_active = False
        student.save(
            update_fields=[
                "is_active",
                "updated_at",
            ]
        )

        messages.success(
            request,
            "Student has been deactivated.",
        )

        return redirect(
            "students:student_list",
        )

    return render(
        request,
        "students/student_confirm_delete.html",
        {
            "student": student,
        },
    )


@login_required
def enrollment_list(request):
    enrollments = (
        Enrollment.objects
        .select_related(
            "student",
            "student__school",
            "session",
            "academic_class",
            "class_arm",
        )
        .order_by(
            "-session__start_date",
            "academic_class__level",
            "class_arm__name",
            "student__last_name",
        )
    )

    return render(
        request,
        "students/enrollment_list.html",
        {
            "enrollments": enrollments,
        },
    )


@login_required
def enrollment_create(request):
    if request.method == "POST":
        form = EnrollmentForm(request.POST)

        if form.is_valid():
            enrollment = form.save()

            messages.success(
                request,
                "Student enrolled successfully.",
            )

            return redirect(
                "students:enrollment_list",
            )

    else:
        form = EnrollmentForm()

    return render(
        request,
        "students/enrollment_form.html",
        {
            "form": form,
            "title": "Enroll Student",
        },
    )


@login_required
def enrollment_update(request, pk):
    enrollment = get_object_or_404(
        Enrollment.objects.select_related(
            "student",
            "session",
            "academic_class",
            "class_arm",
        ),
        pk=pk,
    )

    if request.method == "POST":
        form = EnrollmentForm(
            request.POST,
            instance=enrollment,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Enrollment updated successfully.",
            )

            return redirect(
                "students:enrollment_list",
            )

    else:
        form = EnrollmentForm(
            instance=enrollment,
        )

    return render(
        request,
        "students/enrollment_form.html",
        {
            "form": form,
            "enrollment": enrollment,
            "title": "Edit Enrollment",
        },
    )




@login_required
def guardian_list(request):
    guardians = (
        Guardian.objects
        .select_related("school")
        .prefetch_related(
            "students__student",
        )
        .filter(
            is_active=True,
        )
        .order_by(
            "last_name",
            "first_name",
        )
    )

    query = request.GET.get(
        "q",
        "",
    ).strip()

    if query:
        guardians = guardians.filter(
            first_name__icontains=query,
        ) | guardians.filter(
            last_name__icontains=query,
        ) | guardians.filter(
            phone__icontains=query,
        ) | guardians.filter(
            email__icontains=query,
        )

    return render(
        request,
        "students/guardian_list.html",
        {
            "guardians": guardians,
            "query": query,
        },
    )


@login_required
def guardian_create(request):
    if request.method == "POST":
        form = GuardianForm(
            request.POST,
        )

        if form.is_valid():
            guardian = form.save()

            messages.success(
                request,
                "Guardian registered successfully.",
            )

            return redirect(
                "students:guardian_detail",
                pk=guardian.pk,
            )

    else:
        form = GuardianForm()

    return render(
        request,
        "students/guardian_form.html",
        {
            "form": form,
            "title": "Register Guardian",
        },
    )


@login_required
def guardian_update(request, pk):
    guardian = get_object_or_404(
        Guardian.objects.select_related(
            "school",
        ),
        pk=pk,
    )

    if request.method == "POST":
        form = GuardianForm(
            request.POST,
            instance=guardian,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Guardian information updated successfully.",
            )

            return redirect(
                "students:guardian_detail",
                pk=guardian.pk,
            )

    else:
        form = GuardianForm(
            instance=guardian,
        )

    return render(
        request,
        "students/guardian_form.html",
        {
            "form": form,
            "guardian": guardian,
            "title": "Edit Guardian",
        },
    )


@login_required
def guardian_detail(request, pk):
    guardian = get_object_or_404(
        Guardian.objects
        .select_related("school")
        .prefetch_related(
            "students__student",
            "students__student__enrollments__academic_class",
            "students__student__enrollments__class_arm",
            "students__student__enrollments__session",
        ),
        pk=pk,
    )

    return render(
        request,
        "students/guardian_detail.html",
        {
            "guardian": guardian,
        },
    )


@login_required
def guardian_deactivate(request, pk):
    guardian = get_object_or_404(
        Guardian,
        pk=pk,
    )

    if request.method == "POST":
        guardian.is_active = False

        guardian.save(
            update_fields=[
                "is_active",
                "updated_at",
            ]
        )

        messages.success(
            request,
            "Guardian has been deactivated.",
        )

        return redirect(
            "students:guardian_list",
        )

    return render(
        request,
        "students/guardian_confirm_delete.html",
        {
            "guardian": guardian,
        },
    )

@login_required
def student_guardian_create(
    request,
    student_pk,
):
    student = get_object_or_404(
        Student,
        pk=student_pk,
    )

    if request.method == "POST":
        form = StudentGuardianForm(
            request.POST,
        )

        if form.is_valid():
            relationship = form.save(
                commit=False,
            )

            relationship.student = student

            relationship.save()

            messages.success(
                request,
                "Guardian linked to student successfully.",
            )

            return redirect(
                "students:student_detail",
                pk=student.pk,
            )

    else:
        form = StudentGuardianForm()

    return render(
        request,
        "students/student_guardian_form.html",
        {
            "form": form,
            "student": student,
        },
    )


@login_required
def student_guardian_delete(
    request,
    student_pk,
    relation_pk,
):
    relationship = get_object_or_404(
        StudentGuardian.objects.select_related(
            "student",
            "guardian",
        ),
        pk=relation_pk,
        student_id=student_pk,
    )

    if request.method == "POST":
        student = relationship.student

        relationship.delete()

        messages.success(
            request,
            "Guardian removed from student.",
        )

        return redirect(
            "students:student_detail",
            pk=student.pk,
        )

    return render(
        request,
        "students/student_guardian_confirm_delete.html",
        {
            "relationship": relationship,
        },
    )