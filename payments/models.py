from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


def generate_unique_code():
    return uuid.uuid4().hex[:10]


class Ticket(models.Model):
    TICKET_TYPE_CHOICES = [
        ('guest_list', 'Guest List (Free entry, front of queue)'),
        ('skip_list', 'Skip List (Pay for entry, front of queue)'),
        ('standard', 'Standard Ticket (Queue normally, pay for entry)'),
    ]

    ticket_type = models.CharField(max_length=20, choices=TICKET_TYPE_CHOICES, default='standard')
    event_name = models.CharField(max_length=255)
    event_date = models.DateTimeField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_sold = models.BooleanField(default=False)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)
    unique_code = models.CharField(max_length=10, unique=True, default=generate_unique_code)
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchased_tickets')

    def __str__(self):
        return f"{self.event_name} - {self.get_ticket_type_display()}"

    def get_absolute_url(self):
        return reverse('ticket_detail', args=[str(self.pk)])

    def check_availability(self):
        """
        Updates the availability status of the ticket.
        A ticket is unavailable if it's sold or if the event date is in the past.
        """
        self.is_available = not (self.is_sold or self.event_date < timezone.now())
        self.save()

    def save(self, *args, **kwargs):
        self.check_availability()
        super().save(*args, **kwargs)
