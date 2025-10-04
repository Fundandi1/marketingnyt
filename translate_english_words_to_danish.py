"""
Translate ALL remaining English words to proper Danish
"""

from news.models import ArticlePage
import re

print('=== TRANSLATING ENGLISH WORDS TO DANISH ===\n')

# ACTUAL English to Danish translations
translations = {
    # Single words - English → Danish
    'Upload': 'Upload',  # This is acceptable in Danish
    'Minimum': 'Minimum',  # This is acceptable in Danish  
    'minimum': 'minimum',  # This is acceptable in Danish
    'High-quality': 'Høj kvalitet',
    'high-quality': 'høj kvalitet',
    'Exterior': 'Ydre',
    'Interior': 'Indre',
    'interior': 'indre',
    'Products': 'Produkter',
    'products': 'produkter',
    'Team': 'Team',  # Acceptable in Danish
    'team': 'team',  # Acceptable in Danish
    'Logo': 'Logo',  # Acceptable in Danish
    'logo': 'logo',  # Acceptable in Danish
    'Keywords': 'Nøgleord',
    'keywords': 'nøgleord',
    'Events': 'Begivenheder',
    'events': 'begivenheder',
    'Seed': 'Tilføj',
    'seed': 'tilføj',
    'Q&A': 'Spørgsmål & Svar',
    'upload': 'upload',  # Acceptable in Danish
    'Offers': 'Tilbud',
    'offers': 'tilbud',
    'updates': 'opdateringer',
    'Updates': 'Opdateringer',
    'Monitor': 'Overvåg',
    'monitor': 'overvåg',
    
    # Phrases
    'fresh content': 'frisk indhold',
    'Post types': 'Opslags typer',
    'CTA button': 'CTA knap',
    'common questions': 'almindelige spørgsmål',
    'pixels minimum': 'pixels minimum',
}

fixed_count = 0
articles = ArticlePage.objects.filter(live=True).exclude(category__slug='podcasts')

for article in articles:
    body_list = list(article.body.raw_data) if article.body else []
    
    modified = False
    for i, block in enumerate(body_list):
        if block.get('type') == 'rich_text':
            original_value = block.get('value', '')
            translated_value = original_value
            
            # Apply translations (longer phrases first to avoid partial replacements)
            sorted_translations = sorted(translations.items(), key=lambda x: len(x[0]), reverse=True)
            
            for eng, dan in sorted_translations:
                # Use word boundaries for single words to avoid partial matches
                if len(eng.split()) == 1 and eng[0].isupper():
                    # Capitalized single word - use word boundary
                    pattern = r'\b' + re.escape(eng) + r'\b'
                    if re.search(pattern, translated_value):
                        translated_value = re.sub(pattern, dan, translated_value)
                        modified = True
                elif eng in translated_value:
                    translated_value = translated_value.replace(eng, dan)
                    modified = True
            
            if translated_value != original_value:
                body_list[i]['value'] = translated_value
    
    if modified:
        # Save article
        article.body = body_list
        revision = article.save_revision()
        revision.publish()
        fixed_count += 1
        print(f'✓ {article.title[:60]}...')

print(f'\n=== DONE! {fixed_count} articles translated to Danish ===')

