import os
import django
import sys

# Force UTF-8 encoding for stdout
sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aaramba_project.settings')
django.setup()

from core.models import Banner

print("Checking Banners...")
banners = Banner.objects.all()
for b in banners:
    print(f"ID: {b.id}, Title: {b.title}, Subtitle: '{b.subtitle}', Active: {b.is_active}")
