from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=25)
    license_number = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username
        
