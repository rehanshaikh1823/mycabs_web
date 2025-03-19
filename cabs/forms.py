from django import forms
from .models import Cab


class CabForm(forms.ModelForm):
    class Meta:
        model = Cab
        fields = ['vehicle_number', 'model', 'capacity', 'is_active']
        widgets = {
            'vehicle_number': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CabLocationForm(forms.ModelForm):
    class Meta:
        model = Cab
        fields = ['current_location', 'latitude', 'longitude']

    def clean(self):
        cleaned_data = super().clean()
        latitude = cleaned_data.get('latitude')
        longitude = cleaned_data.get('longitude')
        current_location = cleaned_data.get('current_location')

        if not current_location:
            raise forms.ValidationError("Current location is required.")

        if not latitude or not longitude:
            raise forms.ValidationError("Both latitude and longitude are required.")

        try:
            float(latitude)
            float(longitude)
        except ValueError:
            raise forms.ValidationError("Latitude and longitude must be valid numbers.")

        return cleaned_data
