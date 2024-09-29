from django.shortcuts import render, redirect
from .forms import LoginForm

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Processing the data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Add authentication logic here
            return redirect('vehicle_list')  # Replace with your success URL
    else:
        form = LoginForm()

    return render(request, 'login_page.html', {'form': form})
