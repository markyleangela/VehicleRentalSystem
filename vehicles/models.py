from django.db import models

# VehicleModel represents the car model details
class VehicleModel(models.Model):
    TYPE_CHOICES = [
        ('4 seater', '4 seater'),
        ('6 seater', '6 seater'),
        ('1 seater', 'Motorcycle')
    ]
    
    vehicle_model = models.CharField(max_length=100)
    vehicle_brand = models.CharField(max_length=10)
    vehicle_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    vehicle_description = models.CharField(max_length=100, null=True)
    vehicle_price = models.FloatField(default=0.00)
    vehicle_blobimage = models.BinaryField(null=True, blank=True)  # Move the image here
    
    def __str__(self):
        return f"{self.vehicle_brand} {self.vehicle_model} ({self.vehicle_type})"

# Vehicle represents individual cars with a unique ID
class Vehicle(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('In Use', 'In Use')
    ]
    
    vehicle_id = models.AutoField(primary_key=True)
    vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE, related_name='vehicles')
    vehicle_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Available")
    vehicle_is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"ID: {self.vehicle_id} - {self.vehicle_model} - {self.vehicle_status}"
