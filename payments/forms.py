from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Ticket, FAQ
from .models import Testimonial


class TicketForm(forms.ModelForm):
    """Form for creating and editing Ticket instances."""

    class Meta:
        model = Ticket
        fields = ['event_name', 'event_date', 'ticket_price', 'ticket_type']
        widgets = {
            'event_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_event_date(self):
        """Validate that the event date is not in the past."""
        event_date = self.cleaned_data['event_date']
        if event_date < timezone.now():
            raise forms.ValidationError("The event date cannot be in the past.")
        return event_date

    def clean_ticket_price(self):
        """Validate that the ticket price is at least 1 EUR."""
        price = self.cleaned_data.get('ticket_price')
        if price < 1:
            raise forms.ValidationError('Ticket price must be at least 1 EUR.')
        return price


class SignUpForm(UserCreationForm):
    """Form for user registration."""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class FAQForm(forms.ModelForm):
    """Form for creating and editing FAQ instances."""

    class Meta:
        model = FAQ
        fields = ['question', 'answer']


class ContactForm(forms.Form):
    """Form for user contact submissions."""
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)


class NewsletterSignupForm(forms.Form):
    """Form for newsletter signup."""
    email = forms.EmailField(
        label="Email",
        max_length=255,
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your email'}
        )
    )

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Short headline"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Your testimonial here..."}),
        }