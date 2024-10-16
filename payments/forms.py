from django import forms
from .models import Ticket, FAQ
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['event_name', 'event_date', 'ticket_price', 'ticket_type']
        widgets = {
            'event_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_event_date(self):
        event_date = self.cleaned_data['event_date']
        if event_date < timezone.now():
            raise forms.ValidationError("The event date cannot be in the past.")
        return event_date
    def clean_ticket_price(self):
        price = self.cleaned_data.get('ticket_price')
        if price < 1:
            raise forms.ValidationError('Ticket price must be at least 1 EUR.')
        return price

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer']

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)

class NewsletterSignupForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=255, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))