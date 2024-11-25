from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rental_record.models import RentalRecord
from vehicles.models import Vehicle
from datetime import datetime, timedelta
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
        
        if return_date < start_date:
            return JsonResponse({"status": "error", "message": "Return date cannot be earlier than the pickup date."})
        
        conflicting_booking = RentalRecord.objects.filter(
            Q(vehicle=vehicle) & (
                Q(start_date__lte=return_date) & Q(return_date__gte=start_date)
            )
        ).exists()
        
        if conflicting_booking:
            return JsonResponse({"status": "error", "message": "The vehicle is already booked during the selected dates."})
        
        # Calculate the days rented
        days_rented = max((return_date - start_date).days, 1)  # Ensure at least 1 day rental
        
        # Debugging: print the days rented value
        print(f"Days rented: {days_rented}")  # <-- Check the value of days_rented
        
        # Calculate total amount
        if days_rented == 1:
            total_amount = vehicle.vehicle_price  # For single-day rental, it's just the vehicle price
        else:
            additional_day_price = vehicle.vehicle_price / 2  # Additional cost per extra day
            total_amount = vehicle.vehicle_price + additional_day_price * (days_rented - 1)

        # Debugging: print the total amount calculated
        print(f"Total amount: {total_amount}")  # <-- Check the value of total_amount

        # Determine the grace period based on the start date
        now = timezone.now()
        now_local = timezone.localtime(now)

        if start_date <= now_local.date() + timedelta(days=1):
            grace_period_hours = 2
        else:
            grace_period_hours = 72

        payment_due_datetime = now_local + timedelta(hours=grace_period_hours)

        # Save the rental record
        rental_record = RentalRecord(
            customer=request.user,
            vehicle=vehicle,
            start_date=start_date,
            return_date=return_date,
            total_amount=total_amount,
            days_rented=days_rented,
            payment_due_date=payment_due_datetime,
        )
        rental_record.save()
        
        return JsonResponse({"status": "success", "redirect_url": "/booking_list/"})

    return render(request, "booking_process.html", {"vehicle": vehicle})



@login_required
def payment(request, rental_id):
    rental_record = get_object_or_404(RentalRecord, rental_id=rental_id)
    
    if timezone.now() > rental_record.payment_due_date and rental_record.payment_in_progress:
        rental_record.delete()
        return JsonResponse({"status": "expired", "message": "Payment grace period has expired. Booking canceled."})

    if request.method == "POST":
        rental_record.payment_status = True
        rental_record.payment_date = timezone.now()
        rental_record.payment_in_progress = False
        rental_record.save()
        
        return JsonResponse({"status": "success", "message": "Payment successful!"})

    return render(request, "payment.html", {"rental_record": rental_record})
