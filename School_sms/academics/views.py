# Django core imports
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

# Local application forms
from .forms import (
    AcademicClassForm,
    ClassArmForm,
    ClassSubjectForm,
    SubjectForm,
    TeacherSubjectAssignmentForm,
)

# Local application models
from .models import (
    AcademicClass, 
    ClassArm, 
    ClassSubject, 
    Subject, 
    TeacherSubjectAssignment,
)



@login_required
def session_list(request):
    """Display all academic sessions."""

    sessions = (
        AcademicSession.objects
        .select_related("school")
        .prefetch_related("terms")
        .all()
    )

    return render(
        request,
        "academics/session_list.html",
        {
            "sessions": sessions,
        },
    )


@login_required
def session_create(request):
    """Create a new academic session."""

    if request.method == "POST":
        form = AcademicSessionForm(
            request.POST,
        )

        if form.is_valid():
            with transaction.atomic():
                session = form.save()

                if session.is_current:
                    (
                        AcademicSession.objects
                        .filter(
                            school=session.school,
                        )
                        .exclude(
                            pk=session.pk,
                        )
                        .update(
                            is_current=False,
                        )
                    )

            messages.success(
                request,
                "Academic session created successfully.",
            )

            return redirect(
                "academics:session_detail",
                pk=session.pk,
            )

    else:
        form = AcademicSessionForm()

    return render(
        request,
        "academics/session_form.html",
        {
            "form": form,
            "title": "Create Academic Session",
            "is_create": True,
        },
    )


@login_required
def session_detail(request, pk):
    """Display an academic session and its terms."""

    session = get_object_or_404(
        AcademicSession.objects
        .select_related("school")
        .prefetch_related("terms"),
        pk=pk,
    )

    return render(
        request,
        "academics/session_detail.html",
        {
            "session": session,
            "terms": session.terms.all(),
        },
    )


@login_required
def session_update(request, pk):
    """Update an academic session."""

    session = get_object_or_404(
        AcademicSession,
        pk=pk,
    )

    if request.method == "POST":
        form = AcademicSessionForm(
            request.POST,
            instance=session,
        )

        if form.is_valid():
            with transaction.atomic():
                session = form.save()

                if session.is_current:
                    (
                        AcademicSession.objects
                        .filter(
                            school=session.school,
                        )
                        .exclude(
                            pk=session.pk,
                        )
                        .update(
                            is_current=False,
                        )
                    )

            messages.success(
                request,
                "Academic session updated successfully.",
            )

            return redirect(
                "academics:session_detail",
                pk=session.pk,
            )

    else:
        form = AcademicSessionForm(
            instance=session,
        )

    return render(
        request,
        "academics/session_form.html",
        {
            "form": form,
            "session": session,
            "title": "Edit Academic Session",
            "is_create": False,
        },
    )


@login_required
def session_delete(request, pk):
    """Delete an academic session."""

    session = get_object_or_404(
        AcademicSession,
        pk=pk,
    )

    if request.method == "POST":
        session.delete()

        messages.success(
            request,
            "Academic session deleted successfully.",
        )

        return redirect(
            "academics:session_list",
        )

    return render(
        request,
        "academics/session_detail.html",
        {
            "session": session,
            "delete_confirmation": True,
        },
    )


@login_required
def term_list(request):
    """Display all terms."""

    terms = (
        Term.objects
        .select_related(
            "session",
            "session__school",
        )
        .all()
    )

    return render(
        request,
        "academics/term_list.html",
        {
            "terms": terms,
        },
    )


@login_required
def term_create(request, session_pk=None):
    """Create a term."""

    if request.method == "POST":
        form = TermForm(
            request.POST,
        )

        if form.is_valid():
            term = form.save()

            messages.success(
                request,
                "Academic term created successfully.",
            )

            return redirect(
                "academics:session_detail",
                pk=term.session.pk,
            )

    else:
        if session_pk:
            session = get_object_or_404(
                AcademicSession,
                pk=session_pk,
            )

            form = TermForm(
                initial={
                    "session": session,
                }
            )
        else:
            form = TermForm()

    return render(
        request,
        "academics/term_form.html",
        {
            "form": form,
            "title": "Create Academic Term",
            "is_create": True,
        },
    )


@login_required
def term_update(request, pk):
    """Update an academic term."""

    term = get_object_or_404(
        Term,
        pk=pk,
    )

    if request.method == "POST":
        form = TermForm(
            request.POST,
            instance=term,
        )

        if form.is_valid():
            term = form.save()

            messages.success(
                request,
                "Academic term updated successfully.",
            )

            return redirect(
                "academics:session_detail",
                pk=term.session.pk,
            )

    else:
        form = TermForm(
            instance=term,
        )

    return render(
        request,
        "academics/term_form.html",
        {
            "form": form,
            "term": term,
            "title": "Edit Academic Term",
            "is_create": False,
        },
    )


@login_required
def term_delete(request, pk):
    """Delete an academic term."""

    term = get_object_or_404(
        Term,
        pk=pk,
    )

    session_pk = term.session.pk

    if request.method == "POST":
        term.delete()

        messages.success(
            request,
            "Academic term deleted successfully.",
        )

        return redirect(
            "academics:session_detail",
            pk=session_pk,
        )

    return render(
        request,
        "academics/term_form.html",
        {
            "term": term,
            "delete_confirmation": True,
        },
    )


@login_required
def class_list(request):
    """Display all academic classes."""

    classes = (
        AcademicClass.objects
        .select_related("school")
        .prefetch_related("arms")
        .all()
    )

    return render(
        request,
        "academics/class_list.html",
        {
            "classes": classes,
        },
    )


@login_required
def class_create(request):
    """Create an academic class."""

    if request.method == "POST":
        form = AcademicClassForm(request.POST)

        if form.is_valid():
            academic_class = form.save()

            messages.success(
                request,
                "Academic class created successfully.",
            )

            return redirect(
                "academics:class_detail",
                pk=academic_class.pk,
            )

    else:
        form = AcademicClassForm()

    return render(
        request,
        "academics/class_form.html",
        {
            "form": form,
            "title": "Create Academic Class",
        },
    )


@login_required
def class_detail(request, pk):
    """Display an academic class and its arms."""

    academic_class = get_object_or_404(
        AcademicClass.objects
        .select_related("school")
        .prefetch_related(
            "arms",
            "arms__form_teacher",
        ),
        pk=pk,
    )

    return render(
        request,
        "academics/class_detail.html",
        {
            "academic_class": academic_class,
            "arms": academic_class.arms.all(),
        },
    )


@login_required
def class_update(request, pk):
    """Update an academic class."""

    academic_class = get_object_or_404(
        AcademicClass,
        pk=pk,
    )

    if request.method == "POST":
        form = AcademicClassForm(
            request.POST,
            instance=academic_class,
        )

        if form.is_valid():
            academic_class = form.save()

            messages.success(
                request,
                "Academic class updated successfully.",
            )

            return redirect(
                "academics:class_detail",
                pk=academic_class.pk,
            )

    else:
        form = AcademicClassForm(
            instance=academic_class,
        )

    return render(
        request,
        "academics/class_form.html",
        {
            "form": form,
            "academic_class": academic_class,
            "title": "Edit Academic Class",
        },
    )


@login_required
def class_delete(request, pk):
    """Delete an academic class."""

    academic_class = get_object_or_404(
        AcademicClass,
        pk=pk,
    )

    if request.method == "POST":
        academic_class.delete()

        messages.success(
            request,
            "Academic class deleted successfully.",
        )

        return redirect(
            "academics:class_list",
        )

    return render(
        request,
        "academics/class_confirm_delete.html",
        {
            "academic_class": academic_class,
        },
    )


@login_required
def arm_create(request, class_pk=None):
    """Create a class arm."""

    if request.method == "POST":
        form = ClassArmForm(request.POST)

        if form.is_valid():
            arm = form.save()

            messages.success(
                request,
                "Class arm created successfully.",
            )

            return redirect(
                "academics:class_detail",
                pk=arm.academic_class.pk,
            )

    else:
        if class_pk:
            academic_class = get_object_or_404(
                AcademicClass,
                pk=class_pk,
            )

            form = ClassArmForm(
                initial={
                    "academic_class": academic_class,
                }
            )
        else:
            form = ClassArmForm()

    return render(
        request,
        "academics/arm_form.html",
        {
            "form": form,
            "title": "Create Class Arm",
        },
    )


@login_required
def arm_update(request, pk):
    """Update a class arm."""

    arm = get_object_or_404(
        ClassArm,
        pk=pk,
    )

    if request.method == "POST":
        form = ClassArmForm(
            request.POST,
            instance=arm,
        )

        if form.is_valid():
            arm = form.save()

            messages.success(
                request,
                "Class arm updated successfully.",
            )

            return redirect(
                "academics:class_detail",
                pk=arm.academic_class.pk,
            )

    else:
        form = ClassArmForm(
            instance=arm,
        )

    return render(
        request,
        "academics/arm_form.html",
        {
            "form": form,
            "arm": arm,
            "title": "Edit Class Arm",
        },
    )


@login_required
def arm_delete(request, pk):
    """Delete a class arm."""

    arm = get_object_or_404(
        ClassArm.objects.select_related(
            "academic_class",
        ),
        pk=pk,
    )

    class_pk = arm.academic_class.pk

    if request.method == "POST":
        arm.delete()

        messages.success(
            request,
            "Class arm deleted successfully.",
        )

        return redirect(
            "academics:class_detail",
            pk=class_pk,
        )

    return render(
        request,
        "academics/arm_confirm_delete.html",
        {
            "arm": arm,
        },
    )


@login_required
def subject_list(request):
    """Display all subjects."""

    subjects = Subject.objects.all()

    return render(
        request,
        "academics/subject_list.html",
        {
            "subjects": subjects,
        },
    )


@login_required
def subject_create(request):
    """Create a subject."""

    if request.method == "POST":
        form = SubjectForm(request.POST)

        if form.is_valid():
            subject = form.save()

            messages.success(
                request,
                "Subject created successfully.",
            )

            return redirect(
                "academics:subject_detail",
                pk=subject.pk,
            )

    else:
        form = SubjectForm()

    return render(
        request,
        "academics/subject_form.html",
        {
            "form": form,
            "title": "Create Subject",
        },
    )


@login_required
def subject_detail(request, pk):
    """Display subject details."""

    subject = get_object_or_404(
        Subject,
        pk=pk,
    )

    return render(
        request,
        "academics/subject_detail.html",
        {
            "subject": subject,
        },
    )


@login_required
def subject_update(request, pk):
    """Update a subject."""

    subject = get_object_or_404(
        Subject,
        pk=pk,
    )

    if request.method == "POST":
        form = SubjectForm(
            request.POST,
            instance=subject,
        )

        if form.is_valid():
            subject = form.save()

            messages.success(
                request,
                "Subject updated successfully.",
            )

            return redirect(
                "academics:subject_detail",
                pk=subject.pk,
            )

    else:
        form = SubjectForm(
            instance=subject,
        )

    return render(
        request,
        "academics/subject_form.html",
        {
            "form": form,
            "subject": subject,
            "title": "Edit Subject",
        },
    )


@login_required
def subject_delete(request, pk):
    """Delete a subject."""

    subject = get_object_or_404(
        Subject,
        pk=pk,
    )

    if request.method == "POST":
        subject.delete()

        messages.success(
            request,
            "Subject deleted successfully.",
        )

        return redirect(
            "academics:subject_list",
        )

    return render(
        request,
        "academics/subject_confirm_delete.html",
        {
            "subject": subject,
        },
    )


#####################################
@login_required
def class_subject_list(request, class_pk):
    """Display subjects assigned to a class."""

    academic_class = get_object_or_404(
        AcademicClass.objects.select_related(
            "school",
        ),
        pk=class_pk,
    )

    class_subjects = (
        ClassSubject.objects
        .filter(
            academic_class=academic_class,
        )
        .select_related("subject")
        .order_by("display_order", "subject__name")
    )

    return render(
        request,
        "academics/class_subject_list.html",
        {
            "academic_class": academic_class,
            "class_subjects": class_subjects,
        },
    )

############################################
@login_required
def class_subject_create(request, class_pk):
    """Add a subject to a class."""

    academic_class = get_object_or_404(
        AcademicClass,
        pk=class_pk,
    )

    if request.method == "POST":
        form = ClassSubjectForm(request.POST)

        if form.is_valid():

            class_subject = form.save()

            messages.success(
                request,
                "Subject added to class successfully.",
            )

            return redirect(
                "academics:class_subject_list",
                class_pk=academic_class.pk,
            )

    else:
        form = ClassSubjectForm(
            initial={
                "academic_class": academic_class,
            }
        )

    return render(
        request,
        "academics/class_subject_form.html",
        {
            "form": form,
            "academic_class": academic_class,
            "title": "Add Subject to Class",
        },
    )

###############################################
@login_required
def class_subject_update(request, pk):
    """Update a class subject."""

    class_subject = get_object_or_404(
        ClassSubject.objects.select_related(
            "academic_class",
            "subject",
        ),
        pk=pk,
    )

    if request.method == "POST":
        form = ClassSubjectForm(
            request.POST,
            instance=class_subject,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Class subject updated successfully.",
            )

            return redirect(
                "academics:class_subject_list",
                class_pk=class_subject.academic_class.pk,
            )

    else:
        form = ClassSubjectForm(
            instance=class_subject,
        )

    return render(
        request,
        "academics/class_subject_form.html",
        {
            "form": form,
            "academic_class": class_subject.academic_class,
            "class_subject": class_subject,
            "title": "Edit Class Subject",
        },
    )

#############################################
@login_required
def class_subject_delete(request, pk):
    """Remove a subject from a class."""

    class_subject = get_object_or_404(
        ClassSubject.objects.select_related(
            "academic_class",
            "subject",
        ),
        pk=pk,
    )

    academic_class = class_subject.academic_class

    if request.method == "POST":

        class_subject.delete()

        messages.success(
            request,
            "Subject removed from class.",
        )

        return redirect(
            "academics:class_subject_list",
            class_pk=academic_class.pk,
        )

    return render(
        request,
        "academics/class_subject_confirm_delete.html",
        {
            "class_subject": class_subject,
        },
    )

###############################################
@login_required
def teacher_assignment_list(request):
    """Display teacher subject assignments."""

    assignments = (
        TeacherSubjectAssignment.objects
        .select_related(
            "teacher",
            "class_arm",
            "class_arm__academic_class",
            "subject",
            "session",
        )
        .filter(is_active=True)
        .order_by(
            "class_arm__academic_class__name",
            "class_arm__name",
            "subject__name",
        )
    )

    return render(
        request,
        "academics/teacher_assignment_list.html",
        {
            "assignments": assignments,
        },
    )

################################################
@login_required
def teacher_assignment_create(request):
    """Assign a teacher to a subject."""

    if request.method == "POST":

        form = TeacherSubjectAssignmentForm(
            request.POST,
        )

        if form.is_valid():

            assignment = form.save()

            messages.success(
                request,
                "Teacher assigned successfully.",
            )

            return redirect(
                "academics:teacher_assignment_list",
            )

    else:
        form = TeacherSubjectAssignmentForm()

    return render(
        request,
        "academics/teacher_assignment_form.html",
        {
            "form": form,
            "title": "Assign Teacher",
        },
    )

########################################
@login_required
def teacher_assignment_update(request, pk):
    """Update teacher assignment."""

    assignment = get_object_or_404(
        TeacherSubjectAssignment,
        pk=pk,
    )

    if request.method == "POST":

        form = TeacherSubjectAssignmentForm(
            request.POST,
            instance=assignment,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Teacher assignment updated.",
            )

            return redirect(
                "academics:teacher_assignment_list",
            )

    else:
        form = TeacherSubjectAssignmentForm(
            instance=assignment,
        )

    return render(
        request,
        "academics/teacher_assignment_form.html",
        {
            "form": form,
            "assignment": assignment,
            "title": "Edit Teacher Assignment",
        },
    )
##################################################
@login_required
def teacher_assignment_delete(request, pk):
    """Delete teacher assignment."""

    assignment = get_object_or_404(
        TeacherSubjectAssignment.objects.select_related(
            "teacher",
            "subject",
            "class_arm",
            "class_arm__academic_class",
        ),
        pk=pk,
    )

    if request.method == "POST":

        assignment.delete()

        messages.success(
            request,
            "Teacher assignment removed.",
        )

        return redirect(
            "academics:teacher_assignment_list",
        )

    return render(
        request,
        "academics/teacher_assignment_confirm_delete.html",
        {
            "assignment": assignment,
        },
    )