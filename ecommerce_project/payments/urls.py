from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'), 
    path('start/', views.start_payment, name='start_payment'),
    path('success/', views.payment_success, name='payment_success'),
    path('fail/', views.payment_fail, name='payment_fail'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
    path('download-receipt/<int:order_id>/', views.download_receipt, name='download_receipt'),
]