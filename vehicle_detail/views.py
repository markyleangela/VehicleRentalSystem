from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from vehicles.models import Vehicle
from vehicles.models import Rating


def vehicle_detail(request, vehicle_id):
    # Get the vehicle object by vehicle_id
    vehicle = get_object_or_404(Vehicle, vehicle_id=vehicle_id)

    # Fetch all ratings for the vehicle
    ratings = vehicle.ratings.all()  # Get all ratings for the vehicle
    
    # Calculate the average rating
    avg_rating = vehicle.average_rating()  # Assume this method calculates average rating
    count_ratings = vehicle.rating_count()  # Number of ratings for the vehicle

    # Calculate stars for the average rating
    avg_full_stars = int(avg_rating)  # Number of full stars
    avg_half_star = 1 if avg_rating - avg_full_stars >= 0.5 else 0  # Add half star if fraction >= 0.5
    avg_empty_stars = 5 - avg_full_stars - avg_half_star  # Remaining stars should be empty
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
            'stars': stars  # List of stars for this rating
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

    return render(request, 'vehicle_detail.html', context)
