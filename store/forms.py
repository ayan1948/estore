from django import forms
from .models import ShippingAddress


class CheckoutForm(forms.ModelForm):
    save_info = forms.BooleanField(label='Save Address', widget=forms.CheckboxInput(attrs={'class': 'creat_account'}), required=False)

    class Meta:
        model = ShippingAddress
        fields = ['street_address', 'city', 'zip', 'save_info']
        labels = {
            'street_address': 'Street Address',
            'city': ''
        }
        widgets = {
            'street_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'zip': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Pin Code'})
        }
