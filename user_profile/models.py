from django.db import models

from django.conf import settings
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class ProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    license_no = models.CharField(max_length=15, blank=True)
    profile_image = models.BinaryField(null=True, blank=True)
    license_verified = models.BooleanField(default=False) #if the user has license no that is valid then the user is verified
    email_verified = models.BooleanField(default=False)  
    user_verified = models.BooleanField(default=False)  #if email and license is verified
    is_deleted = models.BooleanField(default=False)  

    def __str__(self):
        return f'{self.user.username} Profile'
