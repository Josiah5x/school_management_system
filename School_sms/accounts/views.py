from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import LoginForm
from .forms import UserCreateForm
from .forms import UserUpdateForm


User = get_user_model()


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user

        if user.role == User.Role.SUPER_ADMIN:
            return "/schools/"

        return "/dashboard/"


@login_required
def user_list(request):
    user = request.user

    users = (
        User.objects
        .select_related("school")
        .order_by(
            "school__name",
            "first_name",
            "last_name",
        )
    )

    # Super Admin can see users
    # from every school.
    if user.role != User.Role.SUPER_ADMIN:

        if user.school_id is None:
            raise PermissionDenied(
                "Your account is not assigned "
                "to a school."
            )

        users = users.filter(
            school_id=user.school_id,
        )

    query = request.GET.get(
        "q",
        "",
    ).strip()

    if query:
        users = users.filter(
            Q(username__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
            | Q(phone__icontains=query)
            | Q(staff_id__icontains=query)
        )

    role = request.GET.get(
        "role",
        "",
    ).strip()

    if role:
        users = users.filter(
            role=role,
        )

    school_id = request.GET.get(
        "school",
        "",
    ).strip()

    if (
        school_id
        and user.role == User.Role.SUPER_ADMIN
    ):
        users = users.filter(
            school_id=school_id,
        )

    context = {
        "users": users,
        "query": query,
        "role": role,
        "school_id": school_id,
        "roles": User.Role.choices,
    }

    return render(
        request,
        "accounts/user_list.html",
        context,
    )


@login_required
def user_create(request):

    user = request.user

    # Only authorized administrators
    # should create accounts.
    allowed_roles = [
        User.Role.SUPER_ADMIN,
        User.Role.SCHOOL_ADMIN,
    ]

    if user.role not in allowed_roles:
        raise PermissionDenied(
            "You do not have permission "
            "to create users."
        )

    if request.method == "POST":

        form = UserCreateForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            new_user = form.save(
                commit=False,
            )

            # School Admin cannot create
            # a user for another school.
            if (user.role == User.Role.SCHOOL_ADMIN):

                new_user.school = user.school
                # if (
                #     new_user.school_id
                #     != user.school_id
                # ):
                #     raise PermissionDenied(
                #         "You can only create users "
                #         "for your own school."
                #     )

            new_user.save()

            messages.success(
                request,
                (
                    f"User "
                    f"{new_user.display_name} "
                    "created successfully."
                ),
            )

            return redirect(
                "accounts:user_detail",
                pk=new_user.pk,
            )

    else:

        form = UserCreateForm()

        # School Admin should only see
        # their own school.
        if (
            user.role
            == User.Role.SCHOOL_ADMIN
        ):
            form.fields[
                "school"
            ].queryset = (
                form.fields[
                    "school"
                ].queryset.filter(
                    pk=user.school_id,
                )
            )

            form.fields[
                "school"
            ].initial = user.school_id

            form.fields[
                "school"
            ].disabled = True

    return render(
        request,
        "accounts/user_form.html",
        {
            "form": form,
            "title": "Create User",
        },
    )



def register(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = UserCreateForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            user = form.save()

            return redirect("accounts:login")

    else:
        form = UserCreateForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
            "title": "Create Account",
        },
    )

@login_required
def user_update(request, pk):
    current_user = request.user

    target_user = get_object_or_404(
        User.objects.select_related(
            "school",
        ),
        pk=pk,
    )

    # Super Admin can edit anyone.
    if (
        current_user.role
        == User.Role.SUPER_ADMIN
    ):
        pass

    # School Admin can only edit
    # users in their school.
    elif (
        current_user.role
        == User.Role.SCHOOL_ADMIN
    ):
        if (
            target_user.school_id
            != current_user.school_id
        ):
            raise PermissionDenied(
                "You cannot edit users "
                "from another school."
            )

    else:
        raise PermissionDenied(
            "You do not have permission "
            "to edit users."
        )

    if request.method == "POST":

        form = UserUpdateForm(
            request.POST,
            request.FILES,
            instance=target_user,
        )

        if form.is_valid():

            updated_user = form.save(
                commit=False,
            )

            # School Admin cannot move
            # users to another school.
            if (
                current_user.role
                == User.Role.SCHOOL_ADMIN
            ):
                updated_user.school = (
                    current_user.school
                )

                # School Admin cannot
                # promote someone to
                # Super Admin.
                if (
                    updated_user.role
                    == User.Role.SUPER_ADMIN
                ):
                    raise PermissionDenied(
                        "You cannot assign "
                        "Super Administrator role."
                    )

            updated_user.save()

            messages.success(
                request,
                "User updated successfully.",
            )

            return redirect(
                "accounts:user_detail",
                pk=target_user.pk,
            )

    else:

        form = UserUpdateForm(
            instance=target_user,
        )

        if (
            current_user.role
            == User.Role.SCHOOL_ADMIN
        ):
            form.fields[
                "school"
            ].queryset = (
                form.fields[
                    "school"
                ].queryset.filter(
                    pk=current_user.school_id,
                )
            )

            form.fields[
                "school"
            ].initial = (
                current_user.school_id
            )

            form.fields[
                "school"
            ].disabled = True

            # School Admin cannot
            # assign Super Admin.
            form.fields[
                "role"
            ].choices = [
                choice
                for choice in
                User.Role.choices
                if choice[0]
                != User.Role.SUPER_ADMIN
            ]

    return render(
        request,
        "accounts/user_form.html",
        {
            "form": form,
            "title": "Edit User",
            "user_object": target_user,
        },
    )

@login_required
def user_detail(request, pk):
    current_user = request.user

    user = get_object_or_404(
        User.objects.select_related(
            "school",
        ),
        pk=pk,
    )

    if (
        current_user.role
        != User.Role.SUPER_ADMIN
    ):
        if (
            current_user.school_id
            != user.school_id
        ):
            raise PermissionDenied(
                "You cannot view users "
                "from another school."
            )

    return render(
        request,
        "accounts/user_detail.html",
        {
            "user_object": user,
        },
    )



@login_required
def user_toggle_active(request, pk):
    current_user = request.user

    user = get_object_or_404(
        User,
        pk=pk,
    )

    if (
        current_user.role
        != User.Role.SUPER_ADMIN
    ):
        if (
            current_user.school_id
            != user.school_id
        ):
            raise PermissionDenied(
                "You cannot modify users "
                "from another school."
            )

        if (
            current_user.role
            != User.Role.SCHOOL_ADMIN
        ):
            raise PermissionDenied(
                "You do not have permission "
                "to modify users."
            )

    if request.method != "POST":
        return redirect(
            "accounts:user_detail",
            pk=user.pk,
        )

    # Prevent disabling yourself.
    if user.pk == current_user.pk:
        messages.error(
            request,
            "You cannot deactivate your "
            "own account.",
        )

        return redirect(
            "accounts:user_detail",
            pk=user.pk,
        )

    user.is_active = not user.is_active

    user.save(
        update_fields=[
            "is_active",
            "updated_at",
        ]
    )

    if user.is_active:
        messages.success(
            request,
            "User account activated.",
        )
    else:
        messages.warning(
            request,
            "User account deactivated.",
        )

    return redirect(
        "accounts:user_detail",
        pk=user.pk,
    )



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