from decimal import Decimal
from typing import Iterable

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import (
    Avg,
    F,
    Window,
)
from django.db.models.functions import DenseRank
from collections import defaultdict
from django.db.models import Avg

from .models import (
    AssessmentScheme,
    AssessmentSchemeComponent,
    GradeScale,
    GradeScaleItem,
    StudentAssessment,
    SubjectResult,
    StudentTraitAssessment,
    TermResult,
)

HUNDRED = Decimal("100.00")


def validate_assessment_scheme(
    scheme: AssessmentScheme,
) -> None:
    """
    Validate that all active components in a scheme
    add up to exactly 100 marks.
    """

    components = list(scheme.components.select_related("component").all())

    if not components:
        raise ValidationError(
            "Assessment scheme must contain " "at least one component."
        )

    total = sum(
        (item.maximum_score for item in components),
        Decimal("0.00"),
    )

    if total != HUNDRED:
        raise ValidationError(
            f"Assessment scheme '{scheme.name}' "
            f"must total 100 marks. "
            f"Current total: {total}."
        )


def get_scheme_components(
    scheme: AssessmentScheme,
) -> list[AssessmentSchemeComponent]:
    """
    Return all components belonging to a scheme
    with their component definitions loaded.
    """

    return list(scheme.components.select_related("component").order_by("display_order"))


######################################################
def calculate_total_score(
    assessments: Iterable[StudentAssessment],
) -> Decimal:
    """
    Calculate the student's raw total from all
    assessment components.
    """

    total = sum(
        (assessment.score for assessment in assessments),
        Decimal("0.00"),
    )

    return total.quantize(Decimal("0.01"))


##############################################
def calculate_percentage(
    score: Decimal,
    maximum_score: Decimal,
) -> Decimal:
    """
    Convert a raw score into a percentage.

    Example:
        68 / 80 = 85%
    """

    if maximum_score <= 0:
        raise ValidationError("Maximum score must be greater than zero.")

    percentage = (score / maximum_score) * HUNDRED

    return percentage.quantize(Decimal("0.01"))


########################################
# def get_grade(
#     score: Decimal,
#     scale: GradeScale,
# ) -> GradeScaleItem:
#     """
#     Find the grading scale item matching a
#     student's score.
#     """

#     grade_item = (
#         scale.items.filter(
#             minimum_score__lte=score,
#             maximum_score__gte=score,
#         )
#         .order_by("-minimum_score")
#         .first()
#     )

#     if grade_item is None:
#         raise ValidationError(
#             f"No grade exists for score {score} " f"on scale '{scale.name}'."
#         )

#     return grade_item


####################################
def get_active_grade_scale(
    scale_type: str,
) -> GradeScale:
    """
    Return the active grading scale for a tier.
    """

    scale = (
        GradeScale.objects.filter(
            scale_type=scale_type,
            is_active=True,
        )
        .prefetch_related("items")
        .first()
    )

    if scale is None:
        raise ValidationError(f"No active grading scale exists " f"for '{scale_type}'.")

    return scale


#############################################
def get_student_assessments(
    student,
    term,
    class_subject,
):
    """
    Retrieve all assessment components for one
    student, term and subject in a single query.
    """

    return list(
        StudentAssessment.objects.filter(
            student=student,
            term=term,
            class_subject=class_subject,
        )
        .select_related(
            "component",
            "component__component",
        )
        .order_by(
            "component__display_order",
        )
    )


##############################################
def determine_student_grade(
    student,
    term,
    percentage: Decimal,
):
    """
    Determine the grading scale using the
    student's class for the specified session.
    """

    enrollment = get_student_enrollment_for_term(
        student=student,
        term=term,
    )

    tier = enrollment.class_arm.academic_class.tier

    if tier == "primary":
        scale_type = GradeScale.ScaleType.PRIMARY
    else:
        scale_type = GradeScale.ScaleType.SECONDARY

    scale = get_active_grade_scale(scale_type)

    return get_grade(
        percentage,
        scale,
    )

###########################################
def get_student_enrollment_for_term(
    student,
    term,
):
    """
    Find the student's enrollment for the
    academic session containing the term.
    """

    return student.enrollments.select_related(
        "class_arm",
        "class_arm__academic_class",
    ).get(
        session=term.session,
    )

#########################################
def calculate_subject_result_data(
    student,
    term,
    class_subject,
):
    """
    Calculate the complete result for one subject.
    """

    assessments = get_student_assessments(
        student=student,
        term=term,
        class_subject=class_subject,
    )

    if not assessments:
        raise ValidationError("No assessment scores found.")

    scheme = assessments[0].component.scheme

    validate_assessment_scheme(scheme)

    total = calculate_total_score(assessments)

    maximum_total = sum(
        (assessment.component.maximum_score for assessment in assessments),
        Decimal("0.00"),
    )

    percentage = calculate_percentage(
        total,
        maximum_total,
    )

    return {
        "total_score": percentage,
        "raw_score": total,
        "maximum_score": maximum_total,
        "assessments": assessments,
    }


##################################
@transaction.atomic
def generate_subject_result(
    student,
    term,
    class_subject,
):
    data = calculate_subject_result_data(
        student=student,
        term=term,
        class_subject=class_subject,
    )

    grade_item = determine_student_grade(
        student=student,
        term=term,
        percentage=data["total_score"],
    )

    enrollment = get_student_enrollment_for_term(
        student=student,
        term=term,
    )

    result, _ = SubjectResult.objects.update_or_create(
        student=student,
        term=term,
        class_subject=class_subject,
        defaults={
            "enrollment": enrollment,
            "total_score": data["total_score"],
            "grade": grade_item.grade,
            "grade_point": grade_item.grade_point,
            "remark": grade_item.remark,
        },
    )

    return result


#####################################
def get_student_enrollment_for_term(
    student,
    term,
):
    """
    Find the student's enrollment for the
    academic session containing the term.
    """

    return student.enrollments.select_related(
        "class_arm",
        "class_arm__academic_class",
    ).get(
        session=term.session,
    )


##############################################
def calculate_class_subject_average(
    term,
    class_subject,
):
    """
    Calculate the average score for a subject
    across the class using a database aggregation.
    """

    result = SubjectResult.objects.filter(
        term=term,
        class_subject=class_subject,
    ).aggregate(average=Avg("total_score"))

    return result["average"]


#######################################
def determine_student_grade(
    student,
    term,
    percentage: Decimal,
):
    """
    Determine the grading scale using the
    student's class for the specified session.
    """

    enrollment = get_student_enrollment_for_term(
        student=student,
        term=term,
    )

    tier = enrollment.class_arm.academic_class.tier

    if tier == "primary":
        scale_type = GradeScale.ScaleType.PRIMARY
    else:
        scale_type = GradeScale.ScaleType.SECONDARY

    scale = get_active_grade_scale(scale_type)

    return get_grade(
        percentage,
        scale,
    )


##################################################


def get_subject_rankings(
    term,
    class_subject,
):
    """
    Rank students in a subject within their
    class arm.
    """

    queryset = (
        SubjectResult.objects.filter(
            term=term,
            class_subject=class_subject,
        )
        .annotate(
            position_rank=Window(
                expression=DenseRank(),
                order_by=F("total_score").desc(),
            )
        )
        .select_related(
            "student",
            "enrollment",
            "enrollment__class_arm",
        )
        .order_by(
            "position_rank",
            "student__last_name",
        )
    )

    return queryset


def validate_trait_rating(
    rating: int,
) -> None:
    """
    Validate the Nigerian 1-5 trait rating.
    """

    if not 1 <= rating <= 5:
        raise ValidationError("Trait rating must be between 1 and 5.")


def get_trait_rating_label(
    rating: int,
) -> str:
    """
    Convert a 1-5 rating into a display label.
    """

    labels = {
        5: "Excellent",
        4: "Very Good",
        3: "Good",
        2: "Fair",
        1: "Poor",
    }

    validate_trait_rating(rating)

    return labels[rating]


######################################
@transaction.atomic
def save_trait_assessment(
    student,
    enrollment,
    term,
    trait,
    rating,
    assessed_by=None,
    teacher_comment="",
):
    """
    Create or update a student's affective or
    psychomotor assessment.
    """

    validate_trait_rating(rating)

    if enrollment.student_id != student.id:
        raise ValidationError("Enrollment does not belong to student.")

    if enrollment.session_id != term.session_id:
        raise ValidationError(
            "Enrollment and term must belong to " "the same academic session."
        )

    assessment, _ = StudentTraitAssessment.objects.update_or_create(
        student=student,
        term=term,
        trait=trait,
        defaults={
            "enrollment": enrollment,
            "rating": rating,
            "assessed_by": assessed_by,
            "teacher_comment": teacher_comment,
        },
    )

    return assessment

####################################################

def get_student_trait_assessments(
    student,
    term,
):
    """
    Retrieve all affective and psychomotor assessments
    for a student and term efficiently.
    """

    return (
        StudentTraitAssessment.objects.filter(
            student=student,
            term=term,
        )
        .select_related(
            "trait",
            "enrollment",
            "assessed_by",
        )
        .order_by(
            "trait__category",
            "trait__display_order",
        )
    )


##################################################


def group_student_traits(
    student,
    term,
):
    """
    Group trait assessments into affective and
    psychomotor categories.
    """

    assessments = get_student_trait_assessments(
        student=student,
        term=term,
    )

    grouped = defaultdict(list)

    for assessment in assessments:
        grouped[assessment.trait.category].append(assessment)

    return dict(grouped)


##############################################


def get_trait_domain_averages(
    student,
    term,
):
    """
    Calculate average rating for affective and
    psychomotor domains.
    """

    results = (
        StudentTraitAssessment.objects.filter(
            student=student,
            term=term,
        )
        .values(
            "trait__category",
        )
        .annotate(
            average_rating=Avg("rating"),
        )
    )

    return {item["trait__category"]: item["average_rating"] for item in results}


##############################################


def get_subject_rankings(
    term,
    class_subject,
):
    """
    Rank students in a subject within their class arm.

    Students with equal scores receive the same position.
    """

    return (
        SubjectResult.objects.filter(
            term=term,
            class_subject=class_subject,
        )
        .select_related(
            "student",
            "enrollment",
            "enrollment__class_arm",
        )
        .annotate(
            position_rank=Window(
                expression=DenseRank(),
                partition_by=[
                    F("enrollment__class_arm_id"),
                ],
                order_by=F("total_score").desc(),
            ),
        )
        .order_by(
            "position_rank",
            "student__last_name",
            "student__first_name",
        )
    )

###########################################

@transaction.atomic
def update_subject_positions(
    term,
    class_subject,
):
    """
    Calculate and persist subject positions.
    """

    rankings = get_subject_rankings(
        term=term,
        class_subject=class_subject,
    )

    results = []

    for result in rankings:
        result.position = result.position_rank
        results.append(result)

    SubjectResult.objects.bulk_update(
        results,
        ["position"],
        batch_size=500,
    )

    return results

###############################################

def calculate_student_term_average(
    student,
    term,
):
    """
    Calculate the student's average across all
    subjects for a term.
    """

    result = (
        SubjectResult.objects
        .filter(
            student=student,
            term=term,
        )
        .aggregate(
            average=Avg("total_score"),
        )
    )

    average = result["average"]

    if average is None:
        return Decimal("0.00")

    return average.quantize(
        Decimal("0.01")
    )


###################################
@transaction.atomic
def generate_term_result(
    student,
    term,
):
    """
    Generate the student's overall result for a term.
    """

    subject_results = list(
        SubjectResult.objects
        .filter(
            student=student,
            term=term,
        )
        .select_related(
            "enrollment",
            "class_subject",
            "class_subject__subject",
        )
    )

    if not subject_results:
        raise ValidationError(
            "No subject results exist for this student."
        )

    total_score = sum(
        (
            result.total_score
            for result in subject_results
        ),
        Decimal("0.00"),
    )

    subject_count = len(subject_results)

    average_score = (
        total_score / subject_count
    ).quantize(
        Decimal("0.01")
    )

    enrollment = (
        student.enrollments
        .select_related("class_arm")
        .get(
            session=term.session,
        )
    )

    term_result, _ = (
        TermResult.objects.update_or_create(
            student=student,
            term=term,
            defaults={
                "enrollment": enrollment,
                "total_score": total_score,
                "subject_count": subject_count,
                "average_score": average_score,
            },
        )
    )

    return term_result

###################################################
def calculate_class_average(
    term,
    class_arm,
):
    """
    Calculate the overall average for a class arm.
    """

    result = (
        TermResult.objects
        .filter(
            term=term,
            enrollment__class_arm=class_arm,
        )
        .aggregate(
            average=Avg("average_score"),
        )
    )

    average = result["average"]

    if average is None:
        return Decimal("0.00")

    return average.quantize(
        Decimal("0.01")
    )

###########################################
def get_class_rankings(
    term,
    class_arm,
):
    """
    Rank students by their overall term average
    within a class arm.
    """

    return (
        TermResult.objects
        .filter(
            term=term,
            enrollment__class_arm=class_arm,
        )
        .select_related(
            "student",
            "enrollment",
            "enrollment__class_arm",
        )
        .annotate(
            position_rank=Window(
                expression=DenseRank(),
                order_by=F(
                    "average_score"
                ).desc(),
            ),
        )
        .order_by(
            "position_rank",
            "student__last_name",
            "student__first_name",
        )
    )

##############################################
@transaction.atomic
def update_class_positions(
    term,
    class_arm,
):
    """
    Calculate and save class positions.
    """

    rankings = get_class_rankings(
        term=term,
        class_arm=class_arm,
    )

    class_average = calculate_class_average(
        term=term,
        class_arm=class_arm,
    )

    results = []

    for result in rankings:
        result.position = result.position_rank
        result.class_average = class_average
        results.append(result)

    TermResult.objects.bulk_update(
        results,
        [
            "position",
            "class_average",
        ],
        batch_size=500,
    )

    return results



from django.db.models import Avg, Sum



ZERO = Decimal("0.00")


def get_grade(score, grade_scale=None):
    """
    Return the grade, grade point and remark for a score.

    Pass a GradeScale when your school has multiple
    grading scales.
    """
    if grade_scale is None:
        grade_scale = GradeScale.objects.filter(
            is_active=True,
        ).first()

    if grade_scale is None:
        return "", None, ""

    item = grade_scale.items.filter(
        min_score__lte=score,
        max_score__gte=score,
    ).first()

    if item is None:
        return "", None, ""

    return (
        item.grade,
        item.grade_point,
        item.remark,
    )


@transaction.atomic
def calculate_subject_result(
    student,
    enrollment,
    term,
    class_subject,
    grade_scale=None,
):
    """
    Calculate and save one student's result for one subject.
    """

    if enrollment.student_id != student.pk:
        raise ValidationError(
            "The enrollment does not belong to this student."
        )

    if enrollment.session_id != term.session_id:
        raise ValidationError(
            "The enrollment and term must belong to the same session."
        )

    assessments = StudentAssessment.objects.filter(
        student=student,
        enrollment=enrollment,
        term=term,
        class_subject=class_subject,
    ).select_related("component")

    # Each assessment score is already entered against
    # its scheme component's maximum score.
    total_score = assessments.aggregate(
        total=Sum("score"),
    )["total"] or ZERO

    maximum_score = sum(
        (
            assessment.component.maximum_score
            for assessment in assessments
        ),
        ZERO,
    )

    if total_score < ZERO:
        raise ValidationError("Total score cannot be negative.")

    if maximum_score and total_score > maximum_score:
        raise ValidationError(
            "The total score exceeds the configured component marks."
        )

    # Your SubjectResult model stores a score out of 100.
    # Do not silently scale a partially entered assessment.
    if maximum_score != Decimal("100.00"):
        raise ValidationError(
            "The assessment components for this subject must "
            "total 100 marks before calculating the result."
        )

    grade, grade_point, remark = get_grade(
        total_score,
        grade_scale,
    )

    result, _ = SubjectResult.objects.update_or_create(
        student=student,
        term=term,
        class_subject=class_subject,
        defaults={
            "enrollment": enrollment,
            "total_score": total_score,
            "grade": grade,
            "grade_point": grade_point,
            "remark": remark,
        },
    )

    return result


@transaction.atomic
def calculate_subject_positions(term, class_subject):
    """
    Rank students within a subject, highest score first.
    Equal scores share a position.
    """

    results = SubjectResult.objects.filter(
        term=term,
        class_subject=class_subject,
    ).order_by("-total_score", "student_id")

    previous_score = None
    position = 0

    for index, result in enumerate(results, start=1):
        if result.total_score != previous_score:
            position = index
            previous_score = result.total_score

        if result.position != position:
            result.position = position
            result.save(update_fields=["position", "updated_at"])


@transaction.atomic
def calculate_term_result(student, enrollment, term):
    """
    Calculate one student's term summary from their subject results.
    """

    if enrollment.student_id != student.pk:
        raise ValidationError(
            "The enrollment does not belong to this student."
        )

    if enrollment.session_id != term.session_id:
        raise ValidationError(
            "The enrollment and term must belong to the same session."
        )

    subject_results = SubjectResult.objects.filter(
        student=student,
        enrollment=enrollment,
        term=term,
    )

    aggregate = subject_results.aggregate(
        total=Sum("total_score"),
        average=Avg("total_score"),
    )

    subject_count = subject_results.count()
    total_score = aggregate["total"] or ZERO
    average_score = aggregate["average"] or ZERO

    term_result, _ = TermResult.objects.update_or_create(
        student=student,
        term=term,
        defaults={
            "enrollment": enrollment,
            "total_score": total_score,
            "subject_count": subject_count,
            "average_score": average_score,
            "next_term_resumption_date": (
                term.next_term_resumption_date
            ),
        },
    )

    return term_result