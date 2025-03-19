from django import forms
from .models import Owner


class OwnerProfileForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['business_name', 'business_address', 'registration_number', 'pan_number', 'gst_number']
