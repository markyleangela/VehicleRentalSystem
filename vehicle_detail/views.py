from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from vehicles.models import Vehicle
from vehicles.models import Rating

def vehicle_detail(request, vehicle_id):
    # Get the vehicle object by vehicle_id
    vehicle = get_object_or_404(Vehicle, vehicle_id=vehicle_id)

    # Fetch all ratings for the vehicle
    ratings = vehicle.ratings.all()
    avg_rating = vehicle.average_rating()
    count_ratings = vehicle.rating_count()

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
        'stars': stars,
    }

    return render(request, 'vehicle_detail.html', context)
