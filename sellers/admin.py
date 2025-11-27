from django.contrib import admin
from .models import Seller

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'commission_rate', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('business_name', 'user__username')
    actions = ['approve_sellers']

    def approve_sellers(self, request, queryset):
        queryset.update(is_approved=True)
    approve_sellers.short_description = "Approve selected sellers"
