from django.urls import path
from . import views

app_name = 'promotions'

urlpatterns = [
    path('offers/', views.offer_list, name='offer_list'),
    path('offers/add/', views.offer_add, name='offer_add'),
    path('offers/<int:pk>/edit/', views.offer_edit, name='offer_edit'),
]
