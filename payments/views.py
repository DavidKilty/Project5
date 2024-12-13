import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
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


def test_webhook(request):
    """
    Simulates a webhook event for testing purposes.
    """
    payload = {
        "id": "evt_test_webhook",
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "id": "cs_test_a1OeVS18CDjsE8vk4bKKBW6auChDjqN6ZRIO2FCDtCjoshAaFpBr442p2M",
                "client_reference_id": "8",
                "payment_status": "paid"
            }
        }
    }

    from django.test import RequestFactory
    factory = RequestFactory()
    test_request = factory.post('/webhook/', payload, content_type='application/json')
    test_request.META['HTTP_STRIPE_SIGNATURE'] = 'test_signature'

    response = stripe_webhook(test_request)
    return JsonResponse({"response": response.status_code})


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
            user = form.save()
            subject = "Welcome to Night Spot!"
            message = f"Dear {user.username},\n\nThank you for signing up at Night Spot. We're excited to have you on board.\n\nBest regards,\nNight Spot Team"
            recipient_list = [user.email]
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
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
        client_reference_id=ticket.id,
    )

    return JsonResponse({'id': session.id})


def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        logging.error(f"Webhook Error: Invalid payload - {e}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logging.error(f"Webhook Error: Signature verification failed - {e}")
        return HttpResponse(status=400)

    logging.info(f"Received event: {event['type']}")

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        ticket_id = session.get('client_reference_id')
        payment_status = session.get('payment_status')

        logging.info(f"Processing ticket ID: {ticket_id}, Payment Status: {payment_status}")

        if payment_status == 'paid' and ticket_id:
            try:
                ticket = Ticket.objects.get(id=ticket_id)
                ticket.is_sold = True
                ticket.is_available = False
                ticket.save()

                subject = f"Ticket Purchased: {ticket.event_name}"
                message = (
                    f"Dear {ticket.seller},\n\n"
                    f"Your ticket for '{ticket.event_name}' has been purchased successfully.\n\n"
                    "Thank you,\nNight Spot Team"
                )
                recipient_list = [ticket.seller.email]  
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

                logging.info(f"Ticket {ticket_id} marked as sold and email sent to {ticket.seller.email}.")
            except Ticket.DoesNotExist:
                logging.error(f"Ticket with ID {ticket_id} does not exist.")
            except Exception as e:
                logging.error(f"Error sending email: {e}")

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

            try:
                send_mail(subject, message, from_email, [settings.DEFAULT_FROM_EMAIL])
                messages.success(request, "Your message has been sent successfully.")
            except Exception as e:
                logging.error(f"Error sending contact email: {e}")
                messages.error(request, "An error occurred while sending your message.")

            return redirect('success_contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


class TicketSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Ticket.objects.filter(is_available=True)

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

                subject = "Newsletter Subscription Confirmation"
                message = (
                    "Hello,\n\n"
                    "Thank you for subscribing to the Night Spot newsletter. "
                    "Stay tuned for the latest updates and events!\n\n"
                    "Best regards,\nNight Spot Team"
                )
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

            except ApiException as e:
                logging.error(f"Brevo API error: {e}")
                messages.error(request, "An error occurred while adding you to the newsletter.")
            except Exception as e:
                logging.error(f"Email sending error: {e}")
                messages.error(request, "An error occurred while sending the confirmation email.")

            return redirect('newsletter_signup')
    else:
        form = NewsletterSignupForm()
    return render(request, 'newsletter_signup.html', {'form': form})
