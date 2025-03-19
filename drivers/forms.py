from django import forms
from django.contrib.auth.models import User
from .models import Driver


class DriverDetailsUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class DriverUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['license_number']
