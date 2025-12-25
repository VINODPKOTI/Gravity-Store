from django.urls import path
from . import views

app_name = 'sellers'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),  
    path('orders/', views.seller_orders, name='seller_orders'),
    path('orders/<int:order_id>/', views.seller_order_detail, name='seller_order_detail'),

]
