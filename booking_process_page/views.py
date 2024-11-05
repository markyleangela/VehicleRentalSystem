from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rental_record.models import RentalRecord
from vehicles.models import Vehicle
from django.utils import timezone
from datetime import datetime
from django.http import Http404

@login_required
def booking_process(request, vehicle_id):
    try:
        vehicle = Vehicle.objects.get(vehicle_id=vehicle_id)
    except Vehicle.DoesNotExist:
        raise Http404("Vehicle not found.")

    if request.method == "POST":
        start_date = request.POST.get("start_date")
        return_date = request.POST.get("return_date")
        
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        return_date = datetime.strptime(return_date, '%Y-%m-%d').date()
        
        days_rented = max((return_date - start_date).days, 0)
        total_amount = days_rented * vehicle.vehicle_price
        
        rental_record = RentalRecord(
            customer=request.user,
            vehicle=vehicle,
            start_date=start_date,
            return_date=return_date,
            total_amount=total_amount,
            days_rented=days_rented
        )

        rental_record.save()
        
        return redirect("payment", rental_id=rental_record.rental_id)

    return render(request, "booking_process.html", {"vehicle": vehicle})




@login_required
def payment(request, rental_id):
    rental_record = get_object_or_404(RentalRecord, rental_id=rental_id)
    
    if request.method == "POST":
        rental_record.payment_status = True
        rental_record.payment_date = timezone.now()
        rental_record.save()
        
        return redirect("booking_confirmation", rental_id=rental_record.rental_id)

    return render(request, "payment.html", {"rental_record": rental_record})



@login_required
def booking_confirmation(request, rental_id):
    rental_record = get_object_or_404(RentalRecord, rental_id=rental_id)
    
    if rental_record.payment_status:
        return render(request, "booking_confirmation.html", {"rental_record": rental_record})
    else:
        return redirect('payment', rental_id=rental_id)
