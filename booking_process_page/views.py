from django.shortcuts import render

# Create your views here.
def booking_form(request):
    if request.method == 'POST':
        # Handle booking form submission
        pickup_date = request.POST.get('pickup_date')
        return_date = request.POST.get('return_date')
        # Add your form processing logic here

    return render(request, 'booking_process_page/booking_form.html')