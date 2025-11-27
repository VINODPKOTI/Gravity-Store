from django.db import models
from products.models import Category
from django.utils import timezone

class Offer(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2) # e.g., 5.00 for 5%
    categories = models.ManyToManyField(Category, related_name='offers')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.discount_percent}%)"

    @property
    def is_valid(self):
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date
