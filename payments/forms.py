from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['event_name', 'event_date', 'ticket_price', 'ticket_type']  # Include ticket_type
        widgets = {
            'event_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),  # HTML5 date-time picker
        }
