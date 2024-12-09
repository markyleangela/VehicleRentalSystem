from django.shortcuts import render, redirect, get_object_or_404
from vehicles.models import Vehicle
from rental_record.models import RentalRecord
import base64
from io import BytesIO
from PIL import Image
import logging
from django.contrib.auth.models import User
from user_profile.models import ProfileInfo
from .decorator import admin_or_staff_required


# Create your views here.
@admin_or_staff_required
def dashboard_view(request):
    return render(request, 'admin_dashboard.html')

@admin_or_staff_required
def booking_list_view(request):
    rental_records = RentalRecord.objects.all()  # Get all rental records
    return render(request, 'booking_list_admin.html', {'rental_records': rental_records})

@admin_or_staff_required
def vehicle_list_view(request):
    status_filter = request.GET.get('status', 'operational')  # Get the filter status from the GET request

    # Define the filters based on status
    if status_filter == 'all':
        vehicles = Vehicle.objects.all()
    elif status_filter == 'available':
        vehicles = Vehicle.objects.filter(vehicle_status='Available', vehicle_is_deleted=False)
    elif status_filter == 'in_use':
        vehicles = Vehicle.objects.filter(vehicle_status='In Use', vehicle_is_deleted=False)
    elif status_filter == 'deleted':
        vehicles = Vehicle.objects.filter(vehicle_is_deleted=True)
    else:
        vehicles = Vehicle.objects.filter(vehicle_is_deleted=False)


    for vehicle in vehicles:
        if vehicle.vehicle_blobimage:
            image = Image.open(BytesIO(vehicle.vehicle_blobimage))

            buffer = BytesIO()
            image_format = image.format if image.format else 'JPEG'

            if image_format == 'PNG' and image.mode == 'RGBA':
                image.save(buffer, format='PNG')
                mime_type = "image/png"
            else:
                image = image.convert('RGB')
                image.save(buffer, format='JPEG')
                mime_type = "image/jpeg"

            vehicle.image_base64 = f"data:{mime_type};base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
        else:
            vehicle.image_base64 = None

    if request.method == 'POST':
        if 'delete_vehicle' in request.POST:
            vehicle_id = request.POST.get('delete_vehicle')
            logger.debug(f"Attempting to delete vehicle with ID: {vehicle_id}")
            if vehicle_id and vehicle_id.isdigit():
                vehicle_to_delete = get_object_or_404(Vehicle, pk=vehicle_id)
                vehicle_to_delete.vehicle_is_deleted = True
                vehicle_to_delete.save()
                logger.info(f"Deleted vehicle ID: {vehicle_id}")
                return redirect('vehicle_list')
            else:
                logger.warning(f"Invalid vehicle ID: {vehicle_id}")

        elif 'vehicle_id' in request.POST:
            vehicle_id = request.POST.get('vehicle_id')
            if vehicle_id:
                vehicle_detail = get_object_or_404(Vehicle, pk=vehicle_id)

    return render(request, 'vehicle_list.html', {'vehicles': vehicles})


@admin_or_staff_required
def users_view(request):
    non_admin_users = User.objects.filter(is_staff=False, is_superuser=False)
    profiles = ProfileInfo.objects.filter(user__in=non_admin_users)
    
    status_filter = request.GET.get('status', 'active')  # Get the filter status from the GET request

    # Define the filters based on status
    if status_filter == 'all':
        profiles = profiles
    elif status_filter == 'deleted':
        profiles = ProfileInfo.objects.filter(is_deleted=True, user__in=non_admin_users)
    else:
        profiles = ProfileInfo.objects.filter(is_deleted=False, user__in=non_admin_users)
    
    for profile in profiles:
        user = profile.user  # Access the related User object
        
        # Add first_name and last_name for template rendering
        profile.first_name = user.first_name
        profile.last_name = user.last_name
        profile.email = user.email

        # Convert profile_image to base64 if it exists
        if profile.profile_image:
            try:
                image = Image.open(BytesIO(profile.profile_image))
                buffer = BytesIO()
                image_format = image.format if image.format else 'JPEG'

                if image_format == 'PNG' and image.mode == 'RGBA':
                    image.save(buffer, format='PNG')
                    mime_type = "image/png"
                else:
                    image = image.convert('RGB')
                    image.save(buffer, format='JPEG')
                    mime_type = "image/jpeg"

                profile.image_base64 = f"data:{mime_type};base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
            except Exception as e:
                print(f"Error processing image for user {profile.user.username}: {e}")
                profile.image_base64 = None
        else:
            profile.image_base64 = None

        if request.method == 'POST':
            if 'delete_user' in request.POST:
                profile_id = request.POST.get('delete_user')
                print(f"Attempting to mark user profile as deleted with ID: {profile_id}")

                if profile_id and profile_id.isdigit():
                    # Fetch the ProfileInfo object by its primary key
                    profile_to_delete = get_object_or_404(ProfileInfo, pk=profile_id)
                    profile_to_delete.is_deleted = True  # Mark the profile as deleted
                    profile_to_delete.save()
                    print(f"Marked user profile as deleted: {profile_id}")
                    return redirect('users')
                else:
                    print(f"Invalid profile ID: {profile_id}")
    return render(request, 'user_list.html', {'users': profiles})
