from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateVehicleForm
from admin_dashboard.decorator import admin_or_staff_required
from vehicles.models import Vehicle
import base64
from io import BytesIO
from PIL import Image
from django.http import HttpResponse

from vehicles.models import Vehicle
@admin_or_staff_required
def create_vehicle_page(request):
    if request.method == 'POST':
        form = CreateVehicleForm(request.POST, request.FILES)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicle_list')  # Redirect to the vehicle list after saving
        else:
            print("Form errors:", form.errors)  # Debug form errors
    else:
        form = CreateVehicleForm()

    return render(request, 'create_vehicle_page.html', {'form': form})


def vehicle_detail(request, vehicle_id):
   
    vehicle = get_object_or_404(Vehicle, vehicle_id=vehicle_id)
    ratings = vehicle.ratings.all()  # Get all ratings for the vehicle
    
 
    avg_rating = vehicle.average_rating()  
    count_ratings = vehicle.rating_count()  # Number of ratings for the vehicle

   
    avg_full_stars = int(avg_rating)  # Number of full stars
    avg_half_star = 1 if avg_rating - avg_full_stars >= 0.5 else 0  
    avg_empty_stars = 5 - avg_full_stars - avg_half_star  
    avg_stars = ['full'] * avg_full_stars + ['half'] * avg_half_star + ['empty'] * avg_empty_stars

    # Prepare the individual ratings and their stars
    star_ratings = []
    for rating in ratings:
        individual_rating = rating.rating  # Assuming 'rating' is a float value between 1 and 5

        # Calculate stars for each individual rating
        full_stars = int(individual_rating)  # Number of full stars
        half_star = 1 if individual_rating - full_stars >= 0.5 else 0  # Half star if fraction >= 0.5
        empty_stars = 5 - full_stars - half_star  # Remaining stars should be empty
        stars = ['full'] * full_stars + ['half'] * half_star + ['empty'] * empty_stars
        
        # Add the stars list to the star_ratings
        star_ratings.append({
            'rating': rating,
            'stars': stars , # List of stars for this rating
            'created_at': rating.created_at,
        })

    # Pass the context data to the template
    context = {
        'vehicle': vehicle,
        'ratings': ratings,
        'star_ratings': star_ratings,  # List of dictionaries with rating and stars
        'avg_stars': avg_stars,  # Average stars list
        'avg_rating': avg_rating,  # Average rating value
        'count_ratings': count_ratings,  # Count of ratings
    }

    return render(request, 'read_vehicle_page.html', context)


@admin_or_staff_required
def update_vehicle_page(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, vehicle_id=vehicle_id)

    if request.method == 'POST':
        form = CreateVehicleForm(request.POST, request.FILES, instance=vehicle)

        if form.is_valid():
            form.save()
            return redirect('vehicle_list')  # Redirect after saving
    else:
        form = CreateVehicleForm(instance=vehicle)

    # Convert the blob image to base64 for rendering (if applicable)
    vehicle.image_base64 = get_image_base64(vehicle)

    return render(request, 'update_vehicle_page.html', {'form': form, 'vehicle': vehicle})

def get_image_base64(vehicle):
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

            return f"data:{mime_type};base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
    
    return None
        