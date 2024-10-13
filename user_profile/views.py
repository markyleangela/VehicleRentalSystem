from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile
import base64
from io import BytesIO
from PIL import Image

@login_required
def update_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()  # Save profile and user data
            return redirect('user_profile')  # Redirect to the profile view after saving
    else:
        form = ProfileForm(instance=profile, user=request.user)  # Pass user to prepopulate first and last name

    return render(request, 'update_profile.html', {'form': form})

@login_required
def view_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None 

    return render(request, 'user_profile.html', {'profile': profile, 'user': request.user})
