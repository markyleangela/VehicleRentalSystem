from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Processing the data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Login the user
                login(request, user)

                
                # Check if the user is an admin or staff
                if user.is_staff or user.is_superuser:
                    return redirect('vehicle_list')  # Redirect to the admin dashboard view
                else:
                    return redirect('home')  # Redirect to the home page for normal users

            else:
                # Return an error message if authentication fails
                form.add_error(None, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'login_page.html', {'form': form})