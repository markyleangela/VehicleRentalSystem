from django import forms
from django.contrib.auth.models import User
from user_profile.models import ProfileInfo
from django.contrib.auth.forms import PasswordChangeForm
from license.models import License
import uuid
from django.core.mail import send_mail


class PersonalDetailsForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label='First Name')
    last_name = forms.CharField(max_length=30, required=False, label='Last Name')
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
 
    class Meta:
        model = ProfileInfo
        fields = ['first_name', 'last_name', 'phone_number', 'birth_date']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PersonalDetailsForm, self).__init__(*args, **kwargs)
        
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
           

    def save(self, commit=True):
        user = self.instance.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

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
                return False  # 
            profile.license_verified = True
            return True  
        
        except License.DoesNotExist:
            profile.license_verified = False
            return False  # No matching license record found

    
    def save(self, commit=True):
       
        profile_info, created = ProfileInfo.objects.get_or_create(user=self.user)
        
        profile_info.license_no = self.cleaned_data.get('license_no')
        profile_info.email = self.cleaned_data.get('email')

        if commit:
            profile_info.save()

        return profile_info





from django import forms
from django.core.exceptions import ValidationError
from .models import ProfileInfo  # Update to match your actual model import

class EmailVerificationForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = ProfileInfo
        fields = ['email']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Extract the user from kwargs
        super(EmailVerificationForm, self).__init__(*args, **kwargs)

       
        if self.user and self.user.email:
            self.fields['email'].initial = self.user.email

    def clean_email(self):
        email = self.cleaned_data.get('email')

       
        if ProfileInfo.objects.exclude(user=self.user).filter(user__email=email).exists():
            raise forms.ValidationError("This email is already in use by another user.")

        return email

    def save(self, commit=True):
      
        profile_info, created = ProfileInfo.objects.get_or_create(user=self.user)
        profile_info.email = self.cleaned_data.get('email')
       
        if commit:
            profile_info.save()

        return profile_info





