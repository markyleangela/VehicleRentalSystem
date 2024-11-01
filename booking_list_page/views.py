from django.shortcuts import render
from rental_record.models import RentalRecord
from django.contrib.auth.decorators import login_required

# Ensure only logged-in users can access the booking list
@login_required
def booking_list(request):
    # Filter records by the logged-in user
    records = RentalRecord.objects.filter(customer=request.user)

    # Add calculated days_rented for each record
    for record in records:
        if record.return_date:
            record.days_rented = max((record.return_date - record.start_date).days, 0)
            record.total_amount = record.days_rented * record.vehicle.vehicle_price
        else:
            
            record.days_rented = "Not Returned"

    # Print for debugging
    print(f"Logged in user: {request.user}")

    # Render the booking list template with calculated days
    return render(request, 'booking_list.html', {'records': records})
