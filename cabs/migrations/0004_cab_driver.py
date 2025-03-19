# Generated by Django 5.0.7 on 2024-08-10 09:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabs', '0003_cab_current_location_cab_is_available_cab_latitude_and_more'),
        ('drivers', '0014_remove_driver_experience_years'),
    ]

    operations = [
        migrations.AddField(
            model_name='cab',
            name='driver',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_cab', to='drivers.driver'),
        ),
    ]
