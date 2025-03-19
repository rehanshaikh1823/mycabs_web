# Generated by Django 5.0.7 on 2024-08-07 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0009_booking_multi_drops_locations_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='multi_drops_locations',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='multi_pickups_locations',
        ),
        migrations.AddField(
            model_name='booking',
            name='multi_locations',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
