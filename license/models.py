from django.db import models

# Create your models here.
# models.py


class License(models.Model):
    license_number = models.CharField(max_length=15, unique=True)
    licensee_name = models.CharField(max_length=100, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')])

    def __str__(self):
        return self.license_number
