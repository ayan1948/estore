from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re-enter Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

    # Validating password
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password2'] != cd['password']:
            raise ValidationError("Password don't match")

        return cd['password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'single-input'}),
            'last_name': forms.TextInput(attrs={'class': 'single-input'}),
            'username': forms.TextInput(attrs={'class': 'single-input'}),
            'email': forms.EmailInput(attrs={'class': 'single-input'})
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone']
        widgets = {
            'phone': forms.NumberInput(attrs={'class': 'single-input'})
        }
