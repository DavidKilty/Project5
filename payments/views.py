from django.shortcuts import render, redirect
from django.conf import settings
from .forms import TicketForm
from .models import Ticket

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
