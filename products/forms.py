from django import forms
from .models import Product, SKU

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'category',
            'title',
            'description',
            'base_price',
            'image',
            'is_active',
        )
        widgets = {
            'category': forms.Select(attrs={
                'class': 'w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black',
                'rows': 3
            }),
            'base_price': forms.NumberInput(attrs={
                'class': 'w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full rounded-md border border-gray-300 px-3 py-2 text-sm'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 rounded border-gray-300 text-black focus:ring-black'
            }),
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
