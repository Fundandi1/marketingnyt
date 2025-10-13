"""
Views for the news app.
"""

from django.contrib.sitemaps import Sitemap
from django.contrib.syndication.views import Feed
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from .models import ArticlePage, Category


def robots_txt(request):
    """Robots.txt view."""
    # Always use the main domain for sitemap URL
    site_url = "https://www.marketingnyt.dk"

    content = f"""User-agent: *
Allow: /

# Disallow admin areas
Disallow: /admin/
Disallow: /django-admin/

# Sitemap
Sitemap: {site_url}/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain")


def sitemap_index(request):
    """Sitemap index view."""
    from django.contrib.sitemaps import views as sitemap_views
    from django.contrib.sitemaps.views import index

    sitemaps = {
        "articles": ArticleSitemap,
        "categories": CategorySitemap,
        "static": StaticSitemap,
    }

    return index(request, sitemaps)


def sitemap_section(request, section):
    """Individual sitemap section view."""
    from django.contrib.sitemaps.views import sitemap

    sitemaps = {
        "articles": ArticleSitemap,
        "categories": CategorySitemap,
        "static": StaticSitemap,
    }

    return sitemap(request, sitemaps, section)


def health_check(request):
    """Health check endpoint."""
    return HttpResponse("OK", content_type="text/plain")


def article_detail(request, slug):
    """Article detail view."""
    article = get_object_or_404(ArticlePage, slug=slug)

    # Get related articles from same category (excluding podcasts)
    from news.models import Category
    podcast_category = Category.objects.filter(slug='podcasts').first()

    related_query = ArticlePage.objects.filter(
        live=True,
        category=article.category
    ).exclude(id=article.id)

    if podcast_category:
        related_query = related_query.exclude(category=podcast_category)

    related_articles = list(related_query.order_by('-published_at')[:3])

    # If not enough related by category, get from other categories (excluding podcasts)
    if len(related_articles) < 3:
        additional_query = ArticlePage.objects.filter(live=True).exclude(id=article.id)

        if podcast_category:
            additional_query = additional_query.exclude(category=podcast_category)

        # Exclude current category and already selected articles
        additional_query = additional_query.exclude(category=article.category)
        if related_articles:
            additional_query = additional_query.exclude(
                id__in=[art.id for art in related_articles]
            )

        additional_related = list(additional_query.order_by('-published_at')[:3 - len(related_articles)])
        related_articles = related_articles + additional_related

    context = {
        'page': article,
        'related_articles': related_articles,
    }

    return render(request, 'news/article_page.html', context)


def tag_detail(request, tag_slug):
    """Tag detail view - shows all articles with a specific tag."""
    from taggit.models import Tag
    from django.core.paginator import Paginator

    tag = get_object_or_404(Tag, slug=tag_slug)

    # Get articles with this tag
    articles = ArticlePage.objects.live().filter(
        tags__slug=tag_slug
    ).order_by("-published_at")

    # Pagination
    paginator = Paginator(articles, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'tag': tag,
        'articles': page_obj,
        'page_title': f'Artikler tagget med "{tag.name}"',
    }

    return render(request, 'news/tag_page.html', context)


def category_detail(request, category_slug):
    """Category detail view - shows all articles in a specific category."""
    from django.core.paginator import Paginator

    category = get_object_or_404(Category, slug=category_slug)

    # Get articles in this category
    articles = ArticlePage.objects.live().filter(
        category=category
    ).order_by("-published_at")

    # Pagination
    paginator = Paginator(articles, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'articles': page_obj,
        'page_title': category.name,
    }

    return render(request, 'news/category_page.html', context)


class RSSFeed(Feed):
    """RSS feed for articles."""
    title = "MarketingNyt.dk - Seneste nyheder"
    link = "/"
    description = "De seneste nyheder fra MarketingNyt.dk"
    
    def items(self):
        return ArticlePage.objects.live().order_by("-published_at")[:50]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return item.summary
    
    def item_link(self, item):
        return item.get_full_url()
    
    def item_pubdate(self, item):
        return item.published_at
    
    def item_author_name(self, item):
        return item.author


rss_feed = RSSFeed()


class ArticleSitemap(Sitemap):
    """Sitemap for articles."""
    changefreq = "weekly"
    priority = 0.8
    
    def items(self):
        return ArticlePage.objects.live().order_by("-published_at")
    
    def lastmod(self, obj):
        return obj.last_published_at or obj.published_at
    
    def location(self, obj):
        return obj.get_full_url()


class CategorySitemap(Sitemap):
    """Sitemap for categories."""
    changefreq = "monthly"
    priority = 0.6
    
    def items(self):
        from .models import CategoryPage
        return CategoryPage.objects.live()
    
    def lastmod(self, obj):
        return obj.last_published_at
    
    def location(self, obj):
        return obj.get_full_url()


class StaticSitemap(Sitemap):
    """Sitemap for static pages."""
    changefreq = "monthly"
    priority = 1.0
    
    def items(self):
        from .models import HomePage
        return HomePage.objects.live()
    
    def lastmod(self, obj):
        return obj.last_published_at
    
    def location(self, obj):
        return obj.get_full_url()
