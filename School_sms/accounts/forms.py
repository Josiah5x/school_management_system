from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserCreationForm,
)

from .models import User


class BootstrapFormMixin:
    """
    Automatically applies Bootstrap classes to form fields.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            widget = field.widget

            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault(
                    "class",
                    "form-check-input",
                )

            elif isinstance(widget, forms.RadioSelect):
                widget.attrs.setdefault(
                    "class",
                    "form-check-input",
                )

            elif isinstance(widget, forms.Select):
                widget.attrs.setdefault(
                    "class",
                    "form-select",
                )

            else:
                widget.attrs.setdefault(
                    "class",
                    "form-control",
                )


class LoginForm(
    BootstrapFormMixin,
    AuthenticationForm,
):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter username",
                "autocomplete": "username",
            }
        ),
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter password",
                "autocomplete": "current-password",
            }
        ),
    )


class RegisterForm(
    BootstrapFormMixin,
    UserCreationForm,
):
    first_name = forms.CharField(
        max_length=150,
        required=True,
    )

    last_name = forms.CharField(
        max_length=150,
        required=True,
    )

    email = forms.EmailField(
        required=True,
    )

    role = forms.ChoiceField(
        choices=User.Role.choices,
        widget=forms.RadioSelect,
    )

    phone = forms.CharField(
        max_length=20,
        required=False,
    )

    class Meta:
        model = User

        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "phone",
            "password1",
            "password2",
        ]


class UserUpdateForm(
    BootstrapFormMixin,
    forms.ModelForm,
):
    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "email",
            "role",
            "phone",
            "staff_id",
            "address",
            "date_of_birth",
            "profile_photo",
            "is_active",
            "is_verified",
        ]

        widgets = {
            "date_of_birth": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }


class ProfileForm(
    BootstrapFormMixin,
    forms.ModelForm,
):
    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "date_of_birth",
            "profile_photo",
        ]

        widgets = {
            "date_of_birth": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }


class UserPasswordChangeForm(
    BootstrapFormMixin,
    PasswordChangeForm,
):
    pass