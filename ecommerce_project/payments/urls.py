from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_payment, name='start_payment'),
    path('success/', views.payment_success, name='payment_success'),

]