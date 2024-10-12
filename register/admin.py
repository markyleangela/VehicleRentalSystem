from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'birth_date', 'phone_number', 'license_number')

admin.site.register(UserProfile, UserProfileAdmin)


