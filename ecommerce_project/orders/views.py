from django.shortcuts import render, redirect
from .models import Order, OrderItem
from cart.cart import Cart

def checkout(request):
    cart = Cart(request)

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['product'].price,
                quantity=item['quantity']
            )

        # clear cart
        cart.clear()

        return redirect('payment_started')

    return render(request, 'orders/checkout.html', {'cart': cart})


def payment_started(request):
    return render(request, 'orders/payment_started.html')


def payment_success(request):
    return render(request, 'orders/payment_success.html')

