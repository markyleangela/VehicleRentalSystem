from django.db import models

# Create your models here.
class Vehicle(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('In Use', 'In Use')
    ]

    TYPE_CHOICES = [
        ('4 seater', '4 seater'),
        ('6 seater', '6 seater'),
        ('1 seater', 'Motorcycle')
    ]
    vehicle_id = models.AutoField(primary_key=True)
    vehicle_model = models.CharField(max_length=100)
    vehicle_brand = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    vehicle_price = models.FloatField(default=0.00)
    vehicle_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="available")

