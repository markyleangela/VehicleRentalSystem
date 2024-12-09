from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from user_profile.models import UserProfile, ProfileInfo

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("The username you have entered is already taken. Please choose a different one.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
            UserProfile.objects.create(user=user)
            ProfileInfo.objects.create(user=user)

        return user
