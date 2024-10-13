# forms.py
from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    # Adding fields for first name and last name
    first_name = forms.CharField(max_length=30, required=False, label='First Name')
    last_name = forms.CharField(max_length=30, required=False, label='Last Name')
    profile_image = forms.ImageField(label='Image', required=True)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number', 'birth_date']  

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
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

