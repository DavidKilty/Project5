from django.shortcuts import render
from django.conf import settings

def payment_page(request):
    return render(request, 'payments/payment.html', {
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,  # Pass Stripe key
    })
