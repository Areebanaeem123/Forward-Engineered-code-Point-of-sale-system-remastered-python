"""
Rental Forms
"""

from django import forms


class RentalForm(forms.Form):
    """Form for creating rental"""
    phone_number = forms.CharField(
        max_length=20,
        label='Customer Phone Number',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number',
            'required': True
        })
    )
    item_id = forms.IntegerField(
        label='Item ID',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Item ID',
            'required': True
        })
    )
    quantity = forms.IntegerField(
        label='Quantity',
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Quantity',
            'required': True,
            'min': 1
        })
    )


class ReturnForm(forms.Form):
    """Form for processing returns"""
    phone_number = forms.CharField(
        max_length=20,
        label='Customer Phone Number',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number',
            'required': True
        })
    )
    rental_id = forms.IntegerField(
        label='Rental ID',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Rental ID',
            'required': True
        })
    )

