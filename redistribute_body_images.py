"""
Redistribute existing images so each article has 2 unique images in body
"""

from news.models import ArticlePage
from wagtail.images.models import Image
import random

print('=== REDISTRIBUTING BODY IMAGES ===\n')

# Get all available images (excluding cover images)
all_images = list(Image.objects.all().values_list('id', flat=True))
print(f'Total images available: {len(all_images)}')

# Get all articles
articles = list(ArticlePage.objects.filter(live=True).exclude(category__slug='podcasts'))
print(f'Total articles to fix: {len(articles)}\n')

# Shuffle images to ensure random distribution
random.shuffle(all_images)

# Assign 2 unique images to each article
fixed_count = 0
image_index = 0

for article in articles:
    print(f'{article.title[:50]}...')
    
    # Get current body
    body_list = list(article.body.raw_data) if article.body else []
    
    # Find image blocks
    image_blocks = [(i, b) for i, b in enumerate(body_list) if b.get('type') == 'image']
    
    if len(image_blocks) < 2:
        print(f'  ⚠️  Only {len(image_blocks)} images, skipping')
        continue
    
    # Get 2 unique images for this article
    img1 = all_images[image_index % len(all_images)]
    image_index += 1
    img2 = all_images[image_index % len(all_images)]
    image_index += 1
    
    # Make sure they're different
    while img1 == img2:
        image_index += 1
        img2 = all_images[image_index % len(all_images)]
    
    # Update first 2 image blocks
    old_img1 = body_list[image_blocks[0][0]]['value']['image']
    old_img2 = body_list[image_blocks[1][0]]['value']['image']
    
    body_list[image_blocks[0][0]]['value']['image'] = img1
    body_list[image_blocks[1][0]]['value']['image'] = img2
    
    # Save article
    article.body = body_list
    revision = article.save_revision()
    revision.publish()
    
    fixed_count += 1
    print(f'  ✓ Updated: Image {old_img1} → {img1}, Image {old_img2} → {img2}')

print(f'\n=== DONE! {fixed_count} articles updated with redistributed images ===')

