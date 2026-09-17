from django.core.exceptions import PermissionDenied


class SchoolRequiredMixin:
    """
    Ensures the logged-in user belongs to a school.
    """

    def dispatch(
        self,
        request,
        *args,
        **kwargs,
    ):
        if not request.user.is_authenticated:
            return super().dispatch(
                request,
                *args,
                **kwargs,
            )

        if (
            request.user.role
            == request.user.Role.SUPER_ADMIN
        ):
            return super().dispatch(
                request,
                *args,
                **kwargs,
            )

        if request.user.school_id is None:
            raise PermissionDenied(
                "Your account is not assigned "
                "to a school."
            )

        return super().dispatch(
            request,
            *args,
            **kwargs,
        )