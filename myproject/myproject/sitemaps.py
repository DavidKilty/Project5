"""
Sitemaps module for managing the TicketSitemap class.
"""

from django.contrib.sitemaps import Sitemap
from payments.models import Ticket


class TicketSitemap(Sitemap):
    """
    Sitemap for Ticket model to manage the priority and change frequency of tickets.
    """
    changefreq = 'daily'
    priority = 0.8

    def items(self):
        """
        Returns all Ticket objects to be included in the sitemap.
        """
        return Ticket.objects.all()

    def lastmod(self, obj):
        """
        Returns the last modified date of a Ticket object.
        
        Args:
            obj (Ticket): The Ticket instance.

        Returns:
            datetime: The last modified date of the Ticket instance.
        """
        return obj.modified_at
