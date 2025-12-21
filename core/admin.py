from django.contrib import admin
from .models import Banner, SiteSettings

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle')

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Only allow creating one instance
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
