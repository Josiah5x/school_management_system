from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import AssessmentComponentForm
from .forms import AssessmentSchemeComponentForm
from .forms import AssessmentSchemeForm
from .forms import AssessmentTraitForm
from .forms import GradeScaleForm
from .forms import GradeScaleItemForm
from .forms import StudentAssessmentForm
from .forms import StudentTraitAssessmentForm

from .models import AssessmentComponent
from .models import AssessmentScheme
from .models import AssessmentSchemeComponent
from .models import AssessmentTrait
from .models import GradeScale
from .models import GradeScaleItem
from .models import StudentAssessment
from .models import StudentTraitAssessment


@login_required
def assessment_dashboard(request):
    context = {
        "component_count": AssessmentComponent.objects.filter(
            is_active=True
        ).count(),

        "scheme_count": AssessmentScheme.objects.filter(
            is_active=True
        ).count(),

        "trait_count": AssessmentTrait.objects.filter(
            is_active=True
        ).count(),

        "grade_scale_count": GradeScale.objects.filter(
            is_active=True
        ).count(),

        "assessment_count": StudentAssessment.objects.count(),

        "result_count": StudentAssessment.objects.filter(
            approved=True
        ).count(),
    }

    return render(
        request,
        "assessments/dashboard.html",
        context,
    )


# ==========================================================
# ASSESSMENT COMPONENTS
# ==========================================================

@login_required
def component_list(request):
    components = (
        AssessmentComponent.objects
        .filter(is_active=True)
        .order_by("display_order", "name")
    )

    return render(
        request,
        "assessments/components/list.html",
        {
            "components": components,
        },
    )


@login_required
def component_create(request):
    if request.method == "POST":
        form = AssessmentComponentForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Assessment component created successfully.",
            )

            return redirect(
                "assessments:component_list"
            )
    else:
        form = AssessmentComponentForm()

    return render(
        request,
        "assessments/components/form.html",
        {
            "form": form,
            "title": "Create Assessment Component",
        },
    )


@login_required
def component_edit(request, pk):
    component = get_object_or_404(
        AssessmentComponent,
        pk=pk,
    )

    if request.method == "POST":
        form = AssessmentComponentForm(
            request.POST,
            instance=component,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Assessment component updated successfully.",
            )

            return redirect(
                "assessments:component_list"
            )
    else:
        form = AssessmentComponentForm(
            instance=component
        )

    return render(
        request,
        "assessments/components/form.html",
        {
            "form": form,
            "title": "Edit Assessment Component",
        },
    )


# ==========================================================
# ASSESSMENT SCHEMES
# ==========================================================

@login_required
def scheme_list(request):
    schemes = (
        AssessmentScheme.objects
        .filter(is_active=True)
        .prefetch_related(
            "components__component"
        )
        .order_by("name")
    )

    return render(
        request,
        "assessments/schemes/list.html",
        {
            "schemes": schemes,
        },
    )


@login_required
def scheme_create(request):
    if request.method == "POST":
        form = AssessmentSchemeForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Assessment scheme created successfully.",
            )

            return redirect(
                "assessments:scheme_list"
            )
    else:
        form = AssessmentSchemeForm()

    return render(
        request,
        "assessments/schemes/form.html",
        {
            "form": form,
            "title": "Create Assessment Scheme",
        },
    )


@login_required
def scheme_edit(request, pk):
    scheme = get_object_or_404(
        AssessmentScheme,
        pk=pk,
    )

    if request.method == "POST":
        form = AssessmentSchemeForm(
            request.POST,
            instance=scheme,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Assessment scheme updated successfully.",
            )

            return redirect(
                "assessments:scheme_list"
            )
    else:
        form = AssessmentSchemeForm(
            instance=scheme
        )

    return render(
        request,
        "assessments/schemes/form.html",
        {
            "form": form,
            "title": "Edit Assessment Scheme",
        },
    )


# ==========================================================
# SCHEME COMPONENTS
# ==========================================================

@login_required
def scheme_component_create(request):
    if request.method == "POST":
        form = AssessmentSchemeComponentForm(
            request.POST
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Scheme component added successfully.",
            )

            return redirect(
                "assessments:scheme_list"
            )
    else:
        form = AssessmentSchemeComponentForm()

    return render(
        request,
        "assessments/schemes/component_form.html",
        {
            "form": form,
            "title": "Add Scheme Component",
        },
    )


# ==========================================================
# STUDENT ASSESSMENTS
# ==========================================================

@login_required
def student_assessment_list(request):
    assessments = (
        StudentAssessment.objects
        .select_related(
            "student",
            "enrollment",
            "term",
            "class_subject__subject",
            "component__component",
            "assessment_scheme",
        )
        .order_by(
            "-term__session__start_date",
            "student",
        )
    )

    return render(
        request,
        "assessments/student_assessments/list.html",
        {
            "assessments": assessments,
        },
    )


@login_required
def student_assessment_create(request):
    if request.method == "POST":
        form = StudentAssessmentForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():
            assessment = form.save(
                commit=False
            )

            assessment.entered_by = request.user
            assessment.save()

            messages.success(
                request,
                "Student assessment saved successfully.",
            )

            return redirect(
                "assessments:student_assessment_list"
            )
    else:
        form = StudentAssessmentForm(
            user=request.user
        )

    return render(
        request,
        "assessments/student_assessments/form.html",
        {
            "form": form,
            "title": "Enter Student Assessment",
        },
    )


@login_required
def student_assessment_edit(request, pk):
    assessment = get_object_or_404(
        StudentAssessment,
        pk=pk,
    )

    if request.method == "POST":
        form = StudentAssessmentForm(
            request.POST,
            instance=assessment,
            user=request.user,
        )

        if form.is_valid():
            assessment = form.save(
                commit=False
            )

            assessment.entered_by = request.user
            assessment.save()

            messages.success(
                request,
                "Student assessment updated.",
            )

            return redirect(
                "assessments:student_assessment_list"
            )
    else:
        form = StudentAssessmentForm(
            instance=assessment,
            user=request.user,
        )

    return render(
        request,
        "assessments/student_assessments/form.html",
        {
            "form": form,
            "title": "Edit Student Assessment",
        },
    )


# ==========================================================
# TRAITS
# ==========================================================

@login_required
def trait_list(request):
    traits = (
        AssessmentTrait.objects
        .filter(is_active=True)
        .order_by(
            "category",
            "display_order",
            "name",
        )
    )

    return render(
        request,
        "assessments/traits/list.html",
        {
            "traits": traits,
        },
    )


@login_required
def trait_create(request):
    if request.method == "POST":
        form = AssessmentTraitForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Assessment trait created.",
            )

            return redirect(
                "assessments:trait_list"
            )
    else:
        form = AssessmentTraitForm()

    return render(
        request,
        "assessments/traits/form.html",
        {
            "form": form,
            "title": "Create Assessment Trait",
        },
    )


@login_required
def student_trait_create(request):
    if request.method == "POST":
        form = StudentTraitAssessmentForm(
            request.POST
        )

        if form.is_valid():
            assessment = form.save(
                commit=False
            )

            assessment.assessed_by = request.user
            assessment.save()

            messages.success(
                request,
                "Trait assessment saved.",
            )

            return redirect(
                "assessments:trait_list"
            )
    else:
        form = StudentTraitAssessmentForm()

    return render(
        request,
        "assessments/traits/student_form.html",
        {
            "form": form,
            "title": "Assess Student Trait",
        },
    )


# ==========================================================
# GRADE SCALES
# ==========================================================

@login_required
def grade_scale_list(request):
    scales = (
        GradeScale.objects
        .filter(is_active=True)
        .prefetch_related("items")
    )

    return render(
        request,
        "assessments/gradescales/list.html",
        {
            "scales": scales,
        },
    )


@login_required
def grade_scale_create(request):
    if request.method == "POST":
        form = GradeScaleForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Grade scale created successfully.",
            )

            return redirect(
                "assessments:grade_scale_list"
            )
    else:
        form = GradeScaleForm()

    return render(
        request,
        "assessments/gradescales/form.html",
        {
            "form": form,
            "title": "Create Grade Scale",
        },
    )


@login_required
def grade_scale_item_create(request):
    if request.method == "POST":
        form = GradeScaleItemForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Grade scale item added.",
            )

            return redirect(
                "assessments:grade_scale_list"
            )
    else:
        form = GradeScaleItemForm()

    return render(
        request,
        "assessments/gradescales/item_form.html",
        {
            "form": form,
            "title": "Add Grade Scale Item",
        },
    )