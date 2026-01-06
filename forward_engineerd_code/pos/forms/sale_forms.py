"""
Sale Forms
"""

from django import forms
from pos.models import Item


class SaleItemForm(forms.Form):
    """Form for adding items to sale"""
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


class CouponForm(forms.Form):
    """Form for applying coupon"""
    coupon_code = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Coupon Code',
            'required': False
        })
    )

