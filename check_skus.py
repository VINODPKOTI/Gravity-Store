import os
import django
import sys

# Force UTF-8 encoding for stdout
sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aaramba_project.settings')
django.setup()

from products.models import Product, SKU

try:
    product = Product.objects.get(pk=3)
    print(f"Product: {product.title} (ID: {product.id})")
    skus = SKU.objects.filter(product=product)
    print(f"Found {skus.count()} SKUs:")
    for sku in skus:
        print(f"  - SKU: {sku.sku_code}, Stock: {sku.stock}, ID: {sku.id}")
except Product.DoesNotExist:
    print("Product 3 does not exist.")
