from . import views
from django.urls import path

urlpatterns = [
    path('', views.payment, name='payment'),
    path('create-ticket/', views.create_ticket, name='create_ticket'),
    path('tickets/', views.ticket_list, name='ticket_list'),
    path('tickets/<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('tickets/edit/<int:pk>/', views.edit_ticket, name='edit_ticket'),
    path('tickets/delete/<int:pk>/', views.delete_ticket, name='delete_ticket'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success-contact/', views.success_contact, name='success_contact'),
    path('success/', views.success_page, name='success'),
    path('cancel/', views.cancel_page, name='cancel'),
    path('faq/', views.faq_list, name='faq_list'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('newsletter-signup/', views.newsletter_signup, name='newsletter_signup'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),  
]
