from django import forms
from .models import Product, SKU

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'title', 'description', 'base_price', 'image', 'is_active')
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'base_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class SKUForm(forms.ModelForm):
    class Meta:
        model = SKU
        fields = ('sku_code', 'price', 'stock', 'attributes')
        widgets = {
            'sku_code': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'attributes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': '{"color": "Red", "size": "M"}'}),
        }
