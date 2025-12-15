from django.shortcuts import render
from products.models import Product

def home(request):
    products = Product.objects.all()[:8]
    return render(request, 'core/home.html', {'products': products})
