import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aaramba_project.settings')
django.setup()

from core.models import Banner

banners = Banner.objects.filter(is_active=True)
print(f"Found {banners.count()} active banners.")
for b in banners:
    print(f"Title: '{b.title}', Subtitle: '{b.subtitle}'")
