from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .forms import TicketForm
from .models import Ticket
import stripe
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

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
            ticket.seller = request.user  
            ticket.save()
            return redirect('ticket_list') 
    else:
        form = TicketForm()
    return render(request, 'create_ticket.html', {'form': form})

# Ticket List Page (View available tickets)
def ticket_list(request):
    tickets = Ticket.objects.filter(is_sold=False)  # Show only unsold tickets
    return render(request, 'ticket_list.html', {'tickets': tickets})

# Edit Ticket Page
def edit_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk, seller=request.user) 
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('ticket_list')  
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'edit_ticket.html', {'form': form})

# Delete Ticket Page
def delete_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk, seller=request.user) 
    if request.method == 'POST':
        ticket.delete()  
        return redirect('ticket_list')  
    return render(request, 'delete_ticket.html', {'ticket': ticket})

# Create Stripe Checkout Session
def create_checkout_session(request):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Event Ticket',  
                    },
                    'unit_amount': 2000,  
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://8000-davidkilty-project5-of8fv53e6w4.ws.codeinstitute-ide.net/success/', 
            cancel_url='http://8000-davidkilty-project5-of8fv53e6w4.ws.codeinstitute-ide.net/cancel/',  
        )
        return JsonResponse({'sessionId': session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Stripe Webhook to handle payment success or failure
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)  
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)  

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        ticket_id = session.get('client_reference_id')  

        if ticket_id:
            try:
                ticket = Ticket.objects.get(id=ticket_id)
                ticket.is_sold = True
                ticket.save()
            except Ticket.DoesNotExist:
                pass  

    return HttpResponse(status=200)

