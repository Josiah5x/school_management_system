from django.urls import path

from . import views


app_name = "accounts"


urlpatterns = [
    path(
        "login/",
        views.UserLoginView.as_view(),
        name="login",
    ),

    path(
        "users/",
        views.user_list,
        name="user_list",
    ),

    path(
        "register",
        views.register,
        name="register",
    ),

    path(
        "users/<int:pk>/",
        views.user_detail,
        name="user_detail",
    ),

    path(
        "users/<int:pk>/edit/",
        views.user_update,
        name="user_update",
    ),

    path(
        "users/<int:pk>/toggle-active/",
        views.user_toggle_active,
        name="user_toggle_active",
    ),
]