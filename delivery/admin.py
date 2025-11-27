from django.contrib import admin
from .models import Shipment

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'seller', 'tracking_number', 'status', 'updated_at')
    list_filter = ('status', 'updated_at')
    search_fields = ('tracking_number', 'order__id')
    readonly_fields = ('updated_at',)
