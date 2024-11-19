from django.contrib import admin

from .models import Vehicle, Rating

# Register your models here.


from .models import Vehicle

admin.site.register(Vehicle)

admin.site.register(Rating)