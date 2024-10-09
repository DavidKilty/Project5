from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Ticket
from .forms import TicketForm
import stripe
from django.contrib.auth.decorators import login_required
from django.utils import timezone

stripe.api_key = 'your_stripe_secret_key' 


def check_ticket_availability():
    return True
    
def payment(request):
    ticket_is_available = check_ticket_availability()
    return render(request, 'payment.html', {'ticket_is_available': ticket_is_available})

def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.seller = request.user  
            if ticket.event_date >= timezone.now().date():  # Check date is in the future
                ticket.save()
                return redirect('ticket_list')
            else:
                form.add_error('event_date', 'Event date cannot be in the past.')
    else:
        form = TicketForm()
    return render(request, 'create_ticket.html', {'form': form})

@login_required
def ticket_list(request):
    tickets = Ticket.objects.all()
    return render(request, 'ticket_list.html', {'tickets': tickets})

@login_required
def edit_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.user != ticket.seller:
        return redirect('ticket_list')  # Seller can edit their own ticket
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('ticket_list')
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'edit_ticket.html', {'form': form})

@login_required
def delete_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.user != ticket.seller:
        return redirect('ticket_list')  # Seller can delete their own ticket
    if request.method == 'POST':
        ticket.delete()
        return redirect('ticket_list')
    return render(request, 'delete_ticket.html', {'ticket': ticket})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'signup.html', {'form': form})

def stripe_webhook(request):
    pass  

@login_required
def create_checkout_session(request):
    ticket_id = request.GET.get('ticket_id')
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if ticket.seller == request.user:
        return redirect('ticket_list')  # Prevent from buying their own ticket

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': ticket.event_name,
                    'description': f"Ticket type: {ticket.ticket_type}",
                },
                'unit_amount': int(ticket.ticket_price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/success/'),
        cancel_url=request.build_absolute_uri('/cancel/'),
    )

    return JsonResponse({'id': session.id})
