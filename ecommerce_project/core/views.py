from django.shortcuts import render
from products.models import Product, Category, Slider 




def home(request):
    query = request.GET.get('search')
    if query:
        products = Product.objects.filter(name__icontains=query) 
    else:
        products = Product.objects.all().order_by('-id')[:8]

def home(request):
    products = Product.objects.all().order_by('-id')[:8] 
    categories = Category.objects.all()
    
    sliders = Slider.objects.all()
    main_slider = sliders[0] if sliders.count() > 0 else None
    side_1 = sliders[1] if sliders.count() > 1 else None
    side_2 = sliders[2] if sliders.count() > 2 else None
    
    context = {
        'products': products,
        'categories': categories,
        'main_slider': main_slider,
        'side_1': side_1,
        'side_2': side_2,
    }
    return render(request, 'core/home.html', context)