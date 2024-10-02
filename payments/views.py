from django.shortcuts import render, redirect
from django.conf import settings
from .forms import TicketForm
from .models import Ticket
import stripe
from django.http import JsonResponse

# Set Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

# Payment Page
def payment_page(request):
    return render(request, 'payment.html', {
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,  # Pass Stripe key
    })

# Create Ticket Page
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.seller = request.user  # Assign the current logged-in user as the seller
            ticket.save()
            return redirect('ticket_list')  # Redirect to ticket list after creation
    else:
        form = TicketForm()
    return render(request, 'create_ticket.html', {'form': form})

# Ticket List Page (View available tickets)
def ticket_list(request):
    tickets = Ticket.objects.filter(is_sold=False)  # Show only unsold tickets
    return render(request, 'ticket_list.html', {'tickets': tickets})

# Create Stripe Checkout Session
def create_checkout_session(request):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Event Ticket',  # You can customize this based on the ticket
                    },
                    'unit_amount': 2000,  # Amount in cents (i.e., $20)
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:8000/success/',  # Replace with your success URL
            cancel_url='http://localhost:8000/cancel/',  # Replace with your cancel URL
        )
        return JsonResponse({'sessionId': session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
