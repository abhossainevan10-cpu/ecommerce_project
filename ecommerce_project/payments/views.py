from django.shortcuts import render, redirect
from uuid import uuid4

from .sslcommerz import SSLCommerz


def start_payment(request):
    """
    Start SSLCommerz payment
    """
    # 1️⃣ Unique transaction ID
    tran_id = str(uuid4())

    # 2️⃣ SSLCommerz object
    ssl = SSLCommerz()

    # 3️⃣ Create payment session
    response = ssl.initiate(
        amount='1.00',
        tran_id=tran_id,
        success_url=request.build_absolute_uri('/payments/success/'),
        fail_url=request.build_absolute_uri('/payments/fail/'),
        cancel_url=request.build_absolute_uri('/payments/cancel/')
    )

    # 4️⃣ Redirect to gateway (recommended)
    if response.get('GatewayPageURL'):
        return redirect(response['GatewayPageURL'])

    # 5️⃣ Fallback (if gateway url missing)
    return render(
        request,
        'payments/payment_started.html',
        {'response': response}
    )


def payment_success(request):
    """
    Payment success page
    """
    return render(request, 'payments/payment_success.html')


def payment_fail(request):
    """
    Payment failed page
    """
    return render(request, 'payments/payment_fail.html')


def payment_cancel(request):
    """
    Payment cancelled page
    """
    return render(request, 'payments/payment_cancel.html')
