from django.urls import path

from . import views


app_name = "assessments"


urlpatterns = [
    path(
        "student/<int:student_id>/result/<int:term_id>/",
        views.student_result,
        name="student_result",
    ),
]