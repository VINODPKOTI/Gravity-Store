from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('seller/', include('sellers.urls')),
    path('delivery/', include('delivery.urls')),
    path('payments/', include('payments.urls')),
    # Promotions urls can be part of products or separate, keeping separate for now
    path('promotions/', include('promotions.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
