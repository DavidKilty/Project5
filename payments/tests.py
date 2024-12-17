"""
Test suite for the Ticket model in the payments app.
"""

from datetime import delta  
from django.contrib.auth.models import User
from django.test import TestCase
from payments.models import Ticket
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.core.management.base import BaseCommand


class TicketModelTest(TestCase):
    """
    Test case for the Ticket model to validate its behavior.
    """

    def test_ticket_creation(self):
        """
        Test the creation of a Ticket instance.

        Ensures that a ticket can be created with valid data and
        the attributes are correctly set.
        """
        user = User.objects.create_user(username='testuser', password='12345')
        ticket = Ticket.objects.create(
            ticket_type='standard',
            event_name='Test Event',
            event_date=datetime.now(),
            ticket_price=10.00,
            seller=user
        )
        self.assertEqual(ticket.event_name, 'Test Event')

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['event_name', 'event_date', 'ticket_price']

    def clean_event_date(self):
        event_date = self.cleaned_data['event_date']
        if event_date > timezone.now() + timedelta(days=60): 
            raise ValidationError("Tickets cannot be listed for events more than 2 months in advance.")
        return event_date

class Command(BaseCommand):
    help = 'Delete tickets one week past their event date'

    def handle(self, *args, **kwargs):
        week_ago = now() - timedelta(days=7)
        expired_tickets = Ticket.objects.filter(event_date__lt=week_ago)
        count = expired_tickets.count()
        expired_tickets.delete()
        self.stdout.write(f"{count} expired tickets deleted.")