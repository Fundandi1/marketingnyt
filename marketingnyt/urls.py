"""
URL configuration for marketingnyt project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from news import views as news_views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    # SEO URLs
    path("robots.txt", news_views.robots_txt, name="robots_txt"),
    path("sitemap.xml", news_views.sitemap_index, name="sitemap_index"),
    path("feed.xml", news_views.rss_feed, name="rss_feed"),
    path("healthz", news_views.health_check, name="health_check"),
    # Category URLs
    path("category/<slug:category_slug>/", news_views.category_detail, name="category_detail"),
    # Tag URLs
    path("tag/<slug:tag_slug>/", news_views.tag_detail, name="tag_detail"),
    # Wagtail URLs (catch-all) - handles all pages including ArticlePage and BasicPage
    path("", include(wagtail_urls)),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
