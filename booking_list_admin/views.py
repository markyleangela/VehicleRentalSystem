from django.shortcuts import render, get_object_or_404
from django.utils import timezone
import json
from rental_record.models import RentalRecord
# Create your views here.

def rental_details_view(request, rental_id):
    record = RentalRecord.objects.get(rental_id=rental_id)
    return render(request, 'rental_details_admin.html', {'rental_record': record})

from django.http import JsonResponse
from rental_record.models import RentalRecord

# def handle_action(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         action = data.get("action")
#         rental_id = data.get("rental_id")

#         try:
#             rental_record = RentalRecord.objects.get(rental_id=rental_id)
#         except RentalRecord.DoesNotExist:
#             return JsonResponse({"error": "Rental record not found."}, status=404)

#         # Perform actions
#         if action == "cancel":
#             rental_record.rental_status = "cancelled"
#         elif action == "book" and rental_record.payment_status == "paid" and rental_record.rental_status == "pending":
#             rental_record.rental_status = "booked"
#         elif action == "release" and rental_record.rental_status == "booked":
#             rental_record.rental_status = "in_use"
#         elif action == "return" and rental_record.rental_status == "in_use":
#             rental_record.rental_status = "returned"
#         elif action == "complete" and rental_record.rental_status == "returned":
#             rental_record.rental_status = "completed"
#         elif action == "extend" and rental_record.rental_status == "overdue_pending":
#             return JsonResponse({"redirect": "/extend-url/"})  # Example of redirect URL
#         else:
#             return JsonResponse({"error": "Invalid action or conditions not met."}, status=400)

#         rental_record.save()
#         return JsonResponse({"message": f"{action.capitalize()} action performed successfully!"})
#     return JsonResponse({"error": "Invalid request method."}, status=405)

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

def rental_details_view(request, rental_id):
    rental_record = get_object_or_404(RentalRecord, rental_id=rental_id)

    # Sets the rental_status based on the admin's actions
    if request.method == "POST":
        action = request.POST.get('action')  
        
        if action == "cancel":
            rental_record.rental_status = "cancelled"
            rental_record.save()
            return JsonResponse({"status": "success", "message": "Vehicle released."})

        elif action == "book":
            rental_record.rental_status = "booked"
            rental_record.save()
            return JsonResponse({"status": "success", "message": "Vehicle released."})

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

        elif rental_record.rental_status == "overdue_pending" and action == "complete":
            rental_record.rental_status = "overdue_returned"
            rental_record.save()
            return JsonResponse({"status": "success", "message": "Overdue booking completed."})

        elif action == "extend":
            rental_record.rental_status = "overdue_extended"
            rental_record.save()
            return JsonResponse({"status": "success", "message": "Booking extended."})

        else:
            return JsonResponse({"status": "error", "message": "Invalid action or rental status."})

    return render(request, "rental_details_admin.html", {"rental_record": rental_record})
