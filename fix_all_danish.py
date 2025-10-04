import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketingnyt.settings.dev')
django.setup()

from news.models import ArticlePage

# Comprehensive translation dictionary for headlines and content
TRANSLATIONS = {
    # Headlines - English to Danish
    'A/B testing': 'A/B testning',
    'A/B Testing': 'A/B Testning',
    'split testing': 'split testning',
    'Split Testing': 'Split Testning',
    'Landing Page Optimization': 'Landing Page Optimering',
    'Landing page optimization': 'Landing page optimering',
    'Checkout Optimization': 'Checkout Optimering',
    'checkout optimization': 'checkout optimering',
    'Mobile CRO': 'Mobil CRO',
    'mobile CRO': 'mobil CRO',
    'Conversion Copywriting': 'Konverterings Copywriting',
    'conversion copywriting': 'konverterings copywriting',
    'Trust Signals': 'Tillidssignaler',
    'trust signals': 'tillidssignaler',
    'Performance Max': 'Performance Max',
    'performance max': 'performance max',
    'Google Ads Keyword Strategy': 'Google Ads Søgeordsstrategi',
    'Meta Ads': 'Meta Annoncer',
    'meta ads': 'meta annoncer',
    'TikTok Ads': 'TikTok Annoncer',
    'tiktok ads': 'tiktok annoncer',
    'Community Marketing': 'Community Marketing',
    'community marketing': 'community marketing',
    'Content Repurposing': 'Indhold Genbrug',
    'content repurposing': 'indhold genbrug',
    'SEO Content Strategy': 'SEO Indhold Strategi',
    'seo content strategy': 'seo indhold strategi',
    'Video Marketing': 'Video Marketing',
    'video marketing': 'video marketing',
    
    # Common mixed phrases in content
    'Høj impact tests': 'Tests med høj effekt',
    'høj impact tests': 'tests med høj effekt',
    'høj impact': 'høj effekt',
    'Høj impact': 'Høj effekt',
    'Medium impact tests': 'Tests med medium effekt',
    'medium impact tests': 'tests med medium effekt',
    'Step 1:': 'Trin 1:',
    'Step 2:': 'Trin 2:',
    'Step 3:': 'Trin 3:',
    'Step 4:': 'Trin 4:',
    'Step 5:': 'Trin 5:',
    'Mistake #1:': 'Fejl #1:',
    'Mistake #2:': 'Fejl #2:',
    'Mistake #3:': 'Fejl #3:',
    'Mistake #4:': 'Fejl #4:',
    'Mistake #5:': 'Fejl #5:',
    'Face-bog': 'Facebook',
    'Common mistakes': 'Almindelige fejl',
    'common mistakes': 'almindelige fejl',
    'Best practices': 'Bedste praksis',
    'best practices': 'bedste praksis',
    'Success metrics': 'Succesmålinger',
    'success metrics': 'succesmålinger',
    'Sample size': 'Stikprøvestørrelse',
    'sample size': 'stikprøvestørrelse',
    'Testing kultur': 'Test kultur',
    'testing kultur': 'test kultur',
    'Test roadmap': 'Test køreplan',
    'test roadmap': 'test køreplan',
    'Learning library': 'Læringsbibliotek',
    'learning library': 'læringsbibliotek',
    'Celebrate failures': 'Fejr fejl',
    'celebrate failures': 'fejr fejl',
    'Compound wins': 'Sammensatte gevinster',
    'compound wins': 'sammensatte gevinster',
    'Weekly gennemgangs': 'Ugentlige gennemgange',
    'weekly gennemgangs': 'ugentlige gennemgange',
    
    # Technical terms that should be translated
    'Hero images/video': 'Hovedbilleder/video',
    'hero images/video': 'hovedbilleder/video',
    'Pricing display': 'Prisvisning',
    'pricing display': 'prisvisning',
    'Form length': 'Formular længde',
    'form length': 'formular længde',
    'Social proof type': 'Social bevis type',
    'social proof type': 'social bevis type',
    'Copy length': 'Tekst længde',
    'copy length': 'tekst længde',
    'Visual hierarchy': 'Visuel hierarki',
    'visual hierarchy': 'visuel hierarki',
    'White space': 'Hvidt rum',
    'white space': 'hvidt rum',
    'CTA knaps': 'CTA knapper',
    'CTA-knap': 'CTA-knap',
    'Click-through rate': 'Klikrate',
    'click-through rate': 'klikrate',
    'Bounce rate': 'Afvisningsrate',
    'bounce rate': 'afvisningsrate',
    'Time on site': 'Tid på siden',
    'time on site': 'tid på siden',
    'Baseline konverteringsrate': 'Baseline konverteringsrate',
    'baseline konverteringsrate': 'baseline konverteringsrate',
    'Statistical significance': 'Statistisk signifikans',
    'statistical significance': 'statistisk signifikans',
    'Statistical power': 'Statistisk styrke',
    'statistical power': 'statistisk styrke',
    'Business cycle': 'Forretningscyklus',
    'business cycle': 'forretningscyklus',
    'Planned sample size': 'Planlagt stikprøvestørrelse',
    'planned sample size': 'planlagt stikprøvestørrelse',
    'P-value': 'P-værdi',
    'p-value': 'p-værdi',
    
    # Tool names and categories
    'Enterprise:': 'Enterprise:',
    'Mid-market:': 'Mellemmarked:',
    'Email:': 'Email:',
    'Ads:': 'Annoncer:',
    'Face-bog Ads Manager': 'Facebook Ads Manager',
    
    # Common English words that slip through
    'Prioriteret liste': 'Prioriteret liste',
    'start her': 'start her',
    'Tommelfingerregel:': 'Tommelfingerregel:',
    'Minimum varighed:': 'Minimum varighed:',
    'Fuld business cycle:': 'Fuld forretningscyklus:',
    'Stop ALDRIG': 'Stop ALDRIG',
    'Vent til': 'Vent til',
    'Tjek om': 'Tjek om',
    'built-in': 'indbygget',
    'Built-in': 'Indbygget',
}

print('=== RETTER ALLE ARTIKLER TIL RENT DANSK ===\n')

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
            
            # Apply all translations
            for english, danish in TRANSLATIONS.items():
                # Use word boundaries for whole word replacement
                pattern = r'\b' + re.escape(english) + r'\b'
                content = re.sub(pattern, danish, content, flags=re.IGNORECASE)
            
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

