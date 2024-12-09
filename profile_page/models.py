from django.db import models
from django.contrib.auth.models import User


from user_profile.models import ProfileInfo

class EmailConfirmation(models.Model):
    user = models.OneToOneField(ProfileInfo, on_delete=models.CASCADE)
    code = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class LicenseConfirmation(models.Model):
    user = models.OneToOneField(ProfileInfo, on_delete=models.CASCADE)
    code = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)