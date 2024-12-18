from django.contrib import admin
from .models import FAQ
from .models import Testimonial


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at', 'updated_at')
    search_fields = ('question',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "date_posted", "approved")
    list_filter = ("approved", "date_posted")
    search_fields = ("title", "user__username", "content")
    actions = ["approve_testimonials"]

    def approve_testimonials(self, request, queryset):
        queryset.update(approved=True)
    approve_testimonials.short_description = "Approve selected testimonials"
