from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='orders'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment-started/', views.payment_started, name='payment_started'),
    path('payment-success/', views.payment_success, name='payment_success'),
]


