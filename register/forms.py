from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    # Customizing fields to remove help_text and adjust labels
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        # Customize the username field
        self.fields['username'].label = 'Username'
        self.fields['username'].help_text = ''  # Remove default help text
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Enter Username'
        })

        # Customize the password1 field
        self.fields['password1'].label = 'Password'
        self.fields['password1'].help_text = ''  # Remove default help text
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Enter Password'
        })

        # Customize the password2 field
        self.fields['password2'].label = 'Confirm Password'
        self.fields['password2'].help_text = ''  # Remove default help text
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm Password'
        })
