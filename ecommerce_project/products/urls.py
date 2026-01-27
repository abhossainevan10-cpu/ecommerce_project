
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('products/', views.product_list, name='product_list'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('api/', views.product_list_api, name='product_list_api'),
    path('api/<int:pk>/', views.product_detail_api, name='product_detail_api'),
]

