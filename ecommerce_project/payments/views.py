from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from uuid import uuid4
from .sslcommerz import SSLCommerz
from cart.cart import Cart
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order, OrderItem
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
import io


# --- ১. PDF জেনারেট করার ফাংশন ---
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

# --- ২. PDF ডাউনলোড ভিউ ---
def download_receipt(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    data = {'order': order}
    pdf = render_to_pdf('emails/payment_card.html', data)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"Receipt_Order_{order.id}.pdf"
        content = f"attachment; filename={filename}"
        response['Content-Disposition'] = content
        return response
    return HttpResponse("PDF Not Found")

# --- ৩. পেমেন্ট সফল হওয়ার ভিউ ---
@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        tran_id = request.POST.get('tran_id')
        try:
            order = Order.objects.get(transaction_id=tran_id)
            order.paid = True
            order.save()

            # অ্যাডমিন অ্যালার্ট ইমেল
            admin_email = 'abhossainevan10@gmail.com' 
            admin_message = f"""
New Order Received!
Order ID: #{order.id}
Transaction ID: {order.transaction_id}
Customer: {order.full_name}
Phone: {order.phone_number}
Address: {order.address}, {order.city}
Total: Tk {order.total_amount}
            """
            
            send_mail(
                subject=f"New Paid Order - #{order.id}", 
                message=admin_message, 
                from_email=settings.EMAIL_HOST_USER, 
                recipient_list=[admin_email],
                fail_silently=False
            )

            cart = Cart(request)
            cart.clear()
            
            return render(request, 'payments/payment_success.html', {'order': order})
            
        except Order.DoesNotExist:
            return HttpResponse("Order Not Found")
    return redirect('home')

# --- ৪. পেমেন্ট শুরু করার ভিউ (ফিক্সড কোড) ---
def start_payment(request):
    if request.method == 'POST':
        cart = Cart(request)
        total_amount = cart.get_total_price()
        tran_id = str(uuid4())[:10]
        
        # ফরম থেকে কাস্টমারের তথ্য সংগ্রহ (IntegrityError ফিক্স করার জন্য)
        fname = request.POST.get('first_name', '')
        lname = request.POST.get('last_name', '')
        full_name = f"{fname} {lname}".strip() or "Guest Customer"
        
        email = request.POST.get('email', '')
        phone = request.POST.get('phone_number', '') # HTML name="phone_number" এর সাথে মিল
        address = request.POST.get('address', '')     # এটিই মূল সমস্যা ছিল
        city = request.POST.get('city', '')           # এটিও যোগ করা হলো
        
        # ডাটাবেসে সব তথ্যসহ অর্ডার তৈরি করা
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            email=email,
            phone_number=phone,
            address=address,  # এখন আর NOT NULL এরর আসবে না
            city=city,
            transaction_id=tran_id,
            total_amount=total_amount,
            paid=False
        )

        # আইটেমগুলো সেভ করা
        for item in cart:
            OrderItem.objects.create(
                order=order, 
                product=item['product'], 
                price=item['price'], 
                quantity=item['quantity']
            )
        
        # SSLCommerz গেটওয়ে শুরু
        ssl = SSLCommerz()
        response = ssl.initiate(
            total_amount=str(total_amount),
            tran_id=tran_id,
            success_url=request.build_absolute_uri('/payments/success/'),
            fail_url=request.build_absolute_uri('/payments/fail/'),
            cancel_url=request.build_absolute_uri('/payments/cancel/'),
            cus_name=full_name,
            cus_email=email,
            cus_phone=phone,
            cus_add1=address, 
            cus_city=city, 
            cus_country='Bangladesh',
            product_category='Gadgets', 
            product_name='Order Items', 
            shipping_method='NO', 
            num_of_item=len(cart), 
            product_profile='general'
        )

        if response.get('status') == 'SUCCESS': 
            return redirect(response['GatewayPageURL'])
        else:
            return HttpResponse(f"Gateway Error: {response.get('failedreason')}")
            
    return redirect('checkout')

# --- ৫. বাকি সাপোর্ট ভিউসমূহ ---
def checkout(request):
    cart = Cart(request)
    return render(request, 'payments/checkout.html', {'cart': cart})

@csrf_exempt
def payment_fail(request):
    return render(request, 'payments/payment_fail.html')

@csrf_exempt
def payment_cancel(request):
    return render(request, 'payments/payment_cancel.html')


