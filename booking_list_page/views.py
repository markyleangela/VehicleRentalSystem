from django.shortcuts import render
from rental_record.models import RentalRecord
from django.contrib.auth.decorators import login_required

# Ensure only logged-in users can access the booking list
@login_required
def booking_list(request):
    # Filter records by the logged-in user (request.user)
    records = RentalRecord.objects.filter(customer=request.user)
    print(f"Logged in user: {request.user}")
    return render(request, 'booking_list.html', {'records': records})
