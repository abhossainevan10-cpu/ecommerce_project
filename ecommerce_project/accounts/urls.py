from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'), # নিশ্চিত করুন views.py এ এই ফাংশনটি আছে
    path('logout/', views.logout_view, name='logout'),
]