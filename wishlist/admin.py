from django.contrib import admin
from .models import Wishlist, WishlistItem


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_id', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'session_id')


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('wishlist', 'product', 'sku', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('product__title',)
