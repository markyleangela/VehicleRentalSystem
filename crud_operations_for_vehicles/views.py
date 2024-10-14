from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateVehicleForm
from vehicles.models import Vehicle
import base64
from io import BytesIO
from PIL import Image

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
            return redirect('vehicle_list')  # Redirect after saving
        else:
            print("Form errors:", form.errors)  # Check for errors
    else:
        form = CreateVehicleForm()

    return render(request, 'create_vehicle_page.html', {'form': form})

def update_vehicle_page(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, vehicle_id=vehicle_id)
    
    # Save the updated data
    if request.method == 'POST':
        form = CreateVehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            form.save() 
            return redirect('vehicle_list')  # Redirect after saving
    
    #Insert the current vehicle data in the fields
    else:
        form = CreateVehicleForm(instance=vehicle)

    # Convert the blob image to base64 for rendering (if applicable)
    vehicle.image_base64 = get_image_base64(vehicle)
    
    return render(request, 'update_vehicle_page.html', {'form': form, 'vehicle': vehicle})

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
