"""
Item Forms
"""

from django import forms
from pos.models import Item


class ItemForm(forms.ModelForm):
    """Form for creating/editing items"""
    class Meta:
        model = Item
        fields = ['item_id', 'name', 'price', 'stock_sale', 'stock_rental', 'item_type']
        widgets = {
            'item_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock_sale': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'stock_rental': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'item_type': forms.Select(attrs={'class': 'form-control'}),
        }

