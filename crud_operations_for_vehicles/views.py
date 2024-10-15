from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateVehicleForm
from .decorator import admin_or_staff_required
from vehicles.models import Vehicle
import base64
from io import BytesIO
from PIL import Image
from venv import logger
from django.http import HttpResponse

from vehicles.models import Vehicle

@admin_or_staff_required
def create_vehicle_page(request):
    if request.method == 'POST':
        form = CreateVehicleForm(request.POST, request.FILES)
        print("Form data received:", request.POST)
        
        if not request.FILES.get('vehicle_image'):
           form.add_error('vehicle_image', 'This field is required.')

        if form.is_valid():
            print("Form is valid")
            vehicle = form.save()
            print("Vehicle saved to the database")  # Confirm saving
            return redirect('read_vehicle_page')  # Redirect after saving
        else:
            print("Form errors:", form.errors)  # Check for errors
    else:
        form = CreateVehicleForm()

    return render(request, 'create_vehicle_page.html', {'form': form})

@admin_or_staff_required
def update_vehicle_page(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, vehicle_id=vehicle_id)
    
    # Save the updated data
    if request.method == 'POST':
        form = CreateVehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            form.save() 
            return redirect('read_vehicle_page')  # Redirect after saving
    
    #Insert the current vehicle data in the fields
    else:
        form = CreateVehicleForm(instance=vehicle)

    # Convert the blob image to base64 for rendering (if applicable)
    vehicle.image_base64 = get_image_base64(vehicle)
    
    return render(request, 'update_vehicle_page.html', {'form': form, 'vehicle': vehicle})

@admin_or_staff_required
def read_vehicle(request, vehicle_id=None):
    vehicles = Vehicle.objects.filter(vehicle_is_deleted=False)
    vehicle_type = request.GET.get('vehicle_type', 'all')
    vehicle_search = request.GET.get('vehicle_search')

    if vehicle_type != 'all':
        vehicles = vehicles.filter(vehicle_type=vehicle_type)

    for vehicle in vehicles:
        if vehicle.vehicle_blobimage:
            image = Image.open(BytesIO(vehicle.vehicle_blobimage))
            if image.mode == 'RGBA':
                image = image.convert('RGB')
            buffer = BytesIO()
            image_format = image.format if image.format else 'JPEG'
            image.save(buffer, format=image_format)
            mime_type = f"image/{image_format.lower()}"
            vehicle.image_base64 = f"data:{mime_type};base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
        else:
            vehicle.image_base64 = None

    vehicle_detail = None  # Initialize vehicle_detail

    if request.method == 'POST':
        if 'delete_vehicle' in request.POST:
            vehicle_id = request.POST.get('delete_vehicle')
            logger.debug(f"Attempting to delete vehicle with ID: {vehicle_id}")
            if vehicle_id and vehicle_id.isdigit(): 
                vehicle_to_delete = get_object_or_404(Vehicle, pk=vehicle_id)
                vehicle_to_delete.vehicle_is_deleted = True
                vehicle_to_delete.save()
                logger.info(f"Deleted vehicle ID: {vehicle_id}")  
                return redirect('read_vehicle_page')
            else:
                logger.warning(f"Invalid vehicle ID: {vehicle_id}")

        elif 'vehicle_id' in request.POST:
            vehicle_id = request.POST.get('vehicle_id')
            if vehicle_id:
                vehicle_detail = get_object_or_404(Vehicle, pk=vehicle_id)

    return render(request, 'read_vehicle_page.html', {
        'vehicles': vehicles,
        'vehicle_detail': vehicle_detail,
        'type_filter': vehicle_type,
    })


def vehicle_image(request, vehicle_id):
    try:
        vehicle = Vehicle.objects.get(pk=vehicle_id)
        if vehicle.vehicle_blobimage:
            return HttpResponse(vehicle.vehicle_blobimage, content_type='image/jpeg')
        else:
            return HttpResponse("Image not available", content_type='text/plain')
    except Vehicle.DoesNotExist:
        return HttpResponse("Vehicle not found", content_type='text/plain')

@admin_or_staff_required
def admin_and_staff_page(request):
    return render(request, 'admin_staff_only.html')

def get_image_base64(vehicle):
    if vehicle.vehicle_blobimage:
        image = Image.open(BytesIO(vehicle.vehicle_blobimage))
        
        # Check the mode and convert if necessary
        if image.mode == 'RGBA':
            image = image.convert('RGB') 
        
        buffer = BytesIO()
        image.save(buffer, format='JPEG') 
        return f"data:image/jpeg;base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
    
    return None
