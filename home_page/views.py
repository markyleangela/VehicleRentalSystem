from venv import logger
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import base64
from io import BytesIO
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


from vehicles.models import Vehicle

# Create your views here.
# @login_required
# def vehicle_list(request, vehicle_id = None):
#     vehicles = Vehicle.objects.all() #use .filter to list specific vehicles
#     vehicle_type = request.GET.get('vehicle_type', 'all') 
#     vehicle_search = request.GET.get('vehicle_search')

#     if vehicle_type != 'all':
#         vehicles = vehicles.filter(vehicle_type=vehicle_type)

#     for vehicle in vehicles:
#         if vehicle.vehicle_blobimage:
#             image = Image.open(BytesIO(vehicle.vehicle_blobimage))
            
#             # Keep transparency for PNGs (no conversion to RGB)
#             buffer = BytesIO()
#             image_format = image.format if image.format else 'JPEG'
            
#             # Handle PNG images with RGBA (keeping transparency)
#             if image_format == 'PNG' and image.mode == 'RGBA':
#                 image.save(buffer, format='PNG')
#                 mime_type = "image/png"
#             else:
#                 # For non-PNG images or images without transparency, use JPEG
#                 image = image.convert('RGB')
#                 image.save(buffer, format='JPEG')
#                 mime_type = "image/jpeg"
            
#             vehicle.image_base64 = f"data:{mime_type};base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
#         else:
#             vehicle.image_base64 = None

#     vehicle_detail = None  # Initialize vehicle_detail

#     if request.method == 'POST':
#         if 'delete_vehicle' in request.POST:
#             vehicle_id = request.POST.get('delete_vehicle')
#             logger.debug(f"Attempting to delete vehicle with ID: {vehicle_id}")
#             if vehicle_id and vehicle_id.isdigit(): 
#                 vehicle_to_delete = get_object_or_404(Vehicle, pk=vehicle_id)
#                 vehicle_to_delete.vehicle_is_deleted = True
#                 vehicle_to_delete.save()
#                 logger.info(f"Deleted vehicle ID: {vehicle_id}")  
#                 return redirect('vehicle_list')
#             else:
#                 logger.warning(f"Invalid vehicle ID: {vehicle_id}")

#         elif 'vehicle_id' in request.POST:
#             vehicle_id = request.POST.get('vehicle_id')
#             if vehicle_id:
#                 vehicle_detail = get_object_or_404(Vehicle, pk=vehicle_id)

#     return render(request, 'home_page.html', {
#         'vehicles': vehicles,
#         'vehicle_detail': vehicle_detail,
#         'type_filter': vehicle_type,
#     })


from datetime import datetime
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from io import BytesIO
from PIL import Image
import base64
import logging

logger = logging.getLogger(__name__)

@login_required
def vehicle_list(request, vehicle_id=None):
    # Start with all vehicles
    vehicles = Vehicle.objects.all()
    vehicle_type = request.GET.get('vehicle_type', 'all')

    # Retrieve the start date and end date from the request
    start_date = request.GET.get('start_date')
    return_date = request.GET.get('return_date')

    # Filter vehicles by vehicle type if provided
    if vehicle_type != 'all':
        vehicles = vehicles.filter(vehicle_type=vehicle_type)

    # Filter vehicles based on availability within the start_date and end_date
    if start_date and return_date:
        try:
            # Convert date strings into datetime objects
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            return_date = datetime.strptime(return_date, "%Y-%m-%d").date()

            # Exclude vehicles that have rentals overlapping the selected date range
            vehicles = vehicles.exclude(
                rentalrecord__start_date__lt=return_date,
                rentalrecord__return_date__gt=start_date
            )

        except ValueError:
            logger.warning("Invalid date format for start_date or end_date.")

    # Process the vehicle images into base64 format for rendering
    for vehicle in vehicles:
        if vehicle.vehicle_blobimage:
            image = Image.open(BytesIO(vehicle.vehicle_blobimage))

            buffer = BytesIO()
            image_format = image.format if image.format else 'JPEG'

            if image_format == 'PNG' and image.mode == 'RGBA':
                image.save(buffer, format='PNG')
                mime_type = "image/png"
            else:
                image = image.convert('RGB')
                image.save(buffer, format='JPEG')
                mime_type = "image/jpeg"

            vehicle.image_base64 = f"data:{mime_type};base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
        else:
            vehicle.image_base64 = None

    # Handle POST requests for deleting or viewing vehicle details
    vehicle_detail = None
    if request.method == 'POST':
        # Handle vehicle deletion
        if 'delete_vehicle' in request.POST:
            vehicle_id = request.POST.get('delete_vehicle')
            logger.debug(f"Attempting to delete vehicle with ID: {vehicle_id}")
            if vehicle_id and vehicle_id.isdigit():
                vehicle_to_delete = get_object_or_404(Vehicle, pk=vehicle_id)
                vehicle_to_delete.vehicle_is_deleted = True
                vehicle_to_delete.save()
                logger.info(f"Deleted vehicle ID: {vehicle_id}")
                return redirect('vehicle_list')
            else:
                logger.warning(f"Invalid vehicle ID: {vehicle_id}")

        # Handle viewing vehicle details
        elif 'vehicle_id' in request.POST:
            vehicle_id = request.POST.get('vehicle_id')
            if vehicle_id:
                vehicle_detail = get_object_or_404(Vehicle, pk=vehicle_id)

    # Render the filtered vehicles and any vehicle details
    return render(request, 'home_page.html', {
        'vehicles': vehicles,
        'vehicle_detail': vehicle_detail,
        'type_filter': vehicle_type,
        'start_date': start_date,
        'return_date': return_date,
    })




@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login_page')
    return render(request, 'logout.html')




