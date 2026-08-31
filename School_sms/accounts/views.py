from django.contrib import messages
from django.contrib.auth import (
    login,
    logout,
)
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)
from django.contrib.auth.views import LoginView
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from django.urls import reverse
from .forms import (
    LoginForm,
    ProfileForm,
    RegisterForm,
    UserPasswordChangeForm,
    UserUpdateForm,
)
from .models import User


from django.contrib.auth.views import LoginView
from django.urls import reverse

from .forms import LoginForm
from .models import User


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user

        # Super Administrator
        if user.role == User.Role.SUPER_ADMIN:
            return "/admin/"

        # School Administration
        if user.role in [ User.Role.SCHOOL_ADMIN, User.Role.PRINCIPAL, User.Role.VICE_PRINCIPAL, User.Role.HEAD_TEACHER,
        ]:
            return reverse("dashboard:dashboard")

        # Academic Staff
        if user.role in [
            User.Role.TEACHER,
            User.Role.FORM_TEACHER,
        ]:
            return reverse("dashboard:dashboard")

        # Finance
        if user.role in [
            User.Role.BURSAR,
            User.Role.ACCOUNTANT,
        ]:
            return reverse("dashboard:dashboard")

        # Administration
        if user.role == User.Role.REGISTRAR:
            return reverse("dashboard:dashboard")

        # Student
        if user.role == User.Role.STUDENT:
            return reverse("dashboard:dashboard")

        # Parent
        if user.role == User.Role.PARENT:
            return reverse("dashboard:dashboard")

        # Fallback
        return reverse("dashboard:dashboard")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            messages.success(
                request,
                "Account created successfully.",
            )

            return redirect("accounts:login")

    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
        },
    )


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)

        messages.success(
            request,
            "You have been logged out successfully.",
        )

        return redirect("accounts:login")

    return redirect("dashboard:dashboard")


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=request.user,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Your profile has been updated.",
            )

            return redirect("accounts:profile")

    else:
        form = ProfileForm(
            instance=request.user,
        )

    return render(
        request,
        "accounts/profile.html",
        {
            "form": form,
            "user_profile": request.user,
        },
    )


@login_required
def change_password(request):
    if request.method == "POST":
        form = UserPasswordChangeForm(
            request.user,
            request.POST,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Password changed successfully.",
            )

            return redirect("accounts:profile")

    else:
        form = UserPasswordChangeForm(
            request.user,
        )

    return render(
        request,
        "accounts/change_password.html",
        {
            "form": form,
        },
    )


def is_admin(user):
    return (
        user.is_authenticated
        and (
            user.is_superuser
            or user.role
            in [
                User.Role.SUPER_ADMIN,
                User.Role.SCHOOL_ADMIN,
            ]
        )
    )


@login_required
@user_passes_test(is_admin)
def user_list(request):
    users = (
        User.objects
        .all()
        .order_by(
            "first_name",
            "last_name",
        )
    )

    query = request.GET.get(
        "q",
        "",
    ).strip()

    role = request.GET.get(
        "role",
        "",
    )

    if query:
        users = users.filter(
            username__icontains=query,
        ) | users.filter(
            first_name__icontains=query,
        ) | users.filter(
            last_name__icontains=query,
        ) | users.filter(
            email__icontains=query,
        )

    if role:
        users = users.filter(
            role=role,
        )

    return render(
        request,
        "accounts/user_list.html",
        {
            "users": users,
            "roles": User.Role.choices,
        },
    )


@login_required
@user_passes_test(is_admin)
def user_create(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            messages.success(
                request,
                f"User {user.display_name} created.",
            )

            return redirect(
                "accounts:user_list",
            )

    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/user_form.html",
        {
            "form": form,
            "title": "Create User",
        },
    )


@login_required
@user_passes_test(is_admin)
def user_update(request, pk):
    user = get_object_or_404(
        User,
        pk=pk,
    )

    if request.method == "POST":
        form = UserUpdateForm(
            request.POST,
            request.FILES,
            instance=user,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "User updated successfully.",
            )

            return redirect(
                "accounts:user_list",
            )

    else:
        form = UserUpdateForm(
            instance=user,
        )

    return render(
        request,
        "accounts/user_form.html",
        {
            "form": form,
            "title": "Edit User",
            "target_user": user,
        },
    )