"""
Context processors for the news app.
"""

from .models import SiteSettings, Category


def site_settings(request):
    """Add site settings to template context."""
    try:
        settings = SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        settings = None
    
    categories = Category.objects.all()
    
    return {
        "site_settings": settings,
        "categories": categories,
    }
