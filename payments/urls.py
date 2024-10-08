from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('', views.payment, name='payment'),
    path('create-ticket/', views.create_ticket, name='create_ticket'),
    path('tickets/', views.ticket_list, name='ticket_list'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', lambda request: render(request, 'success.html'), name='success'),
    path('cancel/', lambda request: render(request, 'cancel.html'), name='cancel'),
    path('tickets/<int:pk>/edit/', views.edit_ticket, name='edit_ticket'),
    path('tickets/<int:pk>/delete/', views.delete_ticket, name='delete_ticket'),
    path('signup/', views.signup, name='signup'),
    path('faq/', views.faq_list, name='faq_list'),
]

