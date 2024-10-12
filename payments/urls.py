from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment, name='payment'),
    path('create-ticket/', views.create_ticket, name='create_ticket'),
    path('tickets/', views.ticket_list, name='ticket_list'),
    path('tickets/<int:pk>/', views.ticket_detail, name='ticket_detail'),  
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.success_page, name='success'),
    path('cancel/', views.cancel_page, name='cancel'),
    path('signup/', views.signup, name='signup'),
    path('faq/', views.faq_list, name='faq_list'),
    path('contact/', views.contact, name='contact'),
]
