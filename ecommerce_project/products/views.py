from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from cart.cart import Cart  # এই লাইনটি যোগ করুন

# ১. সাধারণ ইউজারদের জন্য (HTML View)
def product_list(request):
    products = Product.objects.all()
    cart = Cart(request)  # কার্ট অবজেক্টটি তৈরি করুন
    # 'cart' কে ডিকশনারিতে পাস করুন যেন টেমপ্লেটে {{ cart|length }} কাজ করে
    return render(request, 'products/product_list.html', {
        'products': products, 
        'cart': cart
    })

# ২. অ্যাডমিন বা ডেটার জন্য (API View)
@api_view(['GET'])
def product_list_api(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

def product_detail(request, id):
    # আইডি অনুযায়ী প্রোডাক্ট খুঁজে বের করা, না পেলে ৪-০-৪ এরর দিবে
    product = get_object_or_404(Product, id=id)
    return render(request, 'products/product_detail.html', {'product': product})