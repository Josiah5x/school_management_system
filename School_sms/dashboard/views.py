from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):

    user = request.user
    school = user.school

    context = {
        "school": school,
        "user": user,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context,
    )
@login_required
def main(request):

    return render(
        request,
        "dashboard/main.html",
    )

@login_required
def assessment_menu(request):
 
    context = {
            "title": "Assessment Menu",
        }
    return render(
        request,
        "dashboard/assessment_menu.html", context
    )

@login_required
def academic_menu(request):
 
    context = {
    "title": "Academis Menu",
    }
    return render(
        request,
        "dashboard/academic_menu.html",context
    )

@login_required
def school_menu(request):
 
    context = {
                    "title": "Schools Menu",
                }
    return render(
        request,
        "dashboard/school_menu.html", context
    )

@login_required
def student_menu(request):
 
    context = {
                "title": "Students Menu",
            }
    return render(
        request,
        "dashboard/student_menu.html", context
    )