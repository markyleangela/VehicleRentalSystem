# from django.shortcuts import render, redirect
# from .forms import CreateVehicleForm

# def create_vehicle_page(request):
#     if request.method == 'POST':
#         form = CreateVehicleForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Processing the data
#             # model = form.cleaned_data['model']
#             # brand = form.cleaned_data['brand']
#             # vehicle_type = form.cleaned_data['vehicle_type']
#             # vehicle_price = form.cleaned_data['vehicle_price']
#             # vehicle_status = form.cleaned_data['vehicle_status']
#             # vehicle_blobimage = form.cleaned_data['vehicle_blobimage']
            
#             # vehicle = authenticate(request, 
#             #                        model=model, brand=brand, vehicle_type=vehicle_type, vehicle_price=vehicle_price, 
#             #                        vehicle_status = vehicle_status, vehicle_blobimage = vehicle_blobimage)
#             # if vehicle is not None:
#             #     # Add the vehicle
#             #     vehicle = form.save()
#             #     return redirect('vehicle_list')
#             form = CreateVehicleForm(request.POST, request.FILES)  # Don't forget to pass request.FILES for handling the image upload
#             if form.is_valid():
#                 form.save()  # Save the form (which saves the vehicle)
#                 return redirect('vehicle_list')  # Redirect to a vehicle list page or success page
#             else:
#                 # Return an error message if creating fails
#                 form.add_error(None, "Fill in the required fields.")
#     else:
#         form = CreateVehicleForm()

#     return render(request, 'create_vehicle_page.html', {'form': form})
from django.shortcuts import render, redirect
from .forms import CreateVehicleForm

def create_vehicle_page(request):
    if request.method == 'POST':
        form = CreateVehicleForm(request.POST, request.FILES)
        print("Form data received:", request.POST)
        if form.is_valid():
            print("Form is valid")
            vehicle = form.save()  # This should save the vehicle
            print("Vehicle saved to the database")  # Confirm saving
            return redirect('vehicle_list')  # Redirect after saving
        else:
            print("Form errors:", form.errors)  # Check for errors
    else:
        form = CreateVehicleForm()

    return render(request, 'create_vehicle_page.html', {'form': form})

# def create_vehicle_page(request):
#     if request.method == 'POST':
#         form = CreateVehicleForm(request.POST, request.FILES)  # Pass both request.POST and request.FILES
#         print("Form data received:", request.POST)  # Debugging print to check form data
#         if form.is_valid():
#             print("Form is valid")  # Debugging print to check form validation
#             form.save()  # Save the form (which saves the vehicle)
#             return redirect('vehicle_list')  # Redirect to a vehicle list page or success page
#         else:
#             print("Form errors:", form.errors)  # Debugging print to check form errors
#     else:
#         form = CreateVehicleForm()

#     return render(request, 'create_vehicle_page.html', {'form': form})
