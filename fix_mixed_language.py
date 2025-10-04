"""
Fix all mixed Danish/English text in articles
"""

from news.models import ArticlePage
import re

print('=== FIXING MIXED DANISH/ENGLISH ===\n')

# Comprehensive translation dictionary
translations = {
    # Common mixed phrases
    'highly impacts': 'har stor indflydelse på',
    'purchase decisions': 'købsbeslutninger',
    'consumers stoler': 'forbrugere stoler',
    'traditional ads': 'traditionel annoncering',
    'privacy ændringer': 'privatlivsændringer',
    'marketers tænke': 'marketingfolk tænke',
    'Broad Targeting': 'Bred targeting',
    'Creative Testing': 'Kreativ testning',
    'Video-First Approach': 'Video-først tilgang',
    'Video content performer': 'Video indhold performer',
    'statiske billeder': 'statiske billeder',
    'User Generated Content': 'Bruger-genereret indhold',
    'Conversion API Implementation': 'Conversion API implementering',
    'Server-side tracking': 'Server-side tracking',
    'Retention Campaigns': 'Fastholdelseskampagner',
    'email lists': 'email lister',
    'custom audiences': 'tilpassede målgrupper',
    
    # More English phrases
    'tracking implementation': 'tracking implementering',
    'audience research': 'målgruppeanalyse',
    'competitive analysis': 'konkurrentanalyse',
    'goal setting': 'målsætning',
    'KPI definition': 'KPI definition',
    'Best practices for launch': 'Best practices for lancering',
    'Start small og scale': 'Start småt og skalér',
    'winning formulas': 'vindende formler',
    'proper tracking': 'ordentlig tracking',
    'gut feeling': 'mavefornemmelse',
    'personlige præferencer': 'personlige præferencer',
    'Random testing': 'Tilfældig testning',
    'test roadmap': 'test køreplan',
    'audience targeting': 'målgruppetargeting',
    'website tracking': 'hjemmeside tracking',
    'user behavior analysis': 'brugeradfærdsanalyse',
    'product analytics': 'produkt analytics',
    'Data Studio': 'Data Studio',
    'advanced experimentation': 'avanceret eksperimentering',
    'conversion optimization': 'konverteringsoptimering',
    'workflow automation': 'workflow automatisering',
    'complex automations': 'komplekse automatiseringer',
    'native platform automation features': 'native platform automatiseringsfunktioner',
    'clear KPIs': 'klare KPIs',
    'brand awareness': 'brand awareness',
    'efficiency metrics': 'effektivitets metrics',
    'Quick check': 'Hurtig tjek',
    'key metrics': 'nøgle metrics',
    'Detailed performance review': 'Detaljeret performance gennemgang',
    'performance gennemgang': 'performance gennemgang',
    'Comprehensive analysis': 'Omfattende analyse',
    'strategy adjustments': 'strategi justeringer',
    'Big picture review': 'Overordnet gennemgang',
    'planning': 'planlægning',
    'nuværende setup': 'nuværende opsætning',
    'identificér gaps': 'identificér huller',
    'clear goals': 'klare mål',
    'fokuseret campaign': 'fokuseret kampagne',
    'Measure, learn, og iterate': 'Mål, lær og iterér',
    'konsistent execution': 'konsistent eksekvering',
    'kontinuerlig forbedring': 'kontinuerlig forbedring',
    'Start small, test ofte': 'Start småt, test ofte',
    'scale hvad der virker': 'skalér hvad der virker',
    
    # Technical terms that should stay in English but be used correctly
    'iOS 14.5+': 'iOS 14.5+',
    'Facebook Ads': 'Facebook Ads',
    'Google Analytics': 'Google Analytics',
    'Hotjar': 'Hotjar',
    'Mixpanel': 'Mixpanel',
    'Tableau': 'Tableau',
    'Google Optimize': 'Google Optimize',
    'Optimizely': 'Optimizely',
    'VWO': 'VWO',
    'Zapier': 'Zapier',
    'Make': 'Make',
    'Integromat': 'Integromat',
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
            
            # Apply all translations
            for eng, dan in translations.items():
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
        print(f'✓ {article.title[:60]}...')

print(f'\n=== DONE! {fixed_count} articles fixed ===')

