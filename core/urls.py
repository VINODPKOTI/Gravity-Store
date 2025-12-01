from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('control/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('terms-of-service/', views.terms, name='terms'),
    path('privacy-policy/', views.privacy, name='privacy'),
    path('contact-us/', views.contact, name='contact'),
]
