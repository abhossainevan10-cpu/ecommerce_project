
from django.urls import path
from . import views

urlpatterns = [
    # এটি হবে http://127.0.0.1:8000/products/
    path('', views.product_list, name='product_list'), 
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    
    # এটি হবে http://127.0.0.1:8000/products/api/
    path('api/', views.product_list_api, name='product_list_api'),
]