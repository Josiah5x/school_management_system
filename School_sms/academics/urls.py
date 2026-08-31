from django.urls import path

from . import views


app_name = "academics"


urlpatterns = [
    # Academic Sessions
    path(
        "sessions/",
        views.session_list,
        name="session_list",
    ),

    path(
        "sessions/create/",
        views.session_create,
        name="session_create",
    ),

    path(
        "sessions/<int:pk>/",
        views.session_detail,
        name="session_detail",
    ),

    path(
        "sessions/<int:pk>/edit/",
        views.session_update,
        name="session_update",
    ),

    path(
        "sessions/<int:pk>/delete/",
        views.session_delete,
        name="session_delete",
    ),

    # Terms
    path(
        "terms/",
        views.term_list,
        name="term_list",
    ),

    path(
        "sessions/<int:session_pk>/terms/create/",
        views.term_create,
        name="term_create",
    ),

    path(
        "terms/create/",
        views.term_create,
        name="term_create",
    ),

    path(
        "terms/<int:pk>/edit/",
        views.term_update,
        name="term_update",
    ),

    path(
        "terms/<int:pk>/delete/",
        views.term_delete,
        name="term_delete",
    ),

############################################
    # ==========================
    # ACADEMIC CLASSES
    # ==========================

    path(
        "classes/",
        views.class_list,
        name="class_list",
    ),

    path(
        "classes/create/",
        views.class_create,
        name="class_create",
    ),

    path(
        "classes/<int:pk>/",
        views.class_detail,
        name="class_detail",
    ),

    path(
        "classes/<int:pk>/edit/",
        views.class_update,
        name="class_update",
    ),

    path(
        "classes/<int:pk>/delete/",
        views.class_delete,
        name="class_delete",
    ),


    # ==========================
    # CLASS ARMS
    # ==========================

    path(
        "classes/<int:class_pk>/arms/create/",
        views.arm_create,
        name="arm_create",
    ),

    path(
        "arms/create/",
        views.arm_create,
        name="arm_create",
    ),

    path(
        "arms/<int:pk>/edit/",
        views.arm_update,
        name="arm_update",
    ),

    path(
        "arms/<int:pk>/delete/",
        views.arm_delete,
        name="arm_delete",
    ),


    # ==========================
    # SUBJECTS
    # ==========================

    path(
        "subjects/",
        views.subject_list,
        name="subject_list",
    ),

    path(
        "subjects/create/",
        views.subject_create,
        name="subject_create",
    ),

    path(
        "subjects/<int:pk>/",
        views.subject_detail,
        name="subject_detail",
    ),

    path(
        "subjects/<int:pk>/edit/",
        views.subject_update,
        name="subject_update",
    ),

    path(
        "subjects/<int:pk>/delete/",
        views.subject_delete,
        name="subject_delete",
    ),



    # ==============================
    # CLASS SUBJECTS
    # ==============================

    path(
        "classes/<int:class_pk>/subjects/",
        views.class_subject_list,
        name="class_subject_list",
    ),

    path(
        "classes/<int:class_pk>/subjects/add/",
        views.class_subject_create,
        name="class_subject_create",
    ),

    path(
        "class-subjects/<int:pk>/edit/",
        views.class_subject_update,
        name="class_subject_update",
    ),

    path(
        "class-subjects/<int:pk>/delete/",
        views.class_subject_delete,
        name="class_subject_delete",
    ),


    # ==============================
    # TEACHER ASSIGNMENTS
    # ==============================

    path(
        "teacher-assignments/",
        views.teacher_assignment_list,
        name="teacher_assignment_list",
    ),

    path(
        "teacher-assignments/create/",
        views.teacher_assignment_create,
        name="teacher_assignment_create",
    ),

    path(
        "teacher-assignments/<int:pk>/edit/",
        views.teacher_assignment_update,
        name="teacher_assignment_update",
    ),

    path(
        "teacher-assignments/<int:pk>/delete/",
        views.teacher_assignment_delete,
        name="teacher_assignment_delete",
    ),






]




