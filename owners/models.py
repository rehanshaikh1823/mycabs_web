from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator


class Owner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner_profile')
    business_name = models.CharField(max_length=255)
    business_address = models.TextField()
    registration_number = models.CharField(max_length=50, unique=True)

    # PAN number should follow the format: AAAAA9999A
    pan_number = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^[A-Z]{5}[0-9]{4}[A-Z]$',
                message='PAN number must be in the format AAAAA9999A'
            )
        ],
        blank=True,
        null=True
    )

    # GST number should follow the format: 12ABCDE3456F1Z5
    gst_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}$',
                message='GST number must be in the format 12ABCDE3456F1Z5'
            )
        ],
        blank=True,
        null=True
    )

    def __str__(self):
        return self.business_name
