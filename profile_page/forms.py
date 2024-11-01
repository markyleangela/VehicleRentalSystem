from django import forms
from django.contrib.auth.models import User
from user_profile.models import ProfileInfo
from django.contrib.auth.forms import PasswordChangeForm

class ProfileForm(forms.ModelForm):
    class Meta:
        model = ProfileInfo
        fields = ['license_no']  # Keep only the license_no field

    def __init__(self, *args, **kwargs):
        # Extract `user` from kwargs
        user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        
        if user:
            # Initialize `license_no` with current value from ProfileInfo if it exists
            profile_info = ProfileInfo.objects.filter(user=user).first()
            if profile_info:
                self.fields['license_no'].initial = profile_info.license_no
             
    def save(self, commit=True):
        # Save license_no to the ProfileInfo instance
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
