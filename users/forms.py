from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import User


class BaseSignUpForm(UserCreationForm):
    mobile = forms.CharField(
        max_length=15,
        required=True,
        help_text="Enter 10 digit mobile number",
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Phone number must be 10 digits long."
            ),
        ]
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'mobile']

    def clean_mobile(self) -> str:
        mobile = self.cleaned_data.get('mobile')
        if not mobile:
            raise forms.ValidationError("Mobile number is required.")
        return mobile

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class OwnerSignUpForm(BaseSignUpForm):
    def save(self, commit: bool = True) -> User:
        user = super().save(commit=False)
        user.is_owner = True
        if commit:
            user.save()
        return user


class DriverSignUpForm(BaseSignUpForm):
    def save(self, commit: bool = True) -> User:
        user = super().save(commit=False)
        user.is_driver = True
        if commit:
            user.save()
        return user
