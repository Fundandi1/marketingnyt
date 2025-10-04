"""
Restructure all articles to have better visual flow:
OLD: Rich text, Image, Image
NEW: Rich text, Image, Rich text, Image, Rich text
"""

from news.models import ArticlePage
import uuid

print('=== RESTRUCTURING ALL ARTICLES ===\n')

articles = ArticlePage.objects.filter(live=True).exclude(category__slug='podcasts')
restructured_count = 0

for article in articles:
    body_list = list(article.body.raw_data) if article.body else []
    
    # Separate rich_text blocks and images
    rich_text_blocks = [b for b in body_list if b.get('type') == 'rich_text']
    image_blocks = [b for b in body_list if b.get('type') == 'image']
    
    # Check if restructuring is needed
    if len(rich_text_blocks) > 0 and len(image_blocks) >= 2:
        # Split rich text content into sections
        # If we have 1 rich_text block, split it into 3 sections
        # If we have multiple, use them as-is
        
        if len(rich_text_blocks) == 1:
            # Split the single rich text block into 3 parts
            content = rich_text_blocks[0].get('value', '')
            
            # Split by paragraphs
            paragraphs = content.split('</p>')
            paragraphs = [p + '</p>' for p in paragraphs if p.strip()]
            
            if len(paragraphs) >= 3:
                # Divide paragraphs into 3 sections
                total = len(paragraphs)
                section1_end = max(1, total // 3)
                section2_end = max(2, (total * 2) // 3)
                
                section1 = ''.join(paragraphs[:section1_end])
                section2 = ''.join(paragraphs[section1_end:section2_end])
                section3 = ''.join(paragraphs[section2_end:])
                
                # Create new rich_text blocks
                new_rich_text_blocks = [
                    {
                        'type': 'rich_text',
                        'value': section1,
                        'id': rich_text_blocks[0]['id']
                    },
                    {
                        'type': 'rich_text',
                        'value': section2,
                        'id': str(uuid.uuid4())
                    },
                    {
                        'type': 'rich_text',
                        'value': section3,
                        'id': str(uuid.uuid4())
                    }
                ]
            else:
                # Not enough paragraphs to split, keep as-is
                new_rich_text_blocks = rich_text_blocks
        else:
            # Use existing rich_text blocks
            new_rich_text_blocks = rich_text_blocks
        
        # Build new structure: Rich text, Image, Rich text, Image, Rich text
        new_body = []
        
        if len(new_rich_text_blocks) >= 3 and len(image_blocks) >= 2:
            # Perfect case: 3 text sections, 2 images
            new_body.append(new_rich_text_blocks[0])
            new_body.append(image_blocks[0])
            new_body.append(new_rich_text_blocks[1])
            new_body.append(image_blocks[1])
            new_body.append(new_rich_text_blocks[2])
            
            # Add any remaining text blocks
            for i in range(3, len(new_rich_text_blocks)):
                new_body.append(new_rich_text_blocks[i])
        elif len(new_rich_text_blocks) >= 2 and len(image_blocks) >= 2:
            # 2 text sections, 2 images
            new_body.append(new_rich_text_blocks[0])
            new_body.append(image_blocks[0])
            new_body.append(new_rich_text_blocks[1])
            new_body.append(image_blocks[1])
            
            # Add any remaining text blocks
            for i in range(2, len(new_rich_text_blocks)):
                new_body.append(new_rich_text_blocks[i])
        else:
            # Fallback: interleave as much as possible
            max_pairs = min(len(new_rich_text_blocks), len(image_blocks))
            for i in range(max_pairs):
                new_body.append(new_rich_text_blocks[i])
                new_body.append(image_blocks[i])
            
            # Add remaining text blocks
            for i in range(max_pairs, len(new_rich_text_blocks)):
                new_body.append(new_rich_text_blocks[i])
        
        # Update article
        article.body = new_body
        revision = article.save_revision()
        revision.publish()
        restructured_count += 1
        print(f'✓ {article.title[:50]}... → Restructured ({len(new_rich_text_blocks)} text sections, {len(image_blocks)} images)')

print(f'\n=== DONE! {restructured_count} articles restructured ===')

