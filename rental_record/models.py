from django.db import models
from django.contrib.auth.models import User
from vehicles.models import Vehicle
from django.utils import timezone
from datetime import timedelta

class RentalRecord(models.Model):
    rental_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    start_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_date = models.DateField(null=True, blank=True)
    payment_status = models.BooleanField(default=False)
    return_status = models.BooleanField(default=False)
    days_rented = models.IntegerField(default=0)
    payment_due_date = models.DateTimeField(null=True, blank=True)
    payment_in_progress = models.BooleanField(default=True)
    is_rated =  models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.customer.username} - {self.vehicle}"

    def set_payment_due_date(self, grace_period_days=3):
        self.payment_due_date = timezone.now() + timedelta(days=grace_period_days)

