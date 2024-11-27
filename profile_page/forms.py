from django import forms
from django.contrib.auth.models import User
from user_profile.models import ProfileInfo
from django.contrib.auth.forms import PasswordChangeForm
from license.models import License
import uuid
from django.core.mail import send_mail
from .models import EmailConfirmation

class PersonalDetailsForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label='First Name')
    last_name = forms.CharField(max_length=30, required=False, label='Last Name')
    email = forms.EmailField(required=True, label='Email')  # Added email field
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
 
    class Meta:
        model = ProfileInfo
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'birth_date']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PersonalDetailsForm, self).__init__(*args, **kwargs)
        
        if user:
            # Initialize fields with user's current information
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email  # Initialize email

    def save(self, commit=True):
        user = self.instance.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']  # Save email to user

        if commit:
            user.save()
            self.instance.save()
        return self.instance


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("The two password fields didn't match.")
        
        return new_password2




class LicenseVerificationForm(forms.ModelForm):
    license_no = forms.CharField(max_length=15, required=True)

    class Meta:
        model = ProfileInfo
        fields = ['license_no']  # Only license_no field for verification

    def __init__(self, *args, **kwargs):
        # Extract `user` from kwargs and pass it to the form instance
        self.user = kwargs.pop('user', None)
        super(LicenseVerificationForm, self).__init__(*args, **kwargs)

        if self.user:
            # Initialize `license_no` with current value from ProfileInfo if it exists
            profile_info = ProfileInfo.objects.filter(user=self.user).first()
            if profile_info:
                self.fields['license_no'].initial = profile_info.license_no

    def clean_license_no(self):
        license_no = self.cleaned_data.get('license_no')

        # Perform the license validation
        if not self.is_valid_license(license_no):
            raise forms.ValidationError("The license number does not match your details or is already used by another user.")

        return license_no

    def is_valid_license(self, license_no):
        profile = ProfileInfo.objects.filter(user=self.user).first()

        try:
           
            license_record = License.objects.get(
                license_number=license_no,
                licensee_name=self.user.first_name + " " + self.user.last_name,  
                birth_date=profile.birth_date     
            )
            
       
            if ProfileInfo.objects.exclude(user=self.user).filter(license_no=license_no).exists():
                profile.license_verified = False
                return False  # The license number is already taken by another user
            profile.license_verified = True
            return True  # All details match and license number is not taken by another user
        
        except License.DoesNotExist:
            profile.license_verified = False
            return False  # No matching license record found

    def save(self, commit=True):
        # Check if the ProfileInfo already exists for the current user
        profile_info, created = ProfileInfo.objects.get_or_create(user=self.user)
        
        # Assign license_no if it was updated
        profile_info.license_no = self.cleaned_data.get('license_no')

        if commit:
            profile_info.save()
        
        return profile_info



class EmailVerificationForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = ProfileInfo
        fields = ['email']  # Only the email field for verification

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Extract the user from kwargs
        super(EmailVerificationForm, self).__init__(*args, **kwargs)

        # Pre-fill email field with user's email if user is passed
        if self.user and self.user.email:
            self.fields['email'].initial = self.user.email


    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Ensure that the email matches the user's registered email
        if email != self.user.email:
            raise forms.ValidationError("The email does not match your registered email.")
        
        # Optionally, check if the email is already verified (in case it's not the first time submitting)
        profile = ProfileInfo.objects.filter(user=self.user).first()
        if profile and profile.email_verified:
            raise forms.ValidationError("Your email is already verified.")

        return email

    def save(self, commit=True):
        # Check if the ProfileInfo already exists for the current user
        profile_info, created = ProfileInfo.objects.get_or_create(user=self.user)
        
        # Assign email (although it should already be set)
        profile_info.email = self.cleaned_data.get('email')

        if commit:
            profile_info.save()

        return profile_info

    def send_confirmation_email(user_email, confirmation_code):
        subject = 'Email Confirmation'
        message = f'Click the link to confirm your email: http://localhost:8000/profile/confirm/ your confirmation code is {confirmation_code}'

        from_email = 'markyleangela@gmail.com'
        recipient_list = [user_email]
        
        send_mail(subject, message, from_email, recipient_list)




