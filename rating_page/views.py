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

from django.shortcuts import render, redirect, get_object_or_404
from vehicles.models import Vehicle
from .forms import RatingForm
from rental_record.models import RentalRecord

from django.http import HttpResponse

def vehicle_rating_detail(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, vehicle_id=vehicle_id)  # Retrieve the vehicle by ID

    # Fetch all ratings for the vehicle
    ratings = vehicle.ratings.all()
    avg_rating = vehicle.average_rating()
    count_ratings = vehicle.rating_count()

    # Check if the user has rented this vehicle
    rental_record = RentalRecord.objects.filter(customer=request.user, vehicle=vehicle).first()

    # If no rental record exists, the user can't rate the vehicle
   

    # Check if the user has already rated the vehicle (you can add a condition to prevent double-rating)
    if rental_record.is_rated:
        return HttpResponse("You already rated this car")

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.vehicle = vehicle
            rating.user = request.user

            # Save the rating and mark the rental record as rated
            rating.save()
            rental_record.is_rated = True
            rental_record.save()

            return redirect('vehicle_detail', vehicle_id=vehicle.vehicle_id)
    else:
        form = RatingForm()

    # Calculate the number of stars to display (full, half, empty)
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

