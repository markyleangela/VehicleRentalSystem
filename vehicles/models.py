from django.db import models
import base64
from django.contrib.auth.models import User
from django.db.models import Avg
# Create your models here.
class Vehicle(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('In Use', 'In Use')
    ]

    TYPE_CHOICES = [
        ('4 seater', '4 seater'),
        ('6 seater', '6 seater'),
        ('2 seater', 'Motorcycle')
    ]
    TRANSMISSION_CHOICES = [
         ('Automatic', 'Automatic'),
        ('Manual', 'Manual'),
       
    ]

    CARGO_CHOICES = [
         ('Standard Cargo Capacity', '12.6 cu ft'),
        ('Expanded Cargo Capacity', ' 38.5 cu ft'),
        ('Max Cargo Capacity', '75.5 cu ft '),
    ]
       
    vehicle_id = models.AutoField(primary_key=True)
    vehicle_model = models.CharField(max_length=100)
    vehicle_brand = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    vehicle_price = models.FloatField(default=0.00)
    vehicle_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Available")
    vehicle_blobimage = models.BinaryField(null = True, blank=True)
    vehicle_is_deleted = models.BooleanField(default=False)
    vehicle_description = models.CharField(max_length=500, null=True)
    vehicle_transmission = models.CharField(max_length=50, choices=TRANSMISSION_CHOICES, null=True)
    vehicle_cargo =  models.CharField(max_length=50, choices=CARGO_CHOICES,null=True)
    vehicle_rating = models.FloatField(default=0)
    
    def __str__(self):
        return f"{self.vehicle_model} {self.vehicle_brand} {self.vehicle_type} {self.vehicle_price}"
    

    def image_base64(self):
        if self.vehicle_blobimage:
            return base64.b64encode(self.vehicle_blobimage).decode('utf-8')
        return None
    
    def average_rating(self):
        return self.ratings.aggregate(Avg('rating'))['rating__avg'] or 0

    def rating_count(self):
        return self.ratings.count()
    


class Rating(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)  # e.g., 1-5 scale
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.rating} - { self.review }"