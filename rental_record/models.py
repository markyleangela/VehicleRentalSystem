from django.db import models
from django.contrib.auth.models import User
from vehicles.models import Vehicle
from django.utils import timezone
from datetime import timedelta

class RentalRecord(models.Model):

    # Choices for payment status
    PAYMENT_STATUS_CHOICES = [
        ('not_paid', 'Not Paid'),
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    ]

    # Choices for rental status
    RENTAL_STATUS_CHOICES = [
        ('cancelled','Cancelled'),
        ('pending', 'Pending'),
        ('booked', 'Booked'),
        ('in_use', 'In_use'),
        ('returned', 'Returned'),
        ('overdue_pending', 'Overdue_pending'),
        ('overdue_returned', 'Overdue_returned'),
        ('overdue_extended', 'Overdue_extended'),
        ('completed', 'Completed'),
    ]
        
    rental_id = models.AutoField(primary_key=True)
    transaction_id = models.BigIntegerField(editable=False, unique=True, null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    start_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)  
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    payment_date = models.DateTimeField(null=True, blank=True)      
    payment_status = models.BooleanField(default=False)  
    rental_status = models.CharField(max_length=20, choices=RENTAL_STATUS_CHOICES, default='pending')  
    days_rented = models.IntegerField(default= 0)
    payment_due_date = models.DateTimeField(null=True, blank=True)
    payment_in_progress = models.BooleanField(default=True)
    is_rated =  models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.customer.username} - {self.vehicle}"

    def set_payment_due_date(self, grace_period_days=3):
        self.payment_due_date = timezone.now() + timedelta(days=grace_period_days)
    
    def generate_transaction_id(self):
        # You can customize this logic to generate 7-digit integers
        import random
        return random.randint(1000000, 9999999)
