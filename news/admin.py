"""
Admin configuration for the news app.
"""

from django.contrib import admin
from .models import Category, SiteSettings


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin for Category model."""
    list_display = ["name", "slug", "description"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Admin for SiteSettings model."""
    list_display = ["site_name"]
