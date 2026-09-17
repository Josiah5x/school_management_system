from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from schools.models import School

User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username",
                "autocomplete": "username",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
                "autocomplete": "current-password",
            }
        )
    )


class BootstrapMixin:
    """Apply Bootstrap 5 classes to form widgets."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs["class"] = "form-check-input"
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                widget.attrs["class"] = "form-select"
            else:
                widget.attrs["class"] = "form-control"


class UserCreateForm(BootstrapMixin, UserCreationForm):
    """Form used by Super Admin / authorized administrators to create a new user."""

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "school",
            "role",
            "phone",
            "staff_id",
            "profile_photo",
            "address",
            "date_of_birth",
            "is_verified",
            "is_active",
        ]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Username", "autocomplete": "username"}),
            "first_name": forms.TextInput(attrs={"placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email address"}),
            "school": forms.Select(),
            "role": forms.Select(),
            "phone": forms.TextInput(attrs={"placeholder": "080XXXXXXXX"}),
            "staff_id": forms.TextInput(attrs={"placeholder": "Staff ID"}),
            "profile_photo": forms.ClearableFileInput(),
            "address": forms.Textarea(attrs={"rows": 3, "placeholder": "Residential address"}),
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "is_verified": forms.CheckboxInput(),
            "is_active": forms.CheckboxInput(attrs={"checked": True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["school"].queryset = School.objects.filter(is_active=True).order_by("name")

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")
        school = cleaned_data.get("school")

        if role != User.Role.SUPER_ADMIN and school is None:
            raise forms.ValidationError("Every non-super-admin user must belong to a school.")

        if role == User.Role.SUPER_ADMIN and school is not None:
            raise forms.ValidationError("A Super Administrator should not be assigned to a school.")

        return cleaned_data


class UserUpdateForm(BootstrapMixin, forms.ModelForm):
    """Form used to edit an existing user. Password is intentionally excluded."""

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "school",
            "role",
            "phone",
            "staff_id",
            "profile_photo",
            "address",
            "date_of_birth",
            "is_verified",
            "is_active",
        ]
        widgets = {
            "username": forms.TextInput(attrs={"autocomplete": "username"}),
            "first_name": forms.TextInput(),
            "last_name": forms.TextInput(),
            "email": forms.EmailInput(),
            "school": forms.Select(),
            "role": forms.Select(),
            "phone": forms.TextInput(),
            "staff_id": forms.TextInput(),
            "profile_photo": forms.ClearableFileInput(),
            "address": forms.Textarea(attrs={"rows": 3}),
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "is_verified": forms.CheckboxInput(),
            "is_active": forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["school"].queryset = School.objects.filter(is_active=True).order_by("name")

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")
        school = cleaned_data.get("school")

        if role != User.Role.SUPER_ADMIN and school is None:
            raise forms.ValidationError("Every non-super-admin user must belong to a school.")

        if role == User.Role.SUPER_ADMIN and school is not None:
            raise forms.ValidationError("A Super Administrator should not be assigned to a school.")

        return cleaned_data
