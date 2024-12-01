import random
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
import re
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse


from django.contrib import messages

from license.models import License
from .models import User, EmailConfirmation, LicenseConfirmation
from .forms import EmailVerificationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from .forms import CustomPasswordChangeForm


def activate_email(request, user, to_email):
    # Add a success message
    messages.success(
        request,
        f'Dear <b>{user}</b>, please check your email at <b>{to_email}</b> to activate your account.'
    )

def generate_confirmation_code():
    return str(random.randint(100000, 999999))

@login_required
def send_confirmation_email(user_email, confirmation_code):
    subject = 'Email Confirmation'
    message = f'Click the link to confirm your email: http://localhost:8000/profile/confirm/ your confirmation code is {confirmation_code}'

    from_email = 'markyleangela@gmail.com'
    recipient_list = [user_email]
    
    send_mail(subject, message, from_email, recipient_list)

@login_required
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

@login_required
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

        # Check the license number validation and set user status
    
        profile.verification_status = "Verified" if profile.license_verified else "Unverified"
        profile.image_base64 = process_profile_image(profile)
    except ProfileInfo.DoesNotExist:
        profile = None
    
    # Determine user status for display
    

    return render(request, 'user_profile.html', {'profile': profile, 'user': request.user})



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

from .forms import LicenseVerificationForm

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

    profile, created = ProfileInfo.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = EmailVerificationForm(request.POST, user=request.user)
        if form.is_valid():
  
            profile_info = form.save()
            user = request.user
            user.email = profile_info.email
            user.save()  
            confirmation_code = generate_confirmation_code()

            email_confirmation, created = EmailConfirmation.objects.update_or_create(
                user=profile,
                defaults={'code': confirmation_code}
            )

            send_confirmation_email(profile_info.email, confirmation_code)
            print("YES IT PASSED")
            messages.success(
                request, 
                'A confirmation email has been sent to your registered email address. Please check your inbox.'
            )

            return redirect('confirm_email')  
        else:
            print("NO IT DID NOT PASS")
        
            messages.error(request, 'There was an error with your submission.')
    else:
    
        form = EmailVerificationForm(user=request.user)

    context = {
        'form': form,
        'profile': profile
    }
    return render(request, 'verify_email.html', context)
