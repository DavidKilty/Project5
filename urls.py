from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from payments import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('payment/', permanent=False)),  
    path('payment/', include('payments.urls')), 
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),  
]
