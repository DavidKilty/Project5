from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('create-checkout-session/', views.create_checkout_session, name='checkout-session'),
    path('payment/', views.payment, name='payment'),
    path('success/', views.success_page, name='success'),
    path('cancel/', views.cancel_page, name='cancel'),
    path('admin/', admin.site.urls),
    path('', include('payments.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('signup/', views.signup, name='signup'),
]
