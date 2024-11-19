from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rental_record.models import RentalRecord
from vehicles.models import Vehicle
from datetime import datetime
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone

@login_required
def booking_process(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, vehicle_id=vehicle_id)
    
    if request.method == "POST":
        start_date = request.POST.get("start_date")
        return_date = request.POST.get("return_date")
        
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        return_date = datetime.strptime(return_date, '%Y-%m-%d').date()
        
        conflicting_booking = RentalRecord.objects.filter(
            Q(vehicle=vehicle) & (
                Q(start_date__lte=return_date) & Q(return_date__gte=start_date)
            )
        ).exists()
        
        if conflicting_booking:
            return JsonResponse({"status": "error", "message": "The vehicle is already booked during the selected dates."})
        
        days_rented = max((return_date - start_date).days, 1)
        
        if days_rented == 1:
            total_amount = vehicle.vehicle_price
        else:
            total_amount = vehicle.vehicle_price + (vehicle.vehicle_price / 2) * (days_rented - 1)
        
        rental_record = RentalRecord(
            customer=request.user,
            vehicle=vehicle,
            start_date=start_date,
            return_date=return_date,
            total_amount=total_amount,
            days_rented=days_rented,
        )
        rental_record.set_payment_due_date(grace_period_days=3)
        rental_record.save()
        
        return JsonResponse({"status": "success", "redirect_url": "/booking_list/"})

    return render(request, "booking_process.html", {"vehicle": vehicle})

@login_required
def payment(request, rental_id):
    rental_record = get_object_or_404(RentalRecord, rental_id=rental_id)
    
    if timezone.now() > rental_record.payment_due_date and rental_record.payment_in_progress:
        return JsonResponse({"status": "expired", "message": "Payment grace period has expired. Booking canceled."})

    if request.method == "POST":
        rental_record.payment_status = True
        rental_record.payment_date = timezone.now()
        rental_record.payment_in_progress = False
        rental_record.save()
        
        return JsonResponse({"status": "success", "message": "Payment successful!"})

    return render(request, "payment.html", {"rental_record": rental_record})
    

