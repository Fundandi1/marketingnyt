"""
Advanced SEO optimizations for MarketingNyt.dk
"""

import json
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.conf import settings
from wagtail.models import Page


def generate_structured_data(page, request=None):
    """
    Generate comprehensive JSON-LD structured data for better SEO.
    """
    base_url = getattr(settings, 'BASE_URL', 'https://marketingnyt.dk')
    if request:
        base_url = request.build_absolute_uri('/')[:-1]
    
    # Base organization data
    organization_data = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "MarketingNyt.dk",
        "url": base_url,
        "logo": f"{base_url}/static/images/logo.png",
        "description": "Danmarks førende platform for marketing nyheder, trends og insights",
        "sameAs": [
            "https://twitter.com/marketingnyt",
            "https://facebook.com/marketingnyt",
            "https://linkedin.com/company/marketingnyt"
        ],
        "contactPoint": {
            "@type": "ContactPoint",
            "contactType": "customer service",
            "availableLanguage": "Danish"
        }
    }
    
    # Website data
    website_data = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "MarketingNyt.dk",
        "url": base_url,
        "description": "Danmarks førende platform for marketing nyheder, trends og insights",
        "inLanguage": "da-DK",
        "potentialAction": {
            "@type": "SearchAction",
            "target": f"{base_url}/search/?q={{search_term_string}}",
            "query-input": "required name=search_term_string"
        }
    }
    
    structured_data = [organization_data, website_data]
    
    # Page-specific structured data
    if hasattr(page, 'specific'):
        page = page.specific
    
    # Article page structured data
    if hasattr(page, 'published_at') and hasattr(page, 'author'):
        article_data = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": page.title,
            "description": getattr(page, 'summary', page.search_description or ''),
            "author": {
                "@type": "Person",
                "name": page.author
            },
            "publisher": organization_data,
            "datePublished": page.published_at.isoformat() if page.published_at else None,
            "dateModified": page.last_published_at.isoformat() if page.last_published_at else None,
            "url": f"{base_url}{page.url}",
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": f"{base_url}{page.url}"
            }
        }
        
        # Add image if available
        if hasattr(page, 'cover_image') and page.cover_image:
            try:
                image_rendition = page.cover_image.get_rendition('width-1200')
                article_data["image"] = {
                    "@type": "ImageObject",
                    "url": f"{base_url}{image_rendition.url}",
                    "width": image_rendition.width,
                    "height": image_rendition.height
                }
            except:
                pass
        
        # Add category/section
        if hasattr(page, 'category') and page.category:
            article_data["articleSection"] = page.category.name
        
        structured_data.append(article_data)
    
    # Breadcrumb structured data
    if page.get_ancestors().exists():
        breadcrumb_items = []
        position = 1
        
        # Add home
        breadcrumb_items.append({
            "@type": "ListItem",
            "position": position,
            "name": "Hjem",
            "item": base_url
        })
        position += 1
        
        # Add ancestors
        for ancestor in page.get_ancestors()[1:]:  # Skip root
            breadcrumb_items.append({
                "@type": "ListItem",
                "position": position,
                "name": ancestor.title,
                "item": f"{base_url}{ancestor.url}"
            })
            position += 1
        
        # Add current page
        breadcrumb_items.append({
            "@type": "ListItem",
            "position": position,
            "name": page.title,
            "item": f"{base_url}{page.url}"
        })
        
        breadcrumb_data = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": breadcrumb_items
        }
        
        structured_data.append(breadcrumb_data)
    
    return structured_data


def generate_meta_tags(page, request=None):
    """
    Generate comprehensive meta tags for optimal SEO.
    """
    base_url = getattr(settings, 'BASE_URL', 'https://marketingnyt.dk')
    if request:
        base_url = request.build_absolute_uri('/')[:-1]
    
    meta_tags = []
    
    # Basic meta tags
    title = page.seo_title or page.title
    description = page.search_description or getattr(page, 'summary', '')
    
    if title:
        meta_tags.append(f'<title>{title} - MarketingNyt.dk</title>')
    
    if description:
        meta_tags.append(f'<meta name="description" content="{description}">')
    
    # Canonical URL
    canonical_url = f"{base_url}{page.url}"
    meta_tags.append(f'<link rel="canonical" href="{canonical_url}">')
    
    # Open Graph tags
    meta_tags.extend([
        f'<meta property="og:title" content="{title}">',
        f'<meta property="og:description" content="{description}">',
        f'<meta property="og:url" content="{canonical_url}">',
        f'<meta property="og:site_name" content="MarketingNyt.dk">',
        f'<meta property="og:locale" content="da_DK">',
    ])
    
    # Article-specific Open Graph
    if hasattr(page, 'published_at') and hasattr(page, 'author'):
        meta_tags.extend([
            '<meta property="og:type" content="article">',
            f'<meta property="article:author" content="{page.author}">',
        ])
        
        if page.published_at:
            meta_tags.append(f'<meta property="article:published_time" content="{page.published_at.isoformat()}">')
        
        if hasattr(page, 'category') and page.category:
            meta_tags.append(f'<meta property="article:section" content="{page.category.name}">')
    else:
        meta_tags.append('<meta property="og:type" content="website">')
    
    # Twitter Card tags
    meta_tags.extend([
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{title}">',
        f'<meta name="twitter:description" content="{description}">',
        '<meta name="twitter:site" content="@marketingnyt">',
    ])
    
    # Image meta tags
    if hasattr(page, 'cover_image') and page.cover_image:
        try:
            image_rendition = page.cover_image.get_rendition('fill-1200x630')
            image_url = f"{base_url}{image_rendition.url}"
            
            meta_tags.extend([
                f'<meta property="og:image" content="{image_url}">',
                f'<meta property="og:image:width" content="{image_rendition.width}">',
                f'<meta property="og:image:height" content="{image_rendition.height}">',
                f'<meta name="twitter:image" content="{image_url}">',
            ])
        except:
            pass
    
    # Additional SEO tags
    meta_tags.extend([
        '<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">',
        '<meta name="googlebot" content="index, follow">',
        f'<meta name="author" content="{getattr(page, "author", "MarketingNyt.dk")}">',
        '<meta name="language" content="Danish">',
        '<meta name="geo.region" content="DK">',
        '<meta name="geo.country" content="Denmark">',
    ])
    
    return meta_tags


def generate_hreflang_tags(page, request=None):
    """
    Generate hreflang tags for international SEO (future expansion).
    """
    base_url = getattr(settings, 'BASE_URL', 'https://marketingnyt.dk')
    if request:
        base_url = request.build_absolute_uri('/')[:-1]
    
    hreflang_tags = [
        f'<link rel="alternate" hreflang="da" href="{base_url}{page.url}">',
        f'<link rel="alternate" hreflang="da-DK" href="{base_url}{page.url}">',
        f'<link rel="alternate" hreflang="x-default" href="{base_url}{page.url}">',
    ]
    
    return hreflang_tags


def get_page_performance_score(page):
    """
    Calculate a performance score for the page based on various factors.
    """
    score = 100
    
    # Title length check
    title = page.seo_title or page.title
    if len(title) > 60:
        score -= 10
    elif len(title) < 30:
        score -= 5
    
    # Description length check
    description = page.search_description or getattr(page, 'summary', '')
    if len(description) > 160:
        score -= 10
    elif len(description) < 120:
        score -= 5
    
    # Image optimization check
    if hasattr(page, 'cover_image') and not page.cover_image:
        score -= 15
    
    # Content length check (for articles)
    if hasattr(page, 'body'):
        content_length = len(str(page.body))
        if content_length < 300:
            score -= 20
    
    return max(0, score)


def generate_sitemap_entry(page, request=None):
    """
    Generate sitemap entry for a page with proper priority and change frequency.
    """
    base_url = getattr(settings, 'BASE_URL', 'https://marketingnyt.dk')
    if request:
        base_url = request.build_absolute_uri('/')[:-1]
    
    # Determine priority based on page type and depth
    priority = 0.5
    if page.depth == 2:  # Homepage
        priority = 1.0
    elif page.depth == 3:  # Main sections
        priority = 0.8
    elif hasattr(page, 'published_at'):  # Articles
        priority = 0.6
    
    # Determine change frequency
    changefreq = 'monthly'
    if hasattr(page, 'published_at'):
        changefreq = 'weekly'
    if page.depth == 2:  # Homepage
        changefreq = 'daily'
    
    return {
        'location': f"{base_url}{page.url}",
        'lastmod': page.last_published_at or page.latest_revision_created_at,
        'changefreq': changefreq,
        'priority': priority
    }
