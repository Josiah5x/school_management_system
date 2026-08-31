from django.urls import path

from . import views


app_name = "dashboard"


urlpatterns = [
    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),
    path(
        "assessment_menu/",
        views.assessment_menu,
        name="assessment_menu",
    ),
    path(
        "school_menu/",
        views.school_menu,
        name="school_menu",
    ),
    path(
        "student_menu/",
        views.student_menu,
        name="student_menu",
    ),
    path(
        "academic_menu/",
        views.academic_menu,
        name="academic_menu",
    ),
]