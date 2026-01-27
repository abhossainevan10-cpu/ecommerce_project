from django.shortcuts import render, redirect
from django.http import HttpResponse
from uuid import uuid4
from .sslcommerz import SSLCommerz
from cart.cart import Cart
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order, OrderItem
from django.core.mail import send_mail
from django.conf import settings

def checkout(request):
    cart = Cart(request)
    return render(request, 'payments/checkout.html', {'cart': cart})

def start_payment(request):
    if request.method == 'POST':
        cart = Cart(request)
        total_amount = cart.get_total_price()
        
        if total_amount <= 0:
            return HttpResponse("আপনার কার্ট খালি!")

        # ১. ইউনিক ট্রানজেকশন আইডি তৈরি
        tran_id = str(uuid4())[:10]
        
        # ২. ডাটাবেসে অর্ডার অবজেক্ট তৈরি করা
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            transaction_id=tran_id,
            total_amount=total_amount,
            paid=False
        )

        # ৩. কার্টের আইটেমগুলো OrderItem মডেলে সেভ করা
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )
        
        # SSLCommerz এর জন্য কাস্টমার ডাটা
        customer_name = f"{request.POST.get('first_name', '')} {request.POST.get('last_name', '')}"
        
        ssl = SSLCommerz()
        response = ssl.initiate(
            total_amount=str(total_amount),
            tran_id=tran_id,
            success_url=request.build_absolute_uri('/payments/success/'),
            fail_url=request.build_absolute_uri('/payments/fail/'),
            cancel_url=request.build_absolute_uri('/payments/cancel/'),
            cus_name=customer_name,
            cus_email=request.POST.get('email', 'test@test.com'),
            cus_phone=request.POST.get('phone', '01700000000'),
            cus_add1=request.POST.get('address', 'Dhaka'),
            cus_city=request.POST.get('city', 'Dhaka'),
            cus_country='Bangladesh',
            product_category='Ecommerce Items',
            product_name='Order Products',
            shipping_method='NO',
            num_of_item=len(cart),
            product_profile='general'
        )
        
        if response.get('status') == 'SUCCESS' and response.get('GatewayPageURL'):
            return redirect(response['GatewayPageURL'])
        else:
            return HttpResponse(f"পেমেন্ট গেটওয়েতে সমস্যা: {response.get('failedreason')}")
    
    return redirect('checkout')

@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        tran_id = request.POST.get('tran_id')
        
        try:
            
            order = Order.objects.get(transaction_id=tran_id)
            order.paid = True
            order.save()

            
            subject = f"New Order Alert - #{order.id}"
            message = f"""
            New Order Received!
            Order ID: #{order.id}
            Transaction ID: {order.transaction_id}
            User: {order.user.username if order.user else 'Guest'}
            Total: Tk {order.total_amount}
            Payment Method: SSLCOMMERZ
            """
            
            admin_email = 'abhossainevan10@gmail.com' 
            
           
            send_mail(
                subject, 
                message, 
                settings.EMAIL_HOST_USER, 
                [admin_email], 
                fail_silently=False
            )

           
            cart = Cart(request)
            cart.clear()

            return render(request, 'payments/payment_success.html', {'order': order})
            
        except Order.DoesNotExist:
            return HttpResponse("Order Not Found")
            
    return redirect('home')

@csrf_exempt
def payment_fail(request):
    return render(request, 'payments/payment_fail.html')

@csrf_exempt
def payment_cancel(request):
    return render(request, 'payments/payment_cancel.html')