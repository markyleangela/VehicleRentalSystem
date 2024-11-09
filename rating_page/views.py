from django.shortcuts import render
from vehicles.models import Vehicle
# Create your views here.

def vehicle_rate(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'vehicle_rating.html', {'vehicles': vehicles})