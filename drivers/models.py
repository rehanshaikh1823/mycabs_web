from owners.models import Owner
from django.db import models
from django.conf import settings


class Driver(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='drivers_as_user')
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='drivers_as_owner')
    license_number = models.CharField(max_length=50, unique=True, null=True, blank=True)

    def __str__(self):
        # Accessing the user's first name and last name
        first_name = self.user.first_name
        last_name = self.user.last_name
        username = self.user.username
        mobile = getattr(self.user, 'mobile', 'No Mobile')
        # Using 'getattr' to avoid AttributeError if mobile doesn't exist

        if first_name:
            return f"{first_name} {last_name} - {mobile}"
        else:
            return f"{username} - {mobile}"
