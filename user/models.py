from django.db import models

# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.PhoneNumberField((""))
    birth_date = models.DateField()
    license_number = models.CharField(max_length=10)
    registration_date = models.DateTimeField(auto_now_add=True)
    customer_profile = models.BinaryField(null = True, blank=True)
