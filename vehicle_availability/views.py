from venv import logger
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import base64
from io import BytesIO
from PIL import Image


from vehicles.models import Vehicle

# Create your views here.
from venv import logger
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import base64
from io import BytesIO
from PIL import Image
from vehicles.models import Vehicle

def vehicle_list(request, vehicle_id=None):
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
                return redirect('vehicle_list')
            else:
                logger.warning(f"Invalid vehicle ID: {vehicle_id}")

        elif 'vehicle_id' in request.POST:
            vehicle_id = request.POST.get('vehicle_id')
            if vehicle_id:
                vehicle_detail = get_object_or_404(Vehicle, pk=vehicle_id)

    return render(request, 'vehicle_list/vehicle_list.html', {
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






