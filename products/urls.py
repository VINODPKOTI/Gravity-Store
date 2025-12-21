from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('suggestions/', views.product_search_suggestions, name='product_search_suggestions'),
    path('sku-attributes/<int:sku_id>/', views.get_sku_attributes, name='sku_attributes'),
]
