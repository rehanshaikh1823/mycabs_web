from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    phone_validator = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be exactly 10 digits."
    )
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10, unique=True, validators=[phone_validator])
    is_owner = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)

    def __str__(self):
        return self.email
