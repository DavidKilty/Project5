from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_page, name='payment'),
    path('create-ticket/', views.create_ticket, name='create_ticket'),
    path('tickets/', views.ticket_list, name='ticket_list'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', lambda request: render(request, 'success.html'), name='success'),  
    path('cancel/', lambda request: render(request, 'cancel.html'), name='cancel'),  
]
