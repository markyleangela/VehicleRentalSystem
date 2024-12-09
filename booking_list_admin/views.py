from django.shortcuts import render, get_object_or_404, redirect
from rental_record.models import RentalRecord
from django.http import JsonResponse

# Create your views here.
from django.shortcuts import render, get_object_or_404
from rental_record.models import RentalRecord
from django.http import JsonResponse

def rental_details_view(request, rental_id):
    rental_record = get_object_or_404(RentalRecord, rental_id=rental_id)

    if request.method == "POST":
        action = request.POST.get('action')

        if action == "cancel":
            rental_record.rental_status = "cancelled"
            rental_record.save()
            return JsonResponse({"status": "success", "message": "Booking Cancelled."})

        elif action == "book":
            rental_record.rental_status = "booked"
            rental_record.save()
            return JsonResponse({"status": "success", "message": "Successfully booked."})

        elif action == "release":
            rental_record.rental_status = "in_use"
            rental_record.save()
            return JsonResponse({"status": "success", "message": "Vehicle released."})

        elif action == "return":
            rental_record.rental_status = "returned"
            rental_record.save()
            return JsonResponse({"status": "success", "message": "Vehicle returned."})

        elif action == "complete":
            if rental_record.rental_status == "overdue_pending":
                rental_record.rental_status = "overdue_returned"
            else:
                rental_record.rental_status = "completed"
            rental_record.save()
            return JsonResponse({"status": "success", "message": "Booking completed."})

        elif action == "extend":
            rental_record.rental_status = "overdue_extended"
            rental_record.save()
            return JsonResponse({
                "status": "success", 
                "message": "Booking extended.",
                "redirect_url": "/admin_booking/{}/rental_detail/".format(rental_record.rental_id)
            })

        else:
            return JsonResponse({"status": "error", "message": "Invalid action or rental status."})

    return render(request, "rental_details_admin.html", {"rental_record": rental_record})
