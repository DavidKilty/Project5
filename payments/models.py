from django.db import models
from django.contrib.auth.models import User

# Ticket 
class Ticket(models.Model):
    event_name = models.CharField(max_length=200)
    event_date = models.DateTimeField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(User, related_name='tickets', on_delete=models.CASCADE)
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.event_name} - {self.ticket_price}"

# Transactional
class Transaction(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='transactions', on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE)
    stripe_transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)

    def __str__(self):
        return f"Transaction {self.stripe_transaction_id} - {self.amount}"
