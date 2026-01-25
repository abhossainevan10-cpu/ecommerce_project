# orders/views.py
from django.shortcuts import render, redirect, get_object_or_404
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
                price=item['price'],
                quantity=item['quantity']
            )

        cart.clear()

        return redirect('payment_started', order_id=order.id)

    return render(request, 'orders/checkout.html', {'cart': cart})


def payment_started(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/payment_started.html', {'order': order})


def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.paid = True
    order.save()

    return render(request, 'orders/payment_success.html', {'order': order})

