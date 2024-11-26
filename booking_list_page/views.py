from django.shortcuts import render
from rental_record.models import RentalRecord
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def booking_list(request):
    now = timezone.now()
    now_local = timezone.localtime(now)
    overdue_rentals = RentalRecord.objects.filter(payment_status = False, payment_due_date__lte = now_local)

    for rental in overdue_rentals:
        # Edit in the future to change the rental_status to Cancelled
        # Test purposes only
        rental.delete()

    records = RentalRecord.objects.filter(customer=request.user)

    for record in records:
        if record.return_date:
            record.days_rented = max((record.return_date - record.start_date).days, 1)
            record.total_amount = record.days_rented * record.vehicle.vehicle_price
        else:
            record.days_rented = "Not Returned"

        record.payment_due_date_display = record.payment_due_date if record.payment_due_date else "Not Set"

    return render(request, 'booking_list.html', {'records': records})

