from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'program',
            'name',
            'box_quantity',
            'pallet_box_quantity',  # ✅ 추가
            'product_barcode',
            'box_barcode',
            'image',
            'is_active',
        ]
        widgets = {
            'program': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'box_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'pallet_box_quantity': forms.NumberInput(attrs={'class': 'form-control'}),  # ✅ 추가
            'product_barcode': forms.TextInput(attrs={'class': 'form-control'}),
            'box_barcode': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(),
        }
