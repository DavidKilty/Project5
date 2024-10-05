from django.db import models
from django.contrib.auth.models import User

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

    def __str__(self):
        return f"{self.event_name} - {self.get_ticket_type_display()}"