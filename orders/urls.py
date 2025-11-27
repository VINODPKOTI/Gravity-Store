from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    path('checkout/', views.checkout, name='checkout'),
    path('place_order/', views.place_order, name='place_order'),
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('payment/verify/', views.verify_payment, name='verify_payment'),
    path('success/', views.order_success, name='order_success'),
    path('failed/', views.order_failed, name='order_failed'),
    
    path('history/', views.order_history, name='order_history'),
    path('detail/<int:order_id>/', views.order_detail, name='order_detail'),
]
