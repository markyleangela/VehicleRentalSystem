# forms.py
from django import forms
from django.contrib.auth.models import User
from user_profile.models import ProfileInfo

from django import forms
from user_profile.models import ProfileInfo

class ProfileForm(forms.ModelForm):
    profile_image = forms.ImageField(label='Image', required=True)

    class Meta:
        model = ProfileInfo
        fields = ['license_no']

    def __init__(self, *args, **kwargs):
        # Extract `user` from kwargs
        user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        
        if user:
            # Initialize `license_no` and `profile_image` with current values from ProfileInfo if they exist
            profile_info = ProfileInfo.objects.filter(user=user).first()
            if profile_info:
                self.fields['license_no'].initial = profile_info.license_no
                self.fields['profile_image'].initial  = profile_info.profile_image
             

    def save(self, commit=True):
        # Save license_no and profile_image to the ProfileInfo instance
        profile_info = super(ProfileForm, self).save(commit=False)
        
        if commit:
            profile_info.save()
        return profile_info


class PersonalDetailsForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label='First Name')
    last_name = forms.CharField(max_length=30, required=False, label='Last Name')
    email = forms.EmailField(required=True, label='Email')  # Added email field
 

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