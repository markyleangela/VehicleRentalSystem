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
                return redirect('home')
            else:
                # Return an error message if authentication fails
                form.add_error(None, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'login_page.html', {'form': form})
