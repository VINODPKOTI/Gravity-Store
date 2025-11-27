from django.urls import path
from . import views

app_name = 'delivery'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('shipment/<int:pk>/', views.shipment_detail, name='shipment_detail'),
]
