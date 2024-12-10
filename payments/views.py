import logging
import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from django.contrib.sitemaps import Sitemap

import stripe
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from .models import Ticket, FAQ
from .forms import TicketForm, ContactForm, NewsletterSignupForm

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = '2024-06-20'


def success_page(request):
    return render(request, 'success.html', {'message_type': 'payment'})


def success_contact(request):
    return render(request, 'success.html', {'message_type': 'contact'})



def home(request):
    return render(request, 'home.html')


def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.seller = request.user
            if ticket.event_date >= timezone.now():
                ticket.save()
                return redirect('ticket_list')
            form.add_error('event_date', 'Event date cannot be in the past.')
    else:
        form = TicketForm()
    return render(request, 'create_ticket.html', {'form': form})


@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(is_available=True)
    return render(request, 'ticket_list.html', {
        'tickets': tickets,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY
    })



@login_required
def edit_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.user != ticket.seller:
        return redirect('ticket_list')
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            ticket.check_availability()
            return redirect('ticket_list')
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'edit_ticket.html', {'form': form})


@login_required
def delete_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.user != ticket.seller:
        return redirect('ticket_list')
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


@login_required
def create_checkout_session(request):
    ticket_id = request.GET.get('ticket_id')
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if ticket.seller == request.user:
        return redirect('ticket_list')

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'eur',
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

    ticket.is_available = False
    ticket.save()

    return JsonResponse({'id': session.id})


def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        if session['payment_status'] == 'paid':  
            ticket_id = session.get('client_reference_id')
            if ticket_id:
                ticket = Ticket.objects.get(id=ticket_id)
                ticket.delete()
        else:
            logging.warning(f"Payment failed for session: {session['id']}")

    return HttpResponse(status=200)


def faq_list(request):
    faqs = FAQ.objects.all()
    return render(request, 'faq_list.html', {'faqs': faqs})


def cancel_page(request):
    return render(request, 'cancel.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = form.cleaned_data['email']
            send_mail(subject, message, from_email, [settings.DEFAULT_FROM_EMAIL])
            return redirect('success_contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


class TicketSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Ticket.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /admin/",
        "Allow: /",
        "Sitemap: https://nightspot-d83df74ddcea.herokuapp.com/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    return render(request, 'ticket_detail.html', {'ticket': ticket})


def newsletter_signup(request):
    if request.method == 'POST':
        form = NewsletterSignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key['api-key'] = settings.BREVO_API_KEY

            api_instance = sib_api_v3_sdk.ContactsApi(sib_api_v3_sdk.ApiClient(configuration))
            contact = sib_api_v3_sdk.CreateContact(email=email)

            try:
                api_instance.create_contact(contact)
                messages.success(request, "You've successfully subscribed to the newsletter.")
            except ApiException:
                messages.error(request, "An error occurred while trying to subscribe.")

            return redirect('newsletter_signup')
    else:
        form = NewsletterSignupForm()
    return render(request, 'newsletter_signup.html', {'form': form})
