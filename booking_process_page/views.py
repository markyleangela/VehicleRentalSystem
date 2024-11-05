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
        
        rental_record = RentalRecord.objects.create(
            customer=request.user,
            vehicle=vehicle,
            start_date=start_date,
            return_date=return_date,
            total_amount=total_amount,
            days_rented=days_rented
        )
        
        return redirect("booking_list")

    return render(request, "booking_process.html", {"vehicle": vehicle})
