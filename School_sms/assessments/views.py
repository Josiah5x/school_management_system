from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import (
    AssessmentSchemeComponent,
    StudentAssessment,
    StudentTraitAssessment,
    SubjectResult,
    TermResult,
)

@login_required
def student_result(
    request,
    student_id,
    term_id,
):
    subject_results = (
        SubjectResult.objects
        .filter(
            student_id=student_id,
            term_id=term_id,
        )
        .select_related(
            "student",
            "enrollment",
            "enrollment__class_arm",
            "class_subject",
            "class_subject__subject",
        )
        .order_by(
            "class_subject__display_order",
        )
    )

    term_result = (
        TermResult.objects
        .filter(
            student_id=student_id,
            term_id=term_id,
        )
        .first()
    )

    traits = (
        StudentTraitAssessment.objects
        .filter(
            student_id=student_id,
            term_id=term_id,
        )
        .select_related(
            "trait",
        )
        .order_by(
            "trait__category",
            "trait__display_order",
        )
    )

    affective_traits = [
        item
        for item in traits
        if item.trait.category == "affective"
    ]

    psychomotor_traits = [
        item
        for item in traits
        if item.trait.category == "psychomotor"
    ]

    student = (
        subject_results
        .first()
        .student
    )

    enrollment = (
        subject_results
        .first()
        .enrollment
    )

    term = (
        subject_results
        .first()
        .term
    )

    return render(
        request,
        "assessments/student_result.html",
        {
            "student": student,
            "enrollment": enrollment,
            "term": term,
            "subject_results": subject_results,
            "term_result": term_result,
            "affective_traits": affective_traits,
            "psychomotor_traits": psychomotor_traits,
        },
    )