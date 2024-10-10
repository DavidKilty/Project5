from django.contrib.sitemaps import Sitemap
from .models import Ticket

class TicketSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Ticket.objects.all()

    def lastmod(self, obj):
        return obj.updated_at 