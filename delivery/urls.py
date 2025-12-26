from django.urls import path
from . import views

app_name = 'delivery'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('shipments/', views.shipment_list, name='shipment_list'),
     path("history/", views.shipment_history, name="shipment_history"),
    path('shipment/<int:pk>/', views.shipment_detail, name='shipment_detail'),
]
