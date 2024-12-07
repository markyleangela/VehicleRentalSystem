from django.shortcuts import render, redirect, get_object_or_404
from vehicles.models import Vehicle
from rental_record.models import RentalRecord
import base64
from io import BytesIO
from PIL import Image
from venv import logger

# Create your views here.
def dashboard_view(request):
    return render(request, 'admin_dashboard.html')

def booking_list_view(request):
    rental_records = RentalRecord.objects.all()  # Get all rental records
    return render(request, 'booking_list_admin.html', {'rental_records': rental_records})

def vehicle_list_view(request):
    vehicles = Vehicle.objects.filter(vehicle_is_deleted=False)

    for vehicle in vehicles:
        if vehicle.vehicle_blobimage:
            image = Image.open(BytesIO(vehicle.vehicle_blobimage))

            # Check if image has an alpha channel (transparency)
            if image.mode == 'RGBA':
                # Don't convert to RGB, keep transparency
                buffer = BytesIO()
                image.save(buffer, format="PNG")  # Save as PNG to preserve transparency
                buffer.seek(0)  # Move the cursor back to the beginning of the buffer

                mime_type = "image/png"
                vehicle.image_base64 = f"data:{mime_type};base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
            else:
                # If the image doesn't have transparency, process it as usual
                buffer = BytesIO()
                image_format = image.format if image.format else 'JPEG'
                image.save(buffer, format=image_format)
                mime_type = f"image/{image_format.lower()}"
                vehicle.image_base64 = f"data:{mime_type};base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
        else:
            vehicle.image_base64 = None
            
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
                
    return render(request, 'read_vehicle_page.html', {'vehicles': vehicles})

