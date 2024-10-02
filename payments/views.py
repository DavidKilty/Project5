from django.shortcuts import render
from django.conf import settings

def payment_page(request):
    return render(request, 'payments/payment.html', {
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,  # Pass Stripe key
    })
from django.shortcuts import render, redirect
from .forms import TicketForm

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
    return render(request, 'payments/create_ticket.html', {'form': form})

from .models import Ticket

def ticket_list(request):
    tickets = Ticket.objects.filter(is_sold=False)  # Show only unsold tickets
    return render(request, 'payments/ticket_list.html', {'tickets': tickets})
