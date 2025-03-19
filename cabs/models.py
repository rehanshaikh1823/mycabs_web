from django.db import models
from drivers.models import Driver
from owners.models import Owner


class Cab(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='cabs')
    driver = models.OneToOneField(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_cab')
    vehicle_number = models.CharField(max_length=20, unique=True)
    model = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    current_location = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.model} - {self.vehicle_number}"
