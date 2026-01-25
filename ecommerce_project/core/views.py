from django.shortcuts import render
from products.models import Product

def home(request):
    # ডাটাবেস থেকে প্রথম ৮টি প্রোডাক্ট আনা হচ্ছে
    products = Product.objects.all()[:8]
    return render(request, 'core/home.html', {'products': products})