from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from payments import views
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from .sitemaps import TicketSitemap

sitemaps = {
    'tickets': TicketSitemap,
}

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('', include('payments.urls')),
    path('login/', auth_views.LoginView.as_view
         (template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('robots.txt', TemplateView.as_view
         (template_name="robots.txt", content_type="text/plain"),
         name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
]

handler404 = 'payments.views.custom_404_view'
