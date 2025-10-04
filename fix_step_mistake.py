import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketingnyt.settings.dev')
django.setup()

from news.models import ArticlePage

print('=== RETTER STEP OG MISTAKE FRASER ===\n')

articles = ArticlePage.objects.filter(live=True).exclude(category__slug='podcasts')
updated_count = 0

for article in articles:
    body_list = list(article.body.raw_data) if article.body else []
    
    if not body_list:
        continue
    
    updated = False
    
    for i, block in enumerate(body_list):
        if block.get('type') == 'rich_text':
            content = block.get('value', '')
            original_content = content
            
            # Replace Step patterns
            for num in range(1, 11):
                content = content.replace(f'Step {num}:', f'Trin {num}:')
                content = content.replace(f'step {num}:', f'trin {num}:')
            
            # Replace Mistake patterns
            for num in range(1, 11):
                content = content.replace(f'Mistake #{num}:', f'Fejl #{num}:')
                content = content.replace(f'mistake #{num}:', f'fejl #{num}:')
            
            if content != original_content:
                body_list[i]['value'] = content
                updated = True
    
    if updated:
        article.body = body_list
        revision = article.save_revision()
        revision.publish()
        updated_count += 1
        print(f'✓ {article.title[:60]}...')

print(f'\n=== FÆRDIG! {updated_count} artikler opdateret ===')

