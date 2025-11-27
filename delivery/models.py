from django.db import models
from orders.models import Order
from sellers.models import Seller

class Shipment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        READY_TO_SHIP = 'READY', 'Ready to Ship'
        SHIPPED = 'SHIPPED', 'Shipped'
        DELIVERED = 'DELIVERED', 'Delivered'
        RETURNED = 'RETURNED', 'Returned'

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='shipments')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='shipments')
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Shipment #{self.id} for Order #{self.order.id}"
