"""
Download unique images for each article and replace duplicate body images
"""

from news.models import ArticlePage
from wagtail.images.models import Image
from django.core.files.images import ImageFile
import requests
import uuid
import os
import tempfile

print('=== FIXING DUPLICATE BODY IMAGES ===\n')

# Unsplash image IDs for different marketing topics
UNSPLASH_IMAGES = {
    # AI & Marketing
    'email-marketing-i-2025': ['fikd9t5_5zQ', 'mcSDtbWXUZU'],
    'sådan-skal-du-forberede-dig-til-søgeresultater-med-ai': ['iar-afB0QQw', 'npxXWgQ33ZQ'],
    'influencer-marketing-roi-maaling': ['gMsnXqILjp4', 'W3Jl3jREpDY'],
    'marketing-automation-roi-guide': ['JKUTrJ4vK00', 'Q1p7bh3SHj8'],
    
    # Google Ads
    'google-core-web-vitals-opdatering': ['xG8IQMqMITM', 'jLwVAUtLOAQ'],
    'pinterest-marketing-b2b-guide': ['wD1LRb9OeEo', 'nApaSgkzaxg'],
    
    # Paid Social
    'facebook-ads-strategier-2024': ['dC6Bn0FBTcU', 'Q59HmzK38eQ'],
    'tiktok-ads-begynderguide': ['TamMbr4okv4', 'gySMaocSdqs'],
    'google-analytics-4-migreringsguide': ['hpjSkU2UYSU', 'Mf23Z9CD8g'],
    'programmatic-advertising-guide': ['FHnnjk1Yj7Y', 'JrjhtBJ-pGU'],
    
    # Content
    'marketing-trends-2025': ['505eectW54k', 'OQMZwNd3ThU'],
    'ai-marketing-guide': ['D9Zow2REm8U', 'tZc3LjKv6XY'],
    'content-marketing-masterclass': ['s9CC2SKySJM', 'ZV_64LdGoao'],
    'ugc-marketing-guide': ['2EJCSULRwC8', 'Oalh2MojUuk'],
    'email-marketing-automation': ['xkBaqlcqeb4', 'RLw-UC03Gwc'],
    'community-marketing-strategi': ['g1Kr4Ozfoac', 'QckxruozjRg'],
    
    # CRO
    'content-repurposing-guide': ['UT8LMo-wlyk', 'KE0nC8-58MQ'],
    'seo-content-strategi': ['Q1p7bh3SHj8', 'npxXWgQ33ZQ'],
    'landing-page-optimization': ['xG8IQMqMITM', 'jLwVAUtLOAQ'],
    'ab-testing-guide': ['hpjSkU2UYSU', 'Mf23Z9CD8g'],
    'checkout-optimization': ['FHnnjk1Yj7Y', 'JrjhtBJ-pGU'],
    'mobile-cro-guide': ['505eectW54k', 'OQMZwNd3ThU'],
    'conversion-copywriting': ['D9Zow2REm8U', 'tZc3LjKv6XY'],
    'trust-signals-guide': ['s9CC2SKySJM', 'ZV_64LdGoao'],
    
    # More Google Ads
    'performance-max-guide': ['2EJCSULRwC8', 'Oalh2MojUuk'],
    'meta-ads-2025': ['xkBaqlcqeb4', 'RLw-UC03Gwc'],
    'local-seo-guide': ['g1Kr4Ozfoac', 'QckxruozjRg'],
    'chatgpt-content-marketing-guide': ['UT8LMo-wlyk', 'KE0nC8-58MQ'],
}

def download_and_upload_image(unsplash_id, title):
    """Download image from Unsplash and upload to Wagtail"""
    try:
        # Download image
        url = f'https://images.unsplash.com/photo-{unsplash_id}?w=1600&q=80'
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Save to temp file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        temp_file.write(response.content)
        temp_file.close()
        
        # Upload to Wagtail
        with open(temp_file.name, 'rb') as f:
            image = Image(
                title=title,
                file=ImageFile(f, name=f'{title}.jpg')
            )
            image.save()
        
        # Clean up
        os.unlink(temp_file.name)
        
        return image
    except Exception as e:
        print(f'  ✗ Error downloading {unsplash_id}: {e}')
        return None

# Process each article
fixed_count = 0
articles = ArticlePage.objects.filter(live=True).exclude(category__slug='podcasts')

for article in articles:
    if article.slug not in UNSPLASH_IMAGES:
        continue
    
    print(f'\n{article.title[:50]}...')
    
    # Get current body
    body_list = list(article.body.raw_data) if article.body else []
    
    # Find image blocks
    image_blocks = [(i, b) for i, b in enumerate(body_list) if b.get('type') == 'image']
    
    if len(image_blocks) < 2:
        print(f'  ⚠️  Only {len(image_blocks)} images, skipping')
        continue
    
    # Download 2 new unique images
    unsplash_ids = UNSPLASH_IMAGES[article.slug]
    new_images = []
    
    for i, unsplash_id in enumerate(unsplash_ids[:2]):
        img_title = f'{article.title} - Image {i+1}'
        print(f'  Downloading image {i+1}...')
        image = download_and_upload_image(unsplash_id, img_title)
        if image:
            new_images.append(image)
            print(f'  ✓ Uploaded as ID {image.id}')
    
    if len(new_images) < 2:
        print(f'  ✗ Failed to download images')
        continue
    
    # Replace images in body
    for i, (block_idx, block) in enumerate(image_blocks[:2]):
        body_list[block_idx]['value']['image'] = new_images[i].id
    
    # Save article
    article.body = body_list
    revision = article.save_revision()
    revision.publish()
    
    fixed_count += 1
    print(f'  ✓ Updated with new images')

print(f'\n=== DONE! {fixed_count} articles updated with unique images ===')

