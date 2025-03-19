from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator


class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    phone_validator = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be exactly 10 digits."
    )

    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=10, validators=[phone_validator])
    pickup_date = models.DateTimeField()
    pickup_location = models.CharField(max_length=100, null=True, blank=True)
    pickup_city = models.CharField(max_length=30)

    drop_date = models.DateTimeField(null=True, blank=True)
    drop_location = models.CharField(max_length=100, null=True, blank=True)
    drop_city = models.CharField(max_length=30)

    JOURNEY_TYPE_CHOICES = [
        ('One Way', 'One Way'),
        ('Two Way', 'Two Way'),
        ('Local', 'Local'),
        ('Multiple Locations', 'Multiple Locations'),
    ]

    journey_type = models.CharField(max_length=200, choices=JOURNEY_TYPE_CHOICES)
    journey_description = models.TextField(null=True, blank=True)
    total_fare = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    driver = models.ForeignKey('drivers.Driver', on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='bookings_as_driver')
    cab = models.ForeignKey('cabs.Cab', on_delete=models.SET_NULL, null=True, blank=True,
                            related_name='bookings_as_cab')
    owner = models.ForeignKey('owners.Owner', on_delete=models.CASCADE, related_name='bookings_as_owner')

    multi_locations = models.JSONField(default=dict, blank=True, null=True)
    additional_charges = models.JSONField(default=dict, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Due', 'Due')], default='Paid')

    def __str__(self):
        return f"Booking {self.id} - {self.customer_name}"
