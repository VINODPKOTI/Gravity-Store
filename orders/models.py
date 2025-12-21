from django.db import models
from django.conf import settings
from products.models import Product, SKU

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='cart')
    session_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id} ({self.user.username if self.user else 'Guest'})"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def total_items(self):
        return self.items.count()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sku = models.ForeignKey(SKU, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

    @property
    def unit_price(self):
        base = self.sku.price if self.sku.price > 0 else self.product.base_price
        
        # Re-calculate discount on the fly for the SKU price
        offer = self.product.get_active_offer()
        if offer:
            discount = (base * offer.discount_percent) / 100
            return base - discount
        return base

    @property
    def total_price(self):
        return self.unit_price * self.quantity

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PAID = 'PAID', 'Paid'
        FAILED = 'FAILED', 'Failed'
        CANCELLED = 'CANCELLED', 'Cancelled'
    
    class PaymentMethod(models.TextChoices):
        RAZORPAY = 'RAZORPAY', 'Razorpay'
        COD = 'COD', 'Cash on Delivery'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    shipping_address = models.TextField() # Snapshot of address
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.RAZORPAY)
    payment_id = models.CharField(max_length=100, blank=True, null=True) # Razorpay Order ID
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sku = models.ForeignKey(SKU, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2) # Price at time of purchase
    
    def __str__(self):
        return f"{self.quantity} x {self.product.title}"
