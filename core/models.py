from django.db import models
from products.models import Product

class Banner(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='banners/')
    link = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='banners')
    category = models.ForeignKey('products.Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='banners')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Create your models here.
