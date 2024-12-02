from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PersonalDetailsForm
from user_profile.models import ProfileInfo
import base64
from io import BytesIO
from PIL import Image
import os
from django.conf import settings
from django.templatetags.static import static  # Import static for default image
from django.contrib.auth import logout
import re

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
import six
from django.http import Http404, HttpResponse

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from django.contrib import messages

from license.models import License
from .models import User, EmailConfirmation
from .forms import EmailVerificationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from .forms import CustomPasswordChangeForm
import uuid

from .forms import LicenseVerificationForm
from .models import LicenseConfirmation
import random

def activate_email(request, user, to_email):
    # Add a success message
    messages.success(
        request,
        f'Dear <b>{user}</b>, please check your email at <b>{to_email}</b> to activate your account.'
    )

def generate_confirmation_code():
    return str(random.randint(100000, 999999))

def send_confirmation_email(user_email, confirmation_code):
    subject = 'Email Confirmation'
    message = f'Your confirmation code is {confirmation_code}'

    from_email = 'markyleangela@gmail.com'
    recipient_list = [user_email]
    
    send_mail(subject, message, from_email, recipient_list)

def confirm_email(request):
    profile, created = ProfileInfo.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        code = request.POST['code']

        try:
            # Find the confirmation record
            confirmation = EmailConfirmation.objects.get(code=code)
            
            user = confirmation.user
    
            # Activate the user
            user.is_active = True
            user.save()

            profile.email_verified = True
            profile.save()

            # Delete the confirmation record
            confirmation.delete()
            
            return redirect('profile_page')
        except EmailConfirmation.DoesNotExist:
            return HttpResponse("Invalid or expired confirmation code.", status=400)

    return render(request, 'activate_user.html')

def confirm_license(request):
    profile, created = ProfileInfo.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        code = request.POST['code']

        try:
            # Find the confirmation record
            confirmation = LicenseConfirmation.objects.get(code=code)
            
            user = confirmation.user
    
            # Activate the user
            user.is_active = True
            user.save()

            profile.license_verified = True
            if profile.email_verified:
                profile.user_verified = True
            profile.save()

            # Delete the confirmation record
            confirmation.delete()
            
            return redirect('profile_page')
        except LicenseConfirmation.DoesNotExist:
            return HttpResponse("Invalid or expired confirmation code.", status=400)

    return render(request, 'activate_user.html')

@login_required
def process_profile_image(profile):

 

    if profile.profile_image:
        try:
        
            image = Image.open(BytesIO(profile.profile_image))
            
       
            if image.mode == 'RGBA':
                image = image.convert('RGB')
            
           
            buffer = BytesIO()
            image_format = image.format if image.format else 'JPEG'
            image.save(buffer, format=image_format)
            
        
            mime_type = f"image/{image_format.lower()}"
            return f"data:{mime_type};base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
        except Exception as e:
            print(f"Error processing image: {e}")
            return None
    else:
       
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
def update_details(request):
    profile, created = ProfileInfo.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = PersonalDetailsForm(request.POST, instance=profile, user=request.user)
        
        if form.is_valid():
            # Save form data (like first name, last name, etc.)
            email = form.cleaned_data.get('email')
            
            if email != profile.user.email:
                profile.email_verified = False
            profile.save()
            form.save(commit=True)
            
            if 'profile_image' in request.FILES and request.FILES['profile_image']:
                # Save the profile image
                profile.profile_image = request.FILES['profile_image'].read()
                profile.save()

            # Redirect to the profile page
            return redirect('profile_page')

    else:
        form = PersonalDetailsForm(instance=profile, user=request.user)

    return render(request, 'update_details.html', {'form': form, 'profile': profile})

@login_required
def view_profile(request):
    try:
        profile = ProfileInfo.objects.get(user=request.user)
        print("this is in the view_profile:" + str(profile.user_verified))
        # Check the license number validation and set user status
    
        profile.verification_status = "Verified" if profile.license_verified else "Unverified"
        profile.image_base64 = process_profile_image(profile)
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


@login_required
def change_password(request):
    profile, created = ProfileInfo.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()  # Save the new password
            update_session_auth_hash(request, user)  # Keep the user logged in
            return redirect('login_page')  # Redirect to the profile page after success
    else:
        form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'account_info.html', {
        'form': form,  # Pass the form to the template
        'profile': profile,  # Pass the profile to the template if needed
    })


@login_required
def license_verification_view(request):
    profile, created = ProfileInfo.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = LicenseVerificationForm(request.POST, user=request.user)  # Pass the logged-in user to the form
        
        if form.is_valid():
            profile, created = ProfileInfo.objects.get_or_create(user=request.user)
            
            license_number = form.cleaned_data.get('license_no')
            
            

            confirmation_code = generate_confirmation_code()
            
    
            email_confirmation, created = LicenseConfirmation.objects.update_or_create(
                user=profile,
                defaults={'code': confirmation_code}
            )
            send_confirmation_email(profile.user.email, confirmation_code)

            profile.license_no = license_number
            
            profile.save()
            return redirect('confirm_license')
        else:
            profile.license_verified = False 

            return render(request, 'verify_license.html', {'form': form, 'profile': profile})
    else:
        form = LicenseVerificationForm(user=request.user)  
    return render(request, 'verify_license.html', {'form': form, 'profile': profile})


@login_required
def email_verification_form(request):
    """Handles email verification."""
    profile, created = ProfileInfo.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = EmailVerificationForm(request.POST, user=request.user)
        if form.is_valid():
            # Save the email to the user's profile
            profile_info = form.save()

            # Generate a confirmation code
            confirmation_code = generate_confirmation_code()

            # Update or create an email confirmation entry
            email_confirmation, created = EmailConfirmation.objects.update_or_create(
                user=profile,
                defaults={'code': confirmation_code}
            )

            # Send the confirmation email
            send_confirmation_email(profile_info.email, confirmation_code)
            print("YES IT PASSED")
            messages.success(
                request, 
                'A confirmation email has been sent to your registered email address. Please check your inbox.'
            )

            return redirect('confirm_email')  # Adjust the redirect to your confirmation page
        else:
            print("NO IT DID NOT PASS")
            # Handle form errors
            messages.error(request, 'There was an error with your submission.')
    else:
        # Pre-fill the form with the current user's email
        form = EmailVerificationForm(user=request.user)

    context = {
        'form': form,
        'profile': profile
    }
    return render(request, 'verify_email.html', context)

