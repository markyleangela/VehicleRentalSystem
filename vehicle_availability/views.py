from django.shortcuts import render, redirect, get_object_or_404

from vehicles.models import Vehicle

# Create your views here.
def vehicle_list(request, vehicle_id = None):
    vehicles = Vehicle.objects.all() #use .filter to list specific vehicles

    if request.method == 'POST':
        vehicle_id = request.POST.get('vehicle_id')  # Get the vehicle_id from the form submission
        vehicle_detail = get_object_or_404(Vehicle, pk=vehicle_id)  # Get the specific vehicle details



    return render(request, 'vehicle_list/vehicle_list.html', {
        'vehicles': vehicles,
        'vehicle_detail': vehicle_detail,
    })



