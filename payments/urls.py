from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_page, name='payment'), 
    path('create-ticket/', views.create_ticket, name='create_ticket'),  
    path('tickets/', views.ticket_list, name='ticket_list'), 
]