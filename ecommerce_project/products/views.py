from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    # URL থেকে ?category=Samsung এর মান নেওয়া
    brand_name = request.GET.get('category')

    # সবার আগে সব প্রোডাক্ট নেওয়া
    products = Product.objects.all()

    # যদি ব্র্যান্ড থাকে → ফিল্টার করো
    if brand_name:
        products = products.filter(brand=brand_name)

    return render(request, 'products/product_list.html', {'products': products})


def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product_detail.html', {'product': product})


from django.shortcuts import render, get_object_or_404
from .models import Product








