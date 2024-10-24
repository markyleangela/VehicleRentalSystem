from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from user_profile.models import ProfileInfo
import base64
from io import BytesIO
from PIL import Image
import os
from django.conf import settings
from django.templatetags.static import static  # Import static for default image
from django.contrib.auth import logout


@login_required
def update_profile(request):
    # Get or create the profile for the logged-in user
    profile, created = ProfileInfo.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            # Save form data (first name, last name, etc.)
            form.save()  

            # Check for the image upload
            if 'profile_image' in request.FILES and request.FILES['profile_image']:
                # Read and save the uploaded image as a binary blob
                profile.profile_image = request.FILES['profile_image'].read()  
                profile.save()  # Save the updated profile image

            return redirect('profile_page')
    else:
        form = ProfileForm(instance=profile, user=request.user)

    # Process the image for rendering
    if profile.profile_image:
        try:
            # Convert the binary image (blob) to base64 for rendering in HTML
            image = Image.open(BytesIO(profile.profile_image))
            
            # Convert image mode if necessary
            if image.mode == 'RGBA':
                image = image.convert('RGB')
            
            # Save image to a buffer in the appropriate format
            buffer = BytesIO()
            image_format = image.format if image.format else 'JPEG'  # Default to JPEG
            image.save(buffer, format=image_format)
            
            # Get MIME type and base64 encode the image
            mime_type = f"image/{image_format.lower()}"
            profile.image_base64 = f"data:{mime_type};base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
        except Exception as e:
            print(f"Error processing image: {e}")
            profile.image_base64 = None
    else:
        # If no profile image, load the default image and encode it as base64
        default_image_path = static('images/default-profile.jpg')
        try:
            with open(os.path.join(settings.BASE_DIR, default_image_path), 'rb') as default_image_file:
                default_image = Image.open(default_image_file)
                
                if default_image.mode == 'RGBA':
                    default_image = default_image.convert('RGB')
                
                buffer = BytesIO()
                default_image.save(buffer, format='JPEG')  # Save as JPEG
                profile.image_base64 = f"data:image/jpeg;base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
        except FileNotFoundError:
            profile.image_base64 = None  # Handle missing default image

    return render(request, 'update_profile.html', {'form': form, 'profile': profile})





@login_required
def view_profile(request):
    try:
        profile = ProfileInfo.objects.get(user=request.user)
        
        if profile.profile_image:
            try:
                # Convert the binary image (blob) to base64 for rendering in HTML
                image = Image.open(BytesIO(profile.profile_image))
                
                # Convert image mode if necessary
                if image.mode == 'RGBA':
                    image = image.convert('RGB')
                
                # Save image to a buffer in the appropriate format
                buffer = BytesIO()
                image_format = image.format if image.format else 'JPEG'  # Default to JPEG
                image.save(buffer, format=image_format)
                
                # Get MIME type and base64 encode the image
                mime_type = f"image/{image_format.lower()}"
                profile.image_base64 = f"data:{mime_type};base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
            except Exception as e:
                print(f"Error processing image: {e}")
                profile.image_base64 = None
        else:
            # If no profile image, load the default image and encode it as base64
            default_image_path = static('images/default-profile.jpg')  # Use static method for default image
            try:
                with open(os.path.join(settings.BASE_DIR, default_image_path), 'rb') as default_image_file:
                    default_image = Image.open(default_image_file)
                    
                    if default_image.mode == 'RGBA':
                        default_image = default_image.convert('RGB')
                    
                    buffer = BytesIO()
                    default_image.save(buffer, format='JPEG')  # Save as JPEG
                    profile.image_base64 = f"data:image/jpeg;base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
            except FileNotFoundError:
                profile.image_base64 = None  # Handle missing default image
    except ProfileInfo.DoesNotExist:
        profile = None
    
    return render(request, 'user_profile.html', {'profile': profile, 'user': request.user})



