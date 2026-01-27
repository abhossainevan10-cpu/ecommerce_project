# orders/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('', views.checkout, name='orders_home'), 
    path('checkout/', views.checkout, name='checkout'),
    path('payment/<int:order_id>/', views.payment_started, name='payment_started'),
    path('payment-success/<int:order_id>/', views.payment_success, name='payment_success'),
]
