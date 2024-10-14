from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from accounts.forms import CustomUserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
        else:
            messages.error(request, "There was an error with your registration.")
    else:
        form = CustomUserRegistrationForm()

    return render(request, 'register.html', {'form': form})
