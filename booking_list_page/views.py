from django.shortcuts import render, redirect, get_object_or_404
from rental_record.models import RentalRecord
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def booking_list(request):
    # Fetch rental records for the logged-in user
    records = RentalRecord.objects.filter(customer=request.user)

    # Current date for comparisons
    current_date = timezone.now()

    for record in records:
        record.transaction_id = record.generate_transaction_id()
        record.save()
        if not record.payment_status:
            if record.payment_due_date < current_date: #not paid and beyond grace period
                record.rental_status = 'cancelled'
            record.save()
            continue
        
           
        

        # Calculate days rented and total amount
        if record.return_date:
            record.days_rented = max((record.return_date - record.start_date).days, 1)
            record.total_amount = record.days_rented * record.vehicle.vehicle_price
        else:
            record.days_rented = "Not Returned"

        # Display payment due date or "Not Set" if null
        record.payment_due_date_display = record.payment_due_date if record.payment_due_date else "Not Set"

    # Render the template with updated records
    return render(request, 'booking_list.html', {'records': records})


@login_required
def rental_detail_view(request, rental_id):
    # Fetch rental records for the logged-in user
    record = RentalRecord.objects.get(rental_id=rental_id)
    # record = RentalRecord.objects.filter(customer=request.user, rental_id = rental_id)

    return render(request, 'rental_details.html', {'rental_record': record})
