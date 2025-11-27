from django.db import models
from django.conf import settings

class Seller(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller_profile')
    business_name = models.CharField(max_length=255)
    business_address = models.TextField()
    tax_id = models.CharField(max_length=50, blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.00) # Percentage
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name
