from django.urls import path

from . import views


app_name = "students"


urlpatterns = [

    # -------------------------
    # Students
    # -------------------------

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),

    path(
        
        "",
        views.student_list,
        name="student_list",
    ),

    path(
        "create/",
        views.student_create,
        name="student_create",
    ),

    path(
        "<int:pk>/",
        views.student_detail,
        name="student_detail",
    ),

    path(
        "<int:pk>/edit/",
        views.student_update,
        name="student_update",
    ),

    path(
        "<int:pk>/delete/",
        views.student_delete,
        name="student_delete",
    ),

    # -------------------------
    # Guardians
    # -------------------------

    path(
        "guardians/",
        views.guardian_list,
        name="guardian_list",
    ),

    path(
        "guardians/create/",
        views.guardian_create,
        name="guardian_create",
    ),

    path(
        "guardians/<int:pk>/",
        views.guardian_detail,
        name="guardian_detail",
    ),

    path(
        "guardians/<int:pk>/edit/",
        views.guardian_update,
        name="guardian_update",
    ),

    path(
        "guardians/<int:pk>/deactivate/",
        views.guardian_deactivate,
        name="guardian_deactivate",
    ),

    # -------------------------
    # Student / Guardian
    # -------------------------

    path(
        "<int:student_pk>/guardians/add/",
        views.student_guardian_create,
        name="student_guardian_create",
    ),

    path(
        "<int:student_pk>/guardians/"
        "<int:relation_pk>/delete/",
        views.student_guardian_delete,
        name="student_guardian_delete",
    ),

    # -------------------------
    # Enrollment
    # -------------------------

    path(
        "enrollments/",
        views.enrollment_list,
        name="enrollment_list",
    ),

    path(
        "enrollments/create/",
        views.enrollment_create,
        name="enrollment_create",
    ),

    path(
        "enrollments/<int:pk>/edit/",
        views.enrollment_update,
        name="enrollment_update",
    ),
]