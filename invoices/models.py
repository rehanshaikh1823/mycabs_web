from django.db import models


class Invoice(models.Model):
    booking = models.ForeignKey('bookings.Booking', on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=80, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.invoice_number} for Booking {self.booking.id}"
