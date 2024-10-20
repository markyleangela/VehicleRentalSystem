from django.db import models
from django.contrib.auth.models import User
from vehicles.models import Vehicle

class RentalRecord(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    start_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)  
    total_amount = models.DecimalField(max_digits=10, decimal_places=2) 
    payment_date = models.DateField(null=True, blank=True)  
    payment_status = models.BooleanField(default=False)  
    return_status = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.customer.username} - {self.vehicle}"
