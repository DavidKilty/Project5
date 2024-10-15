from django.test import TestCase
from .models import Ticket
from django.contrib.auth.models import User
from datetime import datetime

class TicketModelTest(TestCase):
    def test_ticket_creation(self):
        user = User.objects.create_user(username='testuser', password='12345')
        ticket = Ticket.objects.create(
            ticket_type='standard',
            event_name='Test Event',
            event_date=datetime.now(),
            ticket_price=10.00,
            seller=user
        )
        self.assertEqual(ticket.event_name, 'Test Event')
