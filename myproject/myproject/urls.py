from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from payments import views  # Corrected import

urlpatterns = [
    path('create-checkout-session/', views.create_checkout_session, name='checkout-session'),
    path('payment/', views.payment, name='payment'),
    path('admin/', admin.site.urls),
    path('', include('payments.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('signup/', views.signup, name='signup'),
    path('faq/', views.faq_list, name='faq_list'),
]
