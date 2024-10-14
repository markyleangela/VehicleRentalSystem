from django.shortcuts import render, redirect, get_object_or_404
import base64
from io import BytesIO
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


from vehicles.models import Vehicle

# Create your views here.
@login_required
def vehicle_list(request, vehicle_id = None):
    vehicles = Vehicle.objects.all() #use .filter to list specific vehicles
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
            image_format = image.format
            
            if not image_format or image_format == 'JPEG':
                image_format = 'JPEG'
            image.save(buffer, format=image_format) 
            mime_type = f"image/{image_format.lower()}"
            vehicle.image_base64 = f"data:{mime_type};base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
        else:
            vehicle.image_base64 = None


    if request.method == 'POST':
        vehicle_id = request.POST.get('vehicle_id')  # Get the vehicle_id from the form submission
        vehicle_detail = get_object_or_404(Vehicle, pk=vehicle_id)  # Get the specific vehicle detail


        return render(request, 'vehicle_list/vehicle_list.html', {
        'vehicles': vehicles,
        'vehicle_detail': vehicle_detail,
        'type_filter': vehicle_type,
    })



    return render(request, 'vehicle_list/vehicle_list.html', {
        'vehicles': vehicles,
        'type_filter': vehicle_type, 
        
    })

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login_page')
    return render(request, 'logout.html')




