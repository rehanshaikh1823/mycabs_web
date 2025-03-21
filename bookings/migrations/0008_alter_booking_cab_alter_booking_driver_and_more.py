# Generated by Django 5.0.7 on 2024-07-31 10:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0007_alter_booking_owner'),
        ('cabs', '0002_initial'),
        ('drivers', '0012_remove_driver_is_employed'),
        ('owners', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='cab',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookings_as_cab', to='cabs.cab'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookings_as_driver', to='drivers.driver'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings_as_owner', to='owners.owner'),
        ),
    ]
