from django.urls import path

from . import views


app_name = "assessments"


urlpatterns = [
    path(
        "",
        views.assessment_dashboard,
        name="dashboard",
    ),

    # Components
    path(
        "components/",
        views.component_list,
        name="component_list",
    ),
    path(
        "components/create/",
        views.component_create,
        name="component_create",
    ),
    path(
        "components/<int:pk>/edit/",
        views.component_edit,
        name="component_edit",
    ),

    # Schemes
    path(
        "schemes/",
        views.scheme_list,
        name="scheme_list",
    ),
    path(
        "schemes/create/",
        views.scheme_create,
        name="scheme_create",
    ),
    path(
        "schemes/<int:pk>/edit/",
        views.scheme_edit,
        name="scheme_edit",
    ),
    path(
        "schemes/components/create/",
        views.scheme_component_create,
        name="scheme_component_create",
    ),

    # Student assessments
    path(
        "student-assessments/",
        views.student_assessment_list,
        name="student_assessment_list",
    ),
    path(
        "student-assessments/create/",
        views.student_assessment_create,
        name="student_assessment_create",
    ),
    path(
        "student-assessments/<int:pk>/edit/",
        views.student_assessment_edit,
        name="student_assessment_edit",
    ),

    # Traits
    path(
        "traits/",
        views.trait_list,
        name="trait_list",
    ),
    path(
        "traits/create/",
        views.trait_create,
        name="trait_create",
    ),
    path(
        "traits/student/create/",
        views.student_trait_create,
        name="student_trait_create",
    ),

    # Grade scales
    path(
        "grade-scales/",
        views.grade_scale_list,
        name="grade_scale_list",
    ),
    path(
        "grade-scales/create/",
        views.grade_scale_create,
        name="grade_scale_create",
    ),
    path(
        "grade-scales/items/create/",
        views.grade_scale_item_create,
        name="grade_scale_item_create",
    ),
]