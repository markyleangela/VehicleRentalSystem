from django.contrib import admin

from .models import Vehicle , VehicleModel

# Register your models here.


from .models import Vehicle

admin.site.register(Vehicle)
admin.site.register(VehicleModel)