from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import base64
from io import BytesIO
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from vehicles.models import Vehicle, VehicleModel

@login_required
def vehicle_list(request):
    vehicle_type = request.GET.get('vehicle_type', 'all')  # Get filter type from request
    vehicle_search = request.GET.get('vehicle_search')  # Search query

    # Get all VehicleModel objects
    vehicle_models = VehicleModel.objects.all()

    # Apply filtering based on vehicle type if specified
    if vehicle_type != 'all':
        vehicle_models = vehicle_models.filter(vehicle_type=vehicle_type)

    vehicle_data = []  # This will store each model with its corresponding vehicles

    # Loop through each VehicleModel to calculate the quantity of available vehicles
    for vehicle_model in vehicle_models:
        vehicles = vehicle_model.vehicles.filter(vehicle_is_deleted=False)  # Get vehicles that are not deleted

        # Count available vehicles for this model
        available_vehicles = vehicles.filter(vehicle_status='Available').count()

        # Process the model's image
        if vehicle_model.vehicle_blobimage:
            image = Image.open(BytesIO(vehicle_model.vehicle_blobimage))
            
            # Handle transparency for PNGs
            buffer = BytesIO()
            image_format = image.format if image.format else 'JPEG'
            
            # Handle PNG images with RGBA (keeping transparency)
            if image_format == 'PNG' and image.mode == 'RGBA':
                image.save(buffer, format='PNG')
                mime_type = "image/png"
            else:
                # For non-PNG images or images without transparency, use JPEG
                image = image.convert('RGB')
                image.save(buffer, format='JPEG')
                mime_type = "image/jpeg"
            
            vehicle_model.image_base64 = f"data:{mime_type};base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
        else:
            vehicle_model.image_base64 = None  # No image case

        # Append model data with available quantity and vehicles
        vehicle_data.append({
            'vehicle_model': vehicle_model,  # The vehicle model info
            'available_count': available_vehicles,  # Count of available vehicles
            'vehicles': vehicles,  # The actual vehicle instances
        })

    vehicle_detail = None  # Initialize vehicle_detail

    if request.method == 'POST':
        if 'delete_vehicle' in request.POST:
            vehicle_id = request.POST.get('delete_vehicle')
            if vehicle_id and vehicle_id.isdigit():
                vehicle_to_delete = get_object_or_404(Vehicle, pk=vehicle_id)
                vehicle_to_delete.vehicle_is_deleted = True
                vehicle_to_delete.save()
                return redirect('vehicle_list')

        elif 'vehicle_id' in request.POST:
            vehicle_id = request.POST.get('vehicle_id')
            if vehicle_id:
                vehicle_detail = get_object_or_404(Vehicle, pk=vehicle_id)

    return render(request, 'home_page.html', {
        'vehicle_data': vehicle_data,  # Pass the vehicle model data with quantity
        'vehicle_detail': vehicle_detail,
        'type_filter': vehicle_type,
    })

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login_page')
    return render(request, 'logout.html')
