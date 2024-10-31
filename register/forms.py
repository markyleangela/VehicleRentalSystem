# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from user_profile.models import UserProfile

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)  
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    phone_number = forms.CharField(max_length=25, required=True)
    license_number = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        # fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'birth_date']
        fields = ['username',  'email','password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'] 

        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                # first_name=self.cleaned_data['first_name'],
                # last_name=self.cleaned_data['last_name'],
                # birth_date=self.cleaned_data['birth_date'],
                # phone_number=self.cleaned_data['phone_number'],
                # license_number=self.cleaned_data['license_number'],
            )
        return user
