from django import forms
from .models import ShippingAddress


class CheckoutForm(forms.Form):
    save_info = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = ShippingAddress
        fields = ['street_address', 'city', 'zip']
        widgets = {
            'street_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'zip': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Pin Code'})
        }
