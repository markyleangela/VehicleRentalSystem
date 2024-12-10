from django.shortcuts import render, get_object_or_404, redirect
from rental_record.models import RentalRecord
from django.http import JsonResponse
from django.utils.timezone import now

def rental_details_view(request, rental_id):
    rental_record = get_object_or_404(RentalRecord, rental_id=rental_id)


    if request.method == "POST":
        action = request.POST.get('action')

        if action == "cancel":
            rental_record.rental_status = "cancelled"
            rental_record.save()
            return redirect('bookings')  # Redirect to the booking list after canceling

        elif action == "book":
            rental_record.rental_status = "booked"
            rental_record.save()
            return redirect('bookings')  # Redirect to the booking list after booking

        elif action == "release":
            rental_record.rental_status = "in_use"
            rental_record.save()
            return redirect('bookings')  # Redirect to the booking list after releasing the vehicle

        elif action == "return":
            rental_record.rental_status = "returned"
            rental_record.save()
            return redirect('bookings')  # Redirect to the booking list after returning the vehicle

        elif action == "complete":
            if rental_record.rental_status == "overdue_pending":
                rental_record.rental_status = "overdue_returned"
            else:
                rental_record.rental_status = "completed"
            rental_record.save()
            return redirect('bookings')  # Redirect to the booking list after completing the booking

        elif action == "extend":
            rental_record.rental_status = "overdue_extended"
            rental_record.save()
            return redirect('bookings')  # Redirect to the booking list after extending the booking

        else:
            return JsonResponse({"status": "error", "message": "Invalid action or rental status."})

    current_date = now().date()

    context = {
        'rental_record': rental_record,
        'current_date': current_date,
    }
    return render(request, "rental_details_admin.html", context)
