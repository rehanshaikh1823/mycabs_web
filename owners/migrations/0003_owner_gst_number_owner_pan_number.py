# Generated by Django 5.0.7 on 2024-08-06 04:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owners', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='gst_number',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(message='GST number must be in the format 12ABCDE3456F1Z5', regex='^\\d{2}[A-Z]{5}\\d{4}[A-Z]{1}[A-Z\\d]{1}[Z]{1}[A-Z\\d]{1}$')]),
        ),
        migrations.AddField(
            model_name='owner',
            name='pan_number',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator(message='PAN number must be in the format AAAAA9999A', regex='^[A-Z]{5}[0-9]{4}[A-Z]$')]),
        ),
    ]
