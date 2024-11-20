from django.shortcuts import render
from rental_record.models import RentalRecord
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def booking_list(request):
    records = RentalRecord.objects.filter(customer=request.user)

    for record in records:
        if record.return_date:
            record.days_rented = max((record.return_date - record.start_date).days, 0)
            record.total_amount = record.days_rented * record.vehicle.vehicle_price
        else:
            record.days_rented = "Not Returned"

        record.payment_due_date_display = record.payment_due_date if record.payment_due_date else "Not Set"

    return render(request, 'booking_list.html', {'records': records})
