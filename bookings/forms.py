from drivers.models import Driver
from cabs.models import Cab
from .models import Booking
from django.utils import timezone
from django.core.exceptions import ValidationError
import json
from django import forms
import logging

logger = logging.getLogger(__name__)


class CreateBookingForm(forms.ModelForm):
    multi_locations = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Booking
        fields = [
            'customer_name', 'customer_phone', 'pickup_date',
            'pickup_location', 'pickup_city', 'drop_date',
            'drop_location', 'drop_city', 'journey_type',
            'journey_description'
        ]
        widgets = {
            'pickup_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'drop_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'journey_description': forms.Textarea(attrs={'rows': 2}),
        }

    def clean(self):
        cleaned_data = super().clean()
        journey_type = cleaned_data.get('journey_type')
        drop_date = cleaned_data.get('drop_date')

        if journey_type != 'One Way' and not drop_date:
            self.add_error('drop_date', 'Drop Date is required for this journey type.')

        if journey_type == 'Multiple Locations':
            multi_locations = cleaned_data.get('multi_locations')
            if multi_locations:
                try:
                    locations = json.loads(multi_locations)
                    if not locations or not isinstance(locations, list) or not any(
                            location.get('pickup') or location.get('drop') for location in locations):
                        raise forms.ValidationError("At least one valid pickup or drop location is required.")
                except json.JSONDecodeError:
                    raise forms.ValidationError("Invalid format for multiple locations.")
            else:
                raise forms.ValidationError("Multiple locations are required for this journey type.")
        else:
            if not cleaned_data.get('pickup_location') or not cleaned_data.get('drop_location'):
                raise forms.ValidationError("Pickup and drop locations are required for this journey type.")

        return cleaned_data


# class UpdateBookingForm(forms.ModelForm):
#     cab = forms.ModelChoiceField(queryset=Cab.objects.filter(is_active=True), required=True)
#     driver = forms.ModelChoiceField(queryset=Driver.objects.filter(user__is_active=True), required=True)
#
#     class Meta:
#         model = Booking
#         fields = [
#             'customer_name', 'customer_phone', 'pickup_date', 'pickup_location', 'pickup_city',
#             'driver', 'cab', 'status', 'drop_date', 'drop_location', 'drop_city', 'journey_type',
#             'journey_description', 'total_fare'
#         ]
#         widgets = {
#             'pickup_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
#             'drop_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
#             'journey_description': forms.Textarea(attrs={'rows': 2}),
#         }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self.instance.pk:
#             self.fields['pickup_date'].initial = self.instance.pickup_date.astimezone(
#                 timezone.get_current_timezone()).strftime('%Y-%m-%dT%H:%M')
#             self.fields['drop_date'].initial = self.instance.drop_date.astimezone(
#                 timezone.get_current_timezone()).strftime('%Y-%m-%dT%H:%M') if self.instance.drop_date else None
#
#     def clean(self):
#         cleaned_data = super().clean()
#         journey_type = cleaned_data.get('journey_type')
#         drop_date = cleaned_data.get('drop_date')
#
#         if journey_type != 'One Way' and not drop_date:
#             self.add_error('drop_date', 'Drop Date is required for this journey type.')
#
#         if journey_type == 'Multiple Locations':
#             multi_locations = cleaned_data.get('multi_locations')
#             if multi_locations is not None:
#                 try:
#                     locations = json.loads(multi_locations)
#                     if not locations or not isinstance(locations, list) or not any(
#                             location.get('pickup') or location.get('drop') for location in locations):
#                         raise forms.ValidationError("At least one valid pickup or drop location is required.")
#                 except json.JSONDecodeError:
#                     raise forms.ValidationError("Invalid format for multiple locations.")
#         else:
#             if not cleaned_data.get('pickup_location') or not cleaned_data.get('drop_location'):
#                 raise forms.ValidationError("Pickup and drop locations are required for this journey type.")
#
#         return cleaned_data
#
#     def clean_total_fare(self):
#         total_fare = self.cleaned_data.get('total_fare')
#         if total_fare is None or total_fare <= 0:
#             raise ValidationError('Total fare must be a positive number.')
#         return total_fare

class UpdateBookingForm(forms.ModelForm):
    cab = forms.ModelChoiceField(queryset=Cab.objects.filter(is_active=True), required=True)
    driver = forms.ModelChoiceField(queryset=Driver.objects.filter(user__is_active=True), required=True)
    toll = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    parking = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    fuel = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    others = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = Booking
        fields = [
            'customer_name', 'customer_phone', 'pickup_date', 'pickup_location', 'pickup_city',
            'driver', 'cab', 'status', 'drop_date', 'drop_location', 'drop_city', 'journey_type',
            'journey_description', 'total_fare', 'payment_status', 'toll', 'parking', 'fuel', 'others'
        ]
        widgets = {
            'pickup_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'drop_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'journey_description': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            additional_charges = self.instance.additional_charges or {}
            self.fields['toll'].initial = additional_charges.get('toll')
            self.fields['parking'].initial = additional_charges.get('parking')
            self.fields['fuel'].initial = additional_charges.get('fuel')
            self.fields['others'].initial = additional_charges.get('others')

            self.fields['pickup_date'].initial = self.instance.pickup_date.astimezone(
                timezone.get_current_timezone()).strftime('%Y-%m-%dT%H:%M')
            self.fields['drop_date'].initial = self.instance.drop_date.astimezone(
                timezone.get_current_timezone()).strftime('%Y-%m-%dT%H:%M') if self.instance.drop_date else None

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        toll = cleaned_data.get('toll')
        fuel = cleaned_data.get('fuel')

        if status == 'Completed':
            if toll is None or toll == '':
                self.add_error('toll', 'Toll is required. Please enter a value of at least 0.')
                cleaned_data['toll'] = 0  # Ensure it gets a value even if empty

            if fuel is None or fuel == '':
                self.add_error('fuel', 'Fuel is required. Please enter a value of at least 0.')
                cleaned_data['fuel'] = 0  # Ensure it gets a value even if empty

        # Other validation logic
        journey_type = cleaned_data.get('journey_type')
        drop_date = cleaned_data.get('drop_date')

        if journey_type != 'One Way' and not drop_date:
            self.add_error('drop_date', 'Drop Date is required for this journey type.')

        if journey_type == 'Multiple Locations':
            multi_locations = cleaned_data.get('multi_locations')
            if multi_locations is not None:
                try:
                    locations = json.loads(multi_locations)
                    if not locations or not isinstance(locations, list) or not any(
                            location.get('pickup') or location.get('drop') for location in locations):
                        raise forms.ValidationError("At least one valid pickup or drop location is required.")
                except json.JSONDecodeError:
                    raise forms.ValidationError("Invalid format for multiple locations.")
        else:
            if not cleaned_data.get('pickup_location') or not cleaned_data.get('drop_location'):
                raise forms.ValidationError("Pickup and drop locations are required for this journey type.")

        return cleaned_data

    def clean_total_fare(self):
        total_fare = self.cleaned_data.get('total_fare')
        if total_fare is None or total_fare <= 0:
            raise ValidationError('Total fare must be a positive number.')
        return total_fare

    def save(self, commit=True):
        booking = super().save(commit=False)
        booking.additional_charges = {
            'toll': float(self.cleaned_data.get('toll', 0) or 0),
            'parking': float(self.cleaned_data.get('parking', 0) or 0),
            'fuel': float(self.cleaned_data.get('fuel', 0) or 0),
            'others': float(self.cleaned_data.get('others', 0) or 0),
        }
        if commit:
            booking.save()
        return booking


class DriverUpdateStatusForm(forms.ModelForm):
    status = forms.ChoiceField(choices=Booking.STATUS_CHOICES, required=True)
    toll = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    parking = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    fuel = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    others = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = Booking
        fields = ['status', 'payment_status',  'toll', 'parking', 'fuel', 'others']

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        if self.instance.pk:
            additional_charges = self.instance.additional_charges or {}
            self.fields['toll'].initial = additional_charges.get('toll')
            self.fields['parking'].initial = additional_charges.get('parking')
            self.fields['fuel'].initial = additional_charges.get('fuel')
            self.fields['others'].initial = additional_charges.get('others')

        booking = kwargs.get('instance')

        if booking and booking.status == 'Confirmed':
            self.fields['status'].choices = [
                ('Confirmed', 'Confirmed'),
                ('Completed', 'Completed')
            ]
        elif booking and booking.status == 'Completed':
            self.fields['status'].choices = [('Completed', 'Completed')]
        else:
            # Set default choices or any other logic if needed
            self.fields['status'].choices = [('', '------')] + self.fields['status'].choices

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        toll = cleaned_data.get('toll')
        fuel = cleaned_data.get('fuel')

        if status == 'Completed':
            if toll is None or toll == '':
                self.add_error('toll', 'Toll is required. Please enter a value of at least 0.')
                cleaned_data['toll'] = 0  # Ensure it gets a value even if empty

            if fuel is None or fuel == '':
                self.add_error('fuel', 'Fuel is required. Please enter a value of at least 0.')
                cleaned_data['fuel'] = 0  # Ensure it gets a value even if empty

        return cleaned_data

    def save(self, commit=True):
        booking = super().save(commit=False)
        booking.additional_charges = {
            'toll': float(self.cleaned_data.get('toll', 0) or 0),
            'parking': float(self.cleaned_data.get('parking', 0) or 0),
            'fuel': float(self.cleaned_data.get('fuel', 0) or 0),
            'others': float(self.cleaned_data.get('others', 0) or 0),
        }
        if commit:
            booking.save()
        return booking
