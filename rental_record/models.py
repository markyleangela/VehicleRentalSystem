from django.db import models
from django.contrib.auth.models import User
from vehicles.models import Vehicle

class RentalRecord(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    start_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)  # In case the vehicle hasn't been returned yet
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Better for currency
    payment_date = models.DateField(null=True, blank=True)  # Optional if payment isn't done yet
    payment_status = models.BooleanField(default=False)  # Default to False until paid
    return_status = models.BooleanField(default=False)  # Default to False until returned

    def __str__(self):
        return f"{self.customer.username} - {self.vehicle}"
