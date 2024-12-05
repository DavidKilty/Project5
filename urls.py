from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from payments import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('payment/', permanent=False)),
    path('payment/', include('payments.urls')),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
