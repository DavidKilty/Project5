from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class Ticket(models.Model):
    TICKET_TYPE_CHOICES = [
        ('guest_list', 'Guest List (Free entry, front of queue)'),
        ('skip_list', 'Skip List (Pay for entry, front of queue)'),
        ('standard', 'Standard Ticket (Queue normally, pay for entry)'),
    ]

    ticket_type = models.CharField(
        max_length=20,
        choices=TICKET_TYPE_CHOICES,
        default='standard'
    )
    event_name = models.CharField(max_length=255)
    event_date = models.DateTimeField()
    ticket_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    is_sold = models.BooleanField(default=False)
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    modified_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)
    unique_code = models.CharField(
        max_length=10,
        default=uuid.uuid4().hex[:10],
        blank=True,
        null=True
    )
    buyer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='purchased_tickets'
    )

    def check_availability(self):
        """
        Updates the availability status of the ticket.
        A ticket is unavailable if it's sold or if the event
        date is in the past.
        """
        self.is_available = not (
            self.is_sold or self.event_date < timezone.now()
        )
        self.save()


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question


class Testimonial(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="testimonials"
    )
    title = models.CharField(
        max_length=255,
        help_text="Short title or headline for the testimonial."
    )
    content = models.TextField(help_text="The main testimonial content.")
    date_posted = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(
        default=False,
        help_text="Admin approval for display."
    )

    class Meta:
        ordering = ["-date_posted"]

    def __str__(self):
        return f"Testimonial by {self.user.username} - {self.title}"
