from django.contrib import admin
from .models import Category, Product, SKU
from mptt.admin import DraggableMPTTAdmin


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'is_active')
    list_display_links = ('indented_title',)
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'category', 'base_price', 'is_active', 'created_at')
    list_filter = ('is_active', 'category', 'seller')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)

@admin.register(SKU)
class SKUAdmin(admin.ModelAdmin):
    list_display = ('sku_code', 'product', 'price', 'stock')
    list_filter = ('product',)
    search_fields = ('sku_code',)
