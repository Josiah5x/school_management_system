from django.urls import path

from .views import (
    UserLoginView,
    change_password,
    logout_view,
    profile,
    register,
    user_create,
    user_list,
    user_update,
)


app_name = "accounts"


urlpatterns = [
    path(
        "login/",
        UserLoginView.as_view(),
        name="login",
    ),

    path(
        "register/",
        register,
        name="register",
    ),

    path(
        "logout/",
        logout_view,
        name="logout",
    ),

    path(
        "profile/",
        profile,
        name="profile",
    ),

    path(
        "password/change/",
        change_password,
        name="change_password",
    ),

    path(
        "users/",
        user_list,
        name="user_list",
    ),

    path(
        "users/create/",
        user_create,
        name="user_create",
    ),

    path(
        "users/<int:pk>/edit/",
        user_update,
        name="user_update",
    ),
]