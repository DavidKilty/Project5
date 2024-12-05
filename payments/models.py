from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone


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


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
