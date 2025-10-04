#!/usr/bin/env python3
"""
Script to add 2 relevant images to each article.
Downloads images from Unsplash and inserts them into article body.
"""

import os
import sys
import django
import requests
import json
import uuid

# Setup Django
sys.path.append('/Users/mikkelfunder/Marketingnyt.dk')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketingnyt.settings')
django.setup()

from news.models import ArticlePage
from wagtail.images.models import Image
from django.core.files.images import ImageFile

# Unsplash image URLs - 2 images per category
CATEGORY_IMAGES = {
    'AI & Marketing': [
        ('https://images.unsplash.com/photo-1655720828018-edd2daec9349?w=1600&q=80', 'AI Marketing Dashboard'),
        ('https://images.unsplash.com/photo-1676277791608-ac3b5a0893d1?w=1600&q=80', 'AI Content Creation'),
    ],
    'Paid Social': [
        ('https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=1600&q=80', 'Social Media Strategy'),
        ('https://images.unsplash.com/photo-1432888622747-4eb9a8f2c293?w=1600&q=80', 'Social Media Analytics Dashboard'),
    ],
    'Google Ads': [
        ('https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1600&q=80', 'Google Ads Dashboard'),
        ('https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1600&q=80', 'Analytics and Data'),
    ],
    'Content': [
        ('https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=1600&q=80', 'Content Writing'),
        ('https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=1600&q=80', 'Content Team Collaboration'),
    ],
    'CRO': [
        ('https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1600&q=80', 'Conversion Analytics'),
        ('https://images.unsplash.com/photo-1551434678-e076c223a692?w=1600&q=80', 'User Experience Design'),
    ],
}

def download_image(url, filename):
    """Download image from URL."""
    try:
        response = requests.get(url, stream=True, timeout=30)
        if response.status_code == 200:
            filepath = f'/Users/mikkelfunder/Marketingnyt.dk/media/temp_images/{filename}'
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return filepath
        else:
            print(f'  ✗ Failed to download {url}: {response.status_code}')
            return None
    except Exception as e:
        print(f'  ✗ Error downloading {url}: {e}')
        return None

def upload_to_wagtail(filepath, title):
    """Upload image to Wagtail."""
    try:
        # Check if image already exists
        existing = Image.objects.filter(title=title).first()
        if existing:
            print(f'  → Image already exists: {title}')
            return existing
        
        with open(filepath, 'rb') as f:
            image_file = ImageFile(f, name=os.path.basename(filepath))
            image = Image(title=title, file=image_file)
            image.save()
            print(f'  ✓ Uploaded: {title} (ID: {image.id})')
            return image
    except Exception as e:
        print(f'  ✗ Error uploading {filepath}: {e}')
        return None

def insert_images_into_body(body_data, image1, image2):
    """Insert 2 images into article body at strategic positions."""
    if not body_data:
        return body_data
    
    # Parse body if it's a string
    if isinstance(body_data, str):
        try:
            body_list = json.loads(body_data)
        except:
            return body_data
    else:
        body_list = body_data
    
    if not isinstance(body_list, list) or len(body_list) == 0:
        return body_data
    
    # Calculate positions to insert images
    # Insert first image after ~1/3 of content
    # Insert second image after ~2/3 of content
    total_blocks = len(body_list)
    
    if total_blocks < 3:
        # Too short, just add images at the end
        positions = [total_blocks, total_blocks + 1]
    else:
        pos1 = max(1, total_blocks // 3)
        pos2 = max(2, (total_blocks * 2) // 3)
        positions = [pos1, pos2]
    
    # Create image blocks
    image_block_1 = {
        'type': 'image',
        'value': {
            'image': image1.id,
            'caption': '',
            'alt_text': image1.title
        },
        'id': str(uuid.uuid4())
    }
    
    image_block_2 = {
        'type': 'image',
        'value': {
            'image': image2.id,
            'caption': '',
            'alt_text': image2.title
        },
        'id': str(uuid.uuid4())
    }
    
    # Insert images (insert second one first to maintain correct positions)
    body_list.insert(positions[1], image_block_2)
    body_list.insert(positions[0], image_block_1)
    
    return body_list

def main():
    print('=== TILFØJER 2 BILLEDER TIL HVER ARTIKEL ===\n')
    
    # Create temp directory
    os.makedirs('/Users/mikkelfunder/Marketingnyt.dk/media/temp_images', exist_ok=True)
    
    # Download all images first
    print('Downloader billeder fra Unsplash...\n')
    downloaded_images = {}
    
    for category, images in CATEGORY_IMAGES.items():
        print(f'Kategori: {category}')
        downloaded_images[category] = []
        
        for idx, (url, title) in enumerate(images, 1):
            filename = f'{category.lower().replace(" ", "_").replace("&", "and")}_{idx}.jpg'
            filepath = download_image(url, filename)
            
            if filepath:
                image = upload_to_wagtail(filepath, title)
                if image:
                    downloaded_images[category].append(image)
        
        print()
    
    # Now update articles
    print('\n=== OPDATERER ARTIKLER MED BILLEDER ===\n')
    
    articles = ArticlePage.objects.filter(live=True).exclude(category__slug='podcasts')
    
    for article in articles:
        category_name = article.category.name
        
        if category_name not in downloaded_images:
            print(f'✗ {article.title[:50]}... → Ingen billeder for kategori {category_name}')
            continue
        
        images = downloaded_images[category_name]
        if len(images) < 2:
            print(f'✗ {article.title[:50]}... → Ikke nok billeder (kun {len(images)})')
            continue
        
        # Insert images into body
        new_body = insert_images_into_body(article.body.raw_data, images[0], images[1])
        
        if new_body:
            article.body = new_body
            revision = article.save_revision()
            revision.publish()
            print(f'✓ {article.title[:50]}... → Tilføjet 2 billeder')
        else:
            print(f'✗ {article.title[:50]}... → Kunne ikke opdatere body')
    
    print('\n=== FÆRDIG! ===')

if __name__ == '__main__':
    main()

