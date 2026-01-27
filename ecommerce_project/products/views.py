from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Slider, Category
from .serializers import ProductSerializer
from cart.cart import Cart

# --- ১. সাধারণ ইউজারদের জন্য (HTML View) ---

def home(request):
    """সার্চ রেজাল্ট, ক্যাটাগরি এবং স্লাইডার ডাটা হ্যান্ডেল করে"""
    query = request.GET.get('search')
    category_slug = request.GET.get('category')
    
    # প্রাথমিক কুয়েরিসেট
    products = Product.objects.all().order_by('-id')

    # ১. সার্চ ফিল্টার
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(brand__icontains=query)
        ).distinct()
    
    # ২. ক্যাটাগরি ফিল্টার
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # ৩. স্লাইডার ডাটা
    main_slider = Slider.objects.filter(title__icontains="MacBook").first()
    side_1 = Slider.objects.filter(title__icontains="Watch").first()
    side_2 = Slider.objects.filter(title__icontains="airpords").first() 

    context = {
        'products': products[:12],
        'categories': Category.objects.all(),
        'main_slider': main_slider,
        'side_1': side_1,
        'side_2': side_2,
        'query': query,
    }
    # ফিক্স: যদি home.html ফাইলটি core অ্যাপের ভেতর থাকে, তবে 'core/home.html' লিখুন
    return render(request, 'core/home.html', context)

def product_list(request):
    """সব প্রোডাক্টের লিস্ট ভিউ"""
    products = Product.objects.all().order_by('-id')
    return render(request, 'products/product_list.html', {
        'products': products, 
    })

def product_detail(request, id):
    """প্রোডাক্টের ডিটেইল পেজ"""
    product = get_object_or_404(Product, id=id)
    return render(request, 'products/product_detail.html', {'product': product})


# --- ২. API CRUD ভিউ (REST API) ---

@api_view(['GET', 'POST'])
def product_list_api(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response({'message': 'Product deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)