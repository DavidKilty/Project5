"""
Test suite for the Ticket model in the payments app.
"""

from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from payments.models import Ticket


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
