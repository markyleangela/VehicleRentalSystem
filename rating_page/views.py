from django.shortcuts import render, redirect, get_object_or_404
from vehicles.models import Vehicle
from .forms import RatingForm
from rental_record.models import RentalRecord
from django.http import HttpResponse

def vehicle_rating_detail(request, vehicle_id):
    # Retrieve the vehicle by ID
    vehicle = get_object_or_404(Vehicle, vehicle_id=vehicle_id)

    # Fetch all ratings for the vehicle
    ratings = vehicle.ratings.all()
    avg_rating = vehicle.average_rating()
    count_ratings = vehicle.rating_count()

    # Find an unrated rental record for this user and vehicle, if any
    rental_record = RentalRecord.objects.filter(customer=request.user, vehicle=vehicle, is_rated=False).first()

    # If no rental record exists, inform the user that they can't rate the vehicle
    if not rental_record:
        return HttpResponse("You need to rent this vehicle before you can leave a rating.")

    # Handle form submission for rating
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
