from django.contrib import admin
from .models import Category, Product, SKU

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'base_price', 'category', 'created_at')
    list_filter = ('category', 'seller', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)

@admin.register(SKU)
class SKUAdmin(admin.ModelAdmin):
    list_display = ('sku_code', 'product', 'price', 'stock')
    list_filter = ('product',)
    search_fields = ('sku_code',)
