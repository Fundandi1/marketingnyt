"""
Translate all English text in articles to Danish
"""

from news.models import ArticlePage
import re

print('=== TRANSLATING ENGLISH TO DANISH ===\n')

# Translation mappings
translations = {
    # Headers
    'Implementation roadmap': 'Implementeringsplan',
    'Common mistakes at undgå': 'Almindelige fejl at undgå',
    'Common mistakes': 'Almindelige fejl',
    'Tools og resources': 'Værktøjer og ressourcer',
    'Analytics tools': 'Analyse værktøjer',
    'Testing tools': 'Test værktøjer',
    'Automation tools': 'Automatiserings værktøjer',
    'Key Performance Indicators': 'Nøgle Performance Indikatorer',
    'Reporting cadence': 'Rapporterings kadence',
    
    # Time periods
    'Daily:': 'Dagligt:',
    'Weekly:': 'Ugentligt:',
    'Monthly:': 'Månedligt:',
    'Quarterly:': 'Kvartalsvis:',
    
    # Common phrases
    'Best practices': 'Best practices',
    'Use case': 'Anvendelsestilfælde',
    'Use cases': 'Anvendelsestilfælde',
    'ROI': 'ROI',
    'CTA': 'CTA',
    'CTAs': 'CTAs',
    'CPA': 'CPA',
    'CPM': 'CPM',
    'CTR': 'CTR',
    'ROAS': 'ROAS',
    'KPI': 'KPI',
    'KPIs': 'KPIs',
    'A/B testing': 'A/B testing',
    'SEO': 'SEO',
    'UGC': 'UGC',
    'API': 'API',
    
    # Phases
    'Fase 1: Foundation': 'Fase 1: Fundament',
    'Fase 2: Launch': 'Fase 2: Lancering',
    'Fase 3: Optimization': 'Fase 3: Optimering',
    'Fase 4: Scale': 'Fase 4: Skalering',
    
    # Specific phrases
    'Optimization fokus områder:': 'Optimerings fokusområder:',
    'Scaling strategier:': 'Skalerings strategier:',
    'Quick check': 'Hurtig tjek',
    'Detailed performance review': 'Detaljeret performance gennemgang',
    'Comprehensive analysis': 'Omfattende analyse',
    'Big picture review': 'Overordnet gennemgang',
    'Primary KPI': 'Primær KPI',
    'Secondary KPIs': 'Sekundære KPIs',
    'Efficiency metrics': 'Effektivitets metrics',
}

# Additional context-specific translations
context_translations = {
    'Start med limited budget': 'Start med begrænset budget',
    'setup proper tracking': 'opsæt ordentlig tracking',
    'Pause underperforming elements': 'Pause underperformerende elementer',
    'scale top performers': 'skalér top performere',
    'test nye variationer': 'test nye variationer',
    'refine targeting': 'forfin targeting',
    'adjust budgets baseret på performance': 'justér budgets baseret på performance',
}

fixed_count = 0
articles = ArticlePage.objects.filter(live=True).exclude(category__slug='podcasts')

for article in articles:
    body_list = list(article.body.raw_data) if article.body else []
    
    # Check if article has English text
    content = ' '.join([b.get('value', '') for b in body_list if b.get('type') == 'rich_text'])
    
    has_english = any(eng in content for eng in ['Implementation roadmap', 'Common mistakes', 'Analytics tools', 'Testing tools'])
    
    if not has_english:
        continue
    
    print(f'{article.title[:60]}...')
    
    # Translate each rich_text block
    modified = False
    for i, block in enumerate(body_list):
        if block.get('type') == 'rich_text':
            original_value = block.get('value', '')
            translated_value = original_value
            
            # Apply all translations
            for eng, dan in translations.items():
                if eng in translated_value:
                    translated_value = translated_value.replace(eng, dan)
                    modified = True
            
            # Apply context translations
            for eng, dan in context_translations.items():
                if eng in translated_value:
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
        print(f'  ✓ Translated to Danish')
    else:
        print(f'  - No changes needed')

print(f'\n=== DONE! {fixed_count} articles translated ===')

