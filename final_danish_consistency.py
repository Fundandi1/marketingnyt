import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketingnyt.settings.dev')
django.setup()

from news.models import ArticlePage

# Comprehensive translation - translate common English words but keep industry terms
TRANSLATIONS = {
    # Common English words that should be Danish
    'Ægte people': 'Ægte mennesker',
    'ægte people': 'ægte mennesker',
    'Ægte experiences': 'Ægte oplevelser',
    'ægte experiences': 'ægte oplevelser',
    ' people': ' mennesker',
    ' People': ' Mennesker',
    ' experiences': ' oplevelser',
    ' Experiences': ' Oplevelser',
    ' customers': ' kunder',
    ' Customers': ' Kunder',
    ' customer': ' kunde',
    ' Customer': ' Kunde',
    
    # Action words
    'Spørg direkte': 'Spørg direkte',
    'Gør det nemt': 'Gør det nemt',
    'Create campaigns': 'Lav kampagner',
    'create campaigns': 'lav kampagner',
    'Showcase existing': 'Vis eksisterende',
    'showcase existing': 'vis eksisterende',
    
    # Common phrases
    'Use cases:': 'Anvendelser:',
    'use cases:': 'anvendelser:',
    'Bedste praksis:': 'Bedste praksis:',
    'Best practices:': 'Bedste praksis:',
    'best practices:': 'bedste praksis:',
    'Timing:': 'Timing:',
    'timing:': 'timing:',
    'Messaging:': 'Besked:',
    'messaging:': 'besked:',
    'Tactics:': 'Taktikker:',
    'tactics:': 'taktikker:',
    'Campaign types:': 'Kampagne typer:',
    'campaign types:': 'kampagne typer:',
    'Format:': 'Format:',
    'format:': 'format:',
    'Formats:': 'Formater:',
    'formats:': 'formater:',
    'Process:': 'Proces:',
    'process:': 'proces:',
    'Email types:': 'Email typer:',
    'email types:': 'email typer:',
    'Volume metrics:': 'Volumen målinger:',
    'volume metrics:': 'volumen målinger:',
    'Engagement metrics:': 'Engagement målinger:',
    'engagement metrics:': 'engagement målinger:',
    'Business metrics:': 'Forretnings målinger:',
    'business metrics:': 'forretnings målinger:',
    
    # Specific mixed phrases
    'Post-purchase email': 'Email efter køb',
    'post-purchase email': 'email efter køb',
    'After positive support interaction': 'Efter positiv support interaktion',
    'after positive support interaction': 'efter positiv support interaktion',
    'When customer shares success': 'Når kunde deler succes',
    'when customer shares success': 'når kunde deler succes',
    'Discount på næste køb': 'Rabat på næste køb',
    'discount på næste køb': 'rabat på næste køb',
    'Entry i giveaway': 'Deltagelse i konkurrence',
    'entry i giveaway': 'deltagelse i konkurrence',
    'Feature på din Instagram': 'Fremhævning på din Instagram',
    'feature på din Instagram': 'fremhævning på din Instagram',
    'Exclusive access': 'Eksklusiv adgang',
    'exclusive access': 'eksklusiv adgang',
    'Loyalty points': 'Loyalitetspoint',
    'loyalty points': 'loyalitetspoint',
    
    # More mixed phrases
    'Branded hashtag': 'Branded hashtag',
    'branded hashtag': 'branded hashtag',
    'Email template': 'Email skabelon',
    'email template': 'email skabelon',
    'Photo upload': 'Foto upload',
    'photo upload': 'foto upload',
    'Social media tagging': 'Social media tagging',
    'social media tagging': 'social media tagging',
    'Repost på Instagram': 'Genpost på Instagram',
    'repost på Instagram': 'genpost på Instagram',
    'Feature på website': 'Fremhæv på website',
    'feature på website': 'fremhæv på website',
    'Include i email': 'Inkluder i email',
    'include i email': 'inkluder i email',
    'Use i ads': 'Brug i annoncer',
    'use i ads': 'brug i annoncer',
    
    # Content types
    'Customer photos': 'Kunde fotos',
    'customer photos': 'kunde fotos',
    'Customer photo': 'Kunde foto',
    'customer photo': 'kunde foto',
    'Video testimonials': 'Video anmeldelser',
    'video testimonials': 'video anmeldelser',
    'Reviews & ratings': 'Anmeldelser & ratings',
    'reviews & ratings': 'anmeldelser & ratings',
    'Unboxing videos': 'Unboxing videoer',
    'unboxing videos': 'unboxing videoer',
    'How-to content': 'Hvordan-gør-du content',
    'how-to content': 'hvordan-gør-du content',
    
    # Tools and platforms
    'Collection tools': 'Indsamlings værktøjer',
    'collection tools': 'indsamlings værktøjer',
    'Rights management': 'Rettigheds håndtering',
    'rights management': 'rettigheds håndtering',
    
    # Marketing terms
    'Social media ads': 'Social media annoncer',
    'social media ads': 'social media annoncer',
    'Product pages': 'Produkt sider',
    'product pages': 'produkt sider',
    'Email campaigns': 'Email kampagner',
    'email campaigns': 'email kampagner',
    'Website homepage': 'Website forside',
    'website homepage': 'website forside',
    
    # Metrics
    'Conversion rate': 'Konverteringsrate',
    'conversion rate': 'konverteringsrate',
    'Engagement rate': 'Engagement rate',
    'engagement rate': 'engagement rate',
    'Customer acquisition cost': 'Kunde anskaffelses omkostning',
    'customer acquisition cost': 'kunde anskaffelses omkostning',
    
    # Case study terms
    'Fashion brand': 'Mode brand',
    'fashion brand': 'mode brand',
    'Brand-created content': 'Brand-skabt indhold',
    'brand-created content': 'brand-skabt indhold',
    'Brand content': 'Brand indhold',
    'brand content': 'brand indhold',
    'Brand ads': 'Brand annoncer',
    'brand ads': 'brand annoncer',
    
    # Actions
    'Start med at create': 'Start med at lave',
    'start med at create': 'start med at lave',
    'Mål impact': 'Mål effekt',
    'mål impact': 'mål effekt',
    
    # Other common mixed phrases
    'Shows product in use': 'Viser produkt i brug',
    'shows product in use': 'viser produkt i brug',
    'Mentions specific results': 'Nævner specifikke resultater',
    'mentions specific results': 'nævner specifikke resultater',
    'Show both positive and negative': 'Vis både positive og negative',
    'show both positive and negative': 'vis både positive og negative',
    'Highlight most helpful': 'Fremhæv mest hjælpsomme',
    'highlight most helpful': 'fremhæv mest hjælpsomme',
    'Beautiful packaging': 'Smuk emballage',
    'beautiful packaging': 'smuk emballage',
    'Surprise gifts': 'Overraskelses gaver',
    'surprise gifts': 'overraskelses gaver',
    
    # More specific phrases
    'Encourage med:': 'Tilskynd med:',
    'encourage med:': 'tilskynd med:',
    'Encourage detailed': 'Tilskynd detaljerede',
    'encourage detailed': 'tilskynd detaljerede',
    'Respond til alle': 'Svar på alle',
    'respond til alle': 'svar på alle',
    
    # Ad-related
    'Outperform stock photos': 'Performer bedre end stock fotos',
    'outperform stock photos': 'performer bedre end stock fotos',
    'Outperform brand-created ads': 'Performer bedre end brand-skabte annoncer',
    'outperform brand-created ads': 'performer bedre end brand-skabte annoncer',
    
    # Specific UGC phrases
    'Peer recommendations': 'Anbefalinger fra ligesindede',
    'peer recommendations': 'anbefalinger fra ligesindede',
    'Cost-effective': 'Omkostningseffektivt',
    'cost-effective': 'omkostningseffektivt',
    'Scalable': 'Skalerbart',
    'scalable': 'skalerbart',
    
    # Additional translations for consistency
    ' pieces': ' stykker',
    ' Pieces': ' Stykker',
    ' users': ' brugere',
    ' Users': ' Brugere',
    ' claims': ' påstande',
    ' Claims': ' Påstande',
    ' questions': ' spørgsmål',
    ' Questions': ' Spørgsmål',
    'Specific questions': 'Specifikke spørgsmål',
    'specific questions': 'specifikke spørgsmål',
    'Specific results': 'Specifikke resultater',
    'specific results': 'specifikke resultater',

    # Keep these as-is (industry standard terms)
    # 'UGC', 'ROAS', 'CTA', 'CPC', 'CPA', 'ROI', 'SEO', 'SaaS', etc.
}

print('=== RETTER ALLE ARTIKLER TIL KONSISTENT DANSK ===\n')

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
                content = content.replace(english, danish)
            
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

