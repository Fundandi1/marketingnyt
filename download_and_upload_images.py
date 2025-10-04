#!/usr/bin/env python3
"""
Script to download relevant images from Unsplash and upload them to Wagtail.
"""
import os
import sys
import django
import requests
from pathlib import Path

# Setup Django
sys.path.insert(0, '/Users/mikkelfunder/Marketingnyt.dk')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketingnyt.settings.dev')
django.setup()

from django.core.files.images import ImageFile
from wagtail.images.models import Image
from news.models import ArticlePage, Category

# Unsplash image URLs (using direct download links for free stock photos)
IMAGES = {
    # AI & Marketing images
    'ai_chatbot': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1600&q=80',  # AI/Robot
    'ai_automation': 'https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=1600&q=80',  # AI technology
    'ai_marketing': 'https://images.unsplash.com/photo-1655393001768-d946c97d6fd1?w=1600&q=80',  # AI brain
    'email_marketing': 'https://images.unsplash.com/photo-1596526131083-e8c633c948d2?w=1600&q=80',  # Email
    'influencer': 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=1600&q=80',  # Influencer
    
    # Paid Social images
    'facebook_ads': 'https://images.unsplash.com/photo-1611162616305-c69b3fa7fbe0?w=1600&q=80',  # Facebook
    'tiktok': 'https://images.unsplash.com/photo-1611162616475-46b635cb6868?w=1600&q=80',  # TikTok
    'social_media': 'https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=1600&q=80',  # Social media
    'instagram': 'https://images.unsplash.com/photo-1611162618071-b39a2ec055fb?w=1600&q=80',  # Instagram
    'analytics': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1600&q=80',  # Analytics dashboard
    'programmatic': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1600&q=80',  # Digital advertising
    
    # Google Ads / SEO images
    'google_search': 'https://images.unsplash.com/photo-1573804633927-bfcbcd909acd?w=1600&q=80',  # Google
    'seo': 'https://images.unsplash.com/photo-1562577309-4932fdd64cd1?w=1600&q=80',  # SEO
    'local_seo': 'https://images.unsplash.com/photo-1524661135-423995f22d0b?w=1600&q=80',  # Local business
    'performance_max': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1600&q=80',  # Performance
    'pinterest': 'https://images.unsplash.com/photo-1611162616305-c69b3fa7fbe0?w=1600&q=80',  # Pinterest
    
    # Content Marketing images
    'content_creation': 'https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=1600&q=80',  # Writing
    'video_marketing': 'https://images.unsplash.com/photo-1492619375914-88005aa9e8fb?w=1600&q=80',  # Video
    'ugc': 'https://images.unsplash.com/photo-1556761175-b413da4baf72?w=1600&q=80',  # User content
    'email_automation': 'https://images.unsplash.com/photo-1563986768609-322da13575f3?w=1600&q=80',  # Email automation
    'community': 'https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=1600&q=80',  # Community
    'repurposing': 'https://images.unsplash.com/photo-1432888498266-38ffec3eaf0a?w=1600&q=80',  # Content repurposing
    
    # CRO images
    'landing_page': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1600&q=80',  # Landing page
    'ab_testing': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1600&q=80',  # A/B testing
    'checkout': 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=1600&q=80',  # Checkout
    'mobile_cro': 'https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=1600&q=80',  # Mobile
    'copywriting': 'https://images.unsplash.com/photo-1455390582262-044cdead277a?w=1600&q=80',  # Copywriting
    'trust': 'https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=1600&q=80',  # Trust/handshake
    
    # Podcast images
    'podcast_mic': 'https://images.unsplash.com/photo-1478737270239-2f02b77fc618?w=1600&q=80',  # Podcast microphone
    'podcast_studio': 'https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=1600&q=80',  # Podcast studio
}

# Article to image mapping
ARTICLE_IMAGE_MAP = {
    # AI & Marketing
    'chatgpt-content-marketing-guide': 'ai_chatbot',
    'marketing-automation-roi-guide': 'ai_automation',
    'email-marketing-i-2025': 'email_marketing',
    'sådan-skal-du-forberede-dig-til-søgeresultater-med-ai': 'ai_marketing',
    'influencer-marketing-roi-maaling': 'influencer',
    
    # Paid Social
    'facebook-ads-strategier-2024': 'facebook_ads',
    'tiktok-ads-begynderguide': 'tiktok',
    'google-analytics-4-migreringsguide': 'analytics',
    'programmatic-advertising-guide': 'programmatic',
    'meta-ads-2025': 'instagram',
    'tiktok-ads-demografi': 'tiktok',
    
    # Google Ads
    'google-lancerer-ny-core-web-vitals-opdatering': 'google_search',
    'local-seo-guide': 'local_seo',
    'performance-max-guide': 'performance_max',
    'pinterest-marketing-b2b': 'pinterest',
    'google-ads-keyword-strategy': 'seo',
    
    # Content
    'ugc-marketing-guide': 'ugc',
    'email-marketing-automation-guide': 'email_automation',
    'community-marketing-guide': 'community',
    'content-repurposing-guide': 'repurposing',
    'seo-content-strategy-2025': 'seo',
    'video-marketing-guide': 'video_marketing',
    
    # CRO
    'landing-page-optimization-guide': 'landing_page',
    'ab-testing-guide-2025': 'ab_testing',
    'checkout-optimization-guide': 'checkout',
    'mobile-cro-guide': 'mobile_cro',
    'conversion-copywriting-guide': 'copywriting',
    'trust-signals-guide': 'trust',
    
    # Podcasts
    'marketing-trends-2025-podcast': 'podcast_mic',
    'ai-marketing-podcast': 'podcast_studio',
    'content-marketing-podcast': 'podcast_mic',
}

def download_image(url, filename):
    """Download image from URL."""
    print(f"Downloading {filename}...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        filepath = f'/Users/mikkelfunder/Marketingnyt.dk/media/temp_images/{filename}'
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"✓ Downloaded {filename}")
        return filepath
    else:
        print(f"✗ Failed to download {filename}: {response.status_code}")
        return None

def upload_to_wagtail(filepath, title):
    """Upload image to Wagtail."""
    print(f"Uploading {title} to Wagtail...")
    
    # Check if image already exists
    existing = Image.objects.filter(title=title).first()
    if existing:
        print(f"✓ Image '{title}' already exists (ID: {existing.id})")
        return existing
    
    with open(filepath, 'rb') as f:
        image_file = ImageFile(f, name=os.path.basename(filepath))
        image = Image(
            title=title,
            file=image_file,
        )
        image.save()
        print(f"✓ Uploaded {title} (ID: {image.id})")
        return image

def main():
    print("=" * 60)
    print("DOWNLOADING AND UPLOADING IMAGES FROM UNSPLASH")
    print("=" * 60)
    
    # Download and upload all images
    uploaded_images = {}
    for key, url in IMAGES.items():
        filename = f"{key}.jpg"
        filepath = download_image(url, filename)
        if filepath:
            title = key.replace('_', ' ').title()
            image = upload_to_wagtail(filepath, title)
            if image:
                uploaded_images[key] = image
    
    print("\n" + "=" * 60)
    print("ASSIGNING IMAGES TO ARTICLES")
    print("=" * 60)
    
    # Assign images to articles
    for article_slug, image_key in ARTICLE_IMAGE_MAP.items():
        article = ArticlePage.objects.filter(slug=article_slug).first()
        if not article:
            print(f"✗ Article not found: {article_slug}")
            continue
        
        if image_key not in uploaded_images:
            print(f"✗ Image not found: {image_key}")
            continue
        
        image = uploaded_images[image_key]
        article.cover_image = image
        
        # Save and publish
        revision = article.save_revision()
        revision.publish()
        
        print(f"✓ {article.title[:50]}... → {image.title}")
    
    print("\n" + "=" * 60)
    print("DONE!")
    print("=" * 60)

if __name__ == '__main__':
    main()

