from django.urls import path

from . import views


app_name = "schools"


urlpatterns = [
    path(
        "",
        views.school_detail,
        name="detail",
    ),

    path(
        "create/",
        views.school_create,
        name="create",
    ),

    path(
        "edit/",
        views.school_update,
        name="update",
    ),

    path(
        "settings/",
        views.school_settings,
        name="settings",
    ),
]