from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, PersonalDetailsForm
from user_profile.models import ProfileInfo
import base64
from io import BytesIO
from PIL import Image
import os
from django.conf import settings
from django.templatetags.static import static  # Import static for default image
from django.contrib.auth import logout
import re

from license.models import License
from .forms import CustomPasswordChangeForm



def process_profile_image(profile):

    #Process the profile image for display. If no image is uploaded, use the default image.

    if profile.profile_image:
        try:
            # Convert the binary image to base64 for rendering in HTML
            image = Image.open(BytesIO(profile.profile_image))
            
            # Convert image mode if necessary
            if image.mode == 'RGBA':
                image = image.convert('RGB')
            
            # Save image to a buffer in the appropriate format
            buffer = BytesIO()
            image_format = image.format if image.format else 'JPEG'
            image.save(buffer, format=image_format)
            
            # Get MIME type and base64 encode the image
            mime_type = f"image/{image_format.lower()}"
            return f"data:{mime_type};base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
        except Exception as e:
            print(f"Error processing image: {e}")
            return None
    else:
        # If no profile image, load the default image and encode it as base64
        default_image_path = static('images/default-profile.jpg')
        try:
            with open(os.path.join(settings.BASE_DIR, default_image_path), 'rb') as default_image_file:
                default_image = Image.open(default_image_file)
                
                if default_image.mode == 'RGBA':
                    default_image = default_image.convert('RGB')
                
                buffer = BytesIO()
                default_image.save(buffer, format='JPEG')
                return f"data:image/jpeg;base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
        except FileNotFoundError:
            print("Default profile image not found.")
            return None


@login_required
def update_profile(request):
    # Get or create the profile for the logged-in user
    profile, created = ProfileInfo.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            # Save form data (first name, last name, etc.)
            form.save()

            # Validate the license number if it exists in the form
            license_number = form.cleaned_data.get('license_no')
            if license_number:
                if not is_valid_license(license_number, request.user):
                    form.add_error('license_no', 'Invalid license number.')
                    profile.user_status = False
                    return render(request, 'update_profile.html', {'form': form, 'profile': profile})
                elif not is_valid_license_format(license_number):
                    form.add_error('license_no', 'Invalid format ex. G00-000-000000')
                    profile.user_status = False
                    return render(request, 'update_profile.html', {'form': form, 'profile': profile})
                else:
                    profile.user_status = True  # Set verified status if valid
            else:
                profile.user_status = False  # Set unverified status if no license number

            profile.save()  

            # Check for the image upload
            if 'profile_image' in request.FILES and request.FILES['profile_image']:
                # Read and save the uploaded image as a binary blob
                profile.profile_image = request.FILES['profile_image'].read()
                profile.save() 

            return redirect('profile_page')
    else:
        form = ProfileForm(instance=profile, user=request.user)

    # Process the image for rendering
    profile.image_base64 = process_profile_image(profile)

    return render(request, 'update_profile.html', {'form': form, 'profile': profile})

@login_required
def update_details(request):
    # Get or create the profile for the logged-in user
    profile, created = ProfileInfo.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = PersonalDetailsForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            # Save form data (like first name, last name, etc.)
            form.save()
            return redirect('profile_page')
    else:
        form = PersonalDetailsForm(instance=profile, user=request.user)  # Load form with existing profile details

    return render(request, 'update_details.html', {'form': form, 'profile': profile})


@login_required
def view_profile(request):
    try:
        profile = ProfileInfo.objects.get(user=request.user)

        # Check the license number validation and set user status
    

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
        profile.verification_status = "Verified" if profile.user_status else "Unverified"
    except ProfileInfo.DoesNotExist:
        profile = None
    
    # Determine user status for display
    

    return render(request, 'user_profile.html', {'profile': profile, 'user': request.user})


def is_valid_license(license_number, user):
    # Check if the license exists in the License table (dummy data)
    if not License.objects.filter(license_number=license_number).exists():
        return False  # License number does not exist in dummy data

    # Check if the license number is unique to the user in ProfileInfo
    return not ProfileInfo.objects.exclude(user=user).filter(license_no=license_number).exists()

def is_valid_license_format(license_number):
    # Pattern: One uppercase letter followed by two digits, a dash, two digits, a dash, and then five digits
    pattern = r"^[A-Z]\d{2}-\d{2}-\d{6}$"
 
    return bool(re.match(pattern, license_number))



from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from .forms import CustomPasswordChangeForm

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in after changing password
            return redirect('profile')  # Redirect to the profile page or wherever you want
    else:
        form = CustomPasswordChangeForm(user=request.user)
    
    return render(request, 'user_profile.html', {'form': form})


