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


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default='Aaramba')
    logo = models.ImageField(upload_to='site/', blank=True, null=True, help_text="Upload your site logo")
    favicon = models.ImageField(upload_to='site/', blank=True, null=True, help_text="Upload your favicon (ico or png)")
    loader_image = models.ImageField(upload_to='site/', blank=True, null=True, help_text="Upload your page loader image")

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name_plural = "Site Settings"
