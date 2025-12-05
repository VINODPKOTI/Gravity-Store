from django.db import models
from products.models import Product, SKU


class Wishlist(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='wishlist', null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wishlist ({self.user.username if self.user else 'Guest'})"


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sku = models.ForeignKey(SKU, on_delete=models.CASCADE, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('wishlist', 'product', 'sku')

    def __str__(self):
        return f"{self.product.title} in Wishlist"
