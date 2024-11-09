from django.shortcuts import render
from vehicles.models import Vehicle
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RatingForm

import base64
from io import BytesIO
from PIL import Image
import os
from django.templatetags.static import static 
from django.conf import settings
# Create your views here.

def vehicle_rating_detail(request, vehicle_id):
    # vehicle = get_object_or_404(Vehicle, vehicle_id=vehicle_id)
    vehicle = Vehicle.objects.get(vehicle_id=vehicle_id)  # Use get if you expect only one result



    ratings = vehicle.ratings.all()
    avg_rating = vehicle.average_rating()
    count_ratings = vehicle.rating_count()

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.vehicle = vehicle
            rating.user = request.user
            rating.save()
            return redirect('vehicle_detail', vehicle_id=vehicle.vehicle_id)
    else:
        form = RatingForm()

    full_stars = int(avg_rating)  # Full stars (e.g., 4 for 4.2)
    half_star = 1 if avg_rating - full_stars >= 0.5 else 0  # Half star if there's any fraction
    empty_stars = 5 - full_stars - half_star  # Remaining stars are empty


    stars = ['full'] * full_stars + ['half'] * half_star + ['empty'] * empty_stars
   
    context = {
        'vehicle': vehicle,
        'ratings': ratings,
        'avg_rating': avg_rating,
        'count_ratings': count_ratings,
        'form': form,
        'stars': stars,
    }
    return render(request, 'vehicle_rating.html', context)


