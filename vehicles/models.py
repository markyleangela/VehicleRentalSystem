from django.db import models

# Create your models here.
class Vehicle(models.Model):
    vehicle_id = models.IntegerField(primary_key=True)
    vehicle_model = models.CharField(max_length=100)
    vehicle_brand = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=50)
    vehicle_price = models.FloatField(default=0.00)
    vehicle_status = models.CharField(max_length=20)


