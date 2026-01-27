from django.shortcuts import redirect, render, get_object_or_404
from .cart import Cart
from products.models import Product

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product) 
    return redirect('cart_detail')


def cart_remove(request, product_id):
    """কার্ট থেকে নির্দিষ্ট প্রোডাক্ট মুছে ফেলার ভিউ"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    
    cart.remove(product)
    
    return redirect('cart_detail')

def cart_detail(request):
    """কার্টে থাকা সব প্রোডাক্ট দেখানোর ভিউ"""
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

def cart_update(request, product_id):
    """প্রয়োজন হলে প্রোডাক্টের পরিমাণ কমানো বা বাড়ানোর জন্য এটি ব্যবহার করতে পারেন"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    return redirect('cart_detail')


