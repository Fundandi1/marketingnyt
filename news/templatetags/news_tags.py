"""
Template tags for the news app.
"""

import re
from django import template
from django.utils.safestring import mark_safe
from bs4 import BeautifulSoup

register = template.Library()


@register.filter
def table_of_contents(value):
    """Generate table of contents from StreamField content."""
    if not value:
        return ""
    
    headings = []
    for block in value:
        if block.block_type == "heading":
            level = block.value["level"]
            text = block.value["text"]
            slug = re.sub(r"[^\w\s-]", "", text).strip().lower()
            slug = re.sub(r"[-\s]+", "-", slug)
            headings.append({
                "level": level,
                "text": text,
                "slug": slug,
            })
        elif block.block_type == "rich_text":
            # Extract headings from rich text
            soup = BeautifulSoup(str(block.value), "html.parser")
            for heading in soup.find_all(["h2", "h3"]):
                text = heading.get_text().strip()
                if text:
                    slug = re.sub(r"[^\w\s-]", "", text).strip().lower()
                    slug = re.sub(r"[-\s]+", "-", slug)
                    headings.append({
                        "level": heading.name,
                        "text": text,
                        "slug": slug,
                    })
    
    if not headings:
        return ""
    
    toc_html = '<div class="table-of-contents"><h3>Indholdsfortegnelse</h3><ul>'
    for heading in headings:
        level_class = "toc-h2" if heading["level"] == "h2" else "toc-h3"
        toc_html += f'<li class="{level_class}"><a href="#{heading["slug"]}">{heading["text"]}</a></li>'
    toc_html += "</ul></div>"
    
    return mark_safe(toc_html)


@register.filter
def add_heading_ids(value):
    """Add IDs to headings in StreamField content."""
    if not value:
        return value
    
    # This would be implemented to add IDs to headings in the rendered HTML
    # For now, we'll rely on the template implementation
    return value


@register.simple_tag
def breadcrumbs(page):
    """Generate breadcrumbs for a page."""
    ancestors = page.get_ancestors(inclusive=True).live().public()
    breadcrumbs_list = []
    
    for ancestor in ancestors:
        if ancestor.depth > 1:  # Skip root page
            breadcrumbs_list.append({
                "title": ancestor.title,
                "url": ancestor.get_full_url(),
            })
    
    return breadcrumbs_list


@register.inclusion_tag("news/tags/related_articles.html", takes_context=True)
def related_articles(context, article, limit=3):
    """Get related articles for an article."""
    related = article.get_context(context["request"])["related_articles"][:limit]
    return {"related_articles": related}


@register.simple_tag
def json_ld_organization():
    """Generate JSON-LD for organization."""
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "MarketingNyt.dk",
        "url": "https://marketingnyt.dk",
        "logo": "https://marketingnyt.dk/static/images/logo.png",
        "sameAs": [
            "https://twitter.com/marketingnyt",
            "https://facebook.com/marketingnyt",
            "https://linkedin.com/company/marketingnyt",
        ],
    }


@register.simple_tag
def json_ld_article(article, request):
    """Generate JSON-LD for an article."""
    return {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": article.title,
        "description": article.summary,
        "datePublished": article.published_at.isoformat(),
        "dateModified": (article.last_published_at or article.published_at).isoformat(),
        "author": {
            "@type": "Person",
            "name": article.author,
        },
        "publisher": {
            "@type": "Organization",
            "name": "MarketingNyt.dk",
            "logo": {
                "@type": "ImageObject",
                "url": "https://marketingnyt.dk/static/images/logo.png",
            },
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": article.get_full_url(request),
        },
        "image": article.cover_image.get_rendition("fill-1200x630").full_url if article.cover_image else None,
    }


@register.simple_tag
def json_ld_breadcrumbs(page, request):
    """Generate JSON-LD breadcrumbs."""
    ancestors = page.get_ancestors(inclusive=True).live().public()
    items = []

    for i, ancestor in enumerate(ancestors):
        if ancestor.depth > 1:  # Skip root page
            items.append({
                "@type": "ListItem",
                "position": i,
                "name": ancestor.title,
                "item": ancestor.get_full_url(request),
            })

    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
    }


@register.simple_tag
def get_categories():
    """Get all categories for navigation."""
    from news.models import Category
    return Category.objects.all().order_by('name')


@register.filter
def article_url(article):
    """Get the URL for an article (external_url if set, otherwise article page)."""
    if hasattr(article, 'external_url') and article.external_url:
        return article.external_url
    return f"/{article.slug}/"


@register.filter
def article_target(article):
    """Get the target attribute for an article link."""
    if hasattr(article, 'external_url') and article.external_url:
        return "_blank"
    return ""


@register.filter
def article_rel(article):
    """Get the rel attribute for an article link."""
    if hasattr(article, 'external_url') and article.external_url:
        return "noopener noreferrer"
    return ""
