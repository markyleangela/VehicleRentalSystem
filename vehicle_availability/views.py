from django.shortcuts import render

from vehicles.models import Vehicle

# Create your views here.
def vehicle_list(request):
    vehicles = Vehicle.objects.all() #use .filter to list specific vehicles
    return render(request, "vehicle_list/vehicle_list.html", {'vehicles':vehicles})


