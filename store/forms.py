from django import forms
from .models import ShippingAddress


class CheckoutForm(forms.ModelForm):
    # save_info = forms.BooleanField(label='Save Address', widget=forms.CheckboxInput(attrs={'class': 'creat_account'}), required=False)

    class Meta:
        model = ShippingAddress
        fields = ['street_address', 'city', 'zip']
        labels = {
            'street_address': 'Street Address',
            'city': 'City'
        }
        widgets = {
            'street_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '221, Baker Street'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'London'}),
            'zip': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '530124'})
        }
