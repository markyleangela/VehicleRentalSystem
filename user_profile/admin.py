from django.contrib import admin
from .models import UserProfile, ProfileInfo
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(ProfileInfo)