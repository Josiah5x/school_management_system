from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    context = {
        "student_count": 0,
        "teacher_count": 0,
        "class_arm_count": 0,
        "subject_count": 0,
        "active_session": None,
        "active_term": None,
        "terms": [],
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context,
    )
@login_required
def assessment_menu(request):
 

    return render(
        request,
        "dashboard/assessment_menu.html"
    )
@login_required
def academic_menu(request):
 

    return render(
        request,
        "dashboard/academic_menu.html"
    )
@login_required
def school_menu(request):
 

    return render(
        request,
        "dashboard/school_menu.html"
    )
@login_required
def student_menu(request):
 

    return render(
        request,
        "dashboard/student_menu.html"
    )