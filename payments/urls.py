# payments/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_page, name='payment'),  # Use an empty string for the payment page URL
]