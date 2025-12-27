from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from sellers.models import Seller
import json

class Category(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products')
    category = TreeForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    title = models.CharField(max_length=255)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_active_offer(self):
        from django.utils import timezone
        from promotions.models import Offer
        now = timezone.now()
        # Get offers for this product's category or its ancestors
        if self.category:
            categories = self.category.get_ancestors(include_self=True)
            return Offer.objects.filter(categories__in=categories, is_active=True, start_date__lte=now, end_date__gte=now).order_by('-discount_percent').first()
        return None

    @property
    def discounted_price(self):
        offer = self.get_active_offer()
        if offer:
            discount = (self.base_price * offer.discount_percent) / 100
            return self.base_price - discount
        return self.base_price

    @property
    def is_in_stock(self):
        return self.skus.filter(stock__gt=0).exists()

class SKU(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='skus')
    sku_code = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    attributes = models.JSONField(default=dict) # e.g., {'color': 'Red', 'size': 'M'}
    
    def __str__(self):
        return f"{self.product.title} ({self.sku_code})"
