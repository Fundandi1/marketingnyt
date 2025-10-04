import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketingnyt.settings.dev')
django.setup()

from wagtail.models import Page, Site
from news.models import HomePage
from wagtail.rich_text import RichText

# Get the home page
home_page = HomePage.objects.first()
if not home_page:
    print("❌ Home page not found")
    exit()

# Define pages to create
pages_to_create = [
    {
        'title': 'Om os',
        'slug': 'om-os',
        'content': '''
        <h2>Om MarketingNyt.dk</h2>
        <p>MarketingNyt.dk er Danmarks førende nyhedssite for digital marketing. Vi leverer daglige nyheder, analyser og guides inden for:</p>
        <ul>
            <li>SEO og søgemaskineoptimering</li>
            <li>Paid Social (Facebook Ads, Instagram Ads, LinkedIn Ads)</li>
            <li>Google Ads og PPC</li>
            <li>Content Marketing</li>
            <li>Conversion Rate Optimization (CRO)</li>
            <li>AI & Marketing Automation</li>
        </ul>
        <p>Vores mission er at holde danske marketingfolk opdaterede med de seneste trends, strategier og best practices.</p>
        '''
    },
    {
        'title': 'Kontakt',
        'slug': 'kontakt',
        'content': '''
        <h2>Kontakt os</h2>
        <p>Har du spørgsmål, forslag eller vil du bidrage med indhold til MarketingNyt.dk?</p>
        <p><strong>Email:</strong> kontakt@marketingnyt.dk</p>
        <p><strong>Følg os på sociale medier:</strong></p>
        <ul>
            <li>Facebook: facebook.com/marketingnyt</li>
            <li>LinkedIn: linkedin.com/company/marketingnyt</li>
            <li>Instagram: instagram.com/marketingnyt</li>
        </ul>
        '''
    },
    {
        'title': 'Cookiepolitik',
        'slug': 'cookiepolitik',
        'content': '''
        <h2>Cookiepolitik</h2>
        <p>MarketingNyt.dk bruger cookies til at forbedre din brugeroplevelse og analysere trafik på sitet.</p>
        <h3>Hvad er cookies?</h3>
        <p>Cookies er små tekstfiler, der gemmes på din computer eller mobilenhed, når du besøger et website.</p>
        <h3>Hvilke cookies bruger vi?</h3>
        <ul>
            <li><strong>Nødvendige cookies:</strong> Sikrer at websitet fungerer korrekt</li>
            <li><strong>Analytiske cookies:</strong> Hjælper os med at forstå hvordan besøgende bruger sitet</li>
            <li><strong>Marketing cookies:</strong> Bruges til at vise relevante annoncer</li>
        </ul>
        <h3>Sådan administrerer du cookies</h3>
        <p>Du kan til enhver tid slette eller blokere cookies i din browsers indstillinger.</p>
        '''
    },
    {
        'title': 'Privatlivspolitik',
        'slug': 'privatlivspolitik',
        'content': '''
        <h2>Privatlivspolitik</h2>
        <p>MarketingNyt.dk respekterer dit privatliv og beskytter dine personlige oplysninger.</p>
        <h3>Hvilke data indsamler vi?</h3>
        <ul>
            <li>Email adresse (hvis du tilmelder dig nyhedsbrev)</li>
            <li>Anonyme brugsdata via Google Analytics</li>
            <li>IP-adresse og browserinformation</li>
        </ul>
        <h3>Hvordan bruger vi dine data?</h3>
        <p>Vi bruger dine data til at:</p>
        <ul>
            <li>Sende dig nyhedsbreve (kun hvis du har tilmeldt dig)</li>
            <li>Forbedre vores website og indhold</li>
            <li>Analysere trafik og brugeradfærd</li>
        </ul>
        <h3>Dine rettigheder</h3>
        <p>Du har ret til at:</p>
        <ul>
            <li>Få indsigt i hvilke data vi har om dig</li>
            <li>Få dine data slettet</li>
            <li>Framelde dig nyhedsbreve</li>
        </ul>
        <p>Kontakt os på kontakt@marketingnyt.dk for at udøve dine rettigheder.</p>
        '''
    },
    {
        'title': 'Handelsbetingelser',
        'slug': 'handelsbetingelser',
        'content': '''
        <h2>Handelsbetingelser</h2>
        <p>Sidst opdateret: Januar 2025</p>
        <h3>Brug af website</h3>
        <p>Ved at bruge MarketingNyt.dk accepterer du disse handelsbetingelser.</p>
        <h3>Indhold og ophavsret</h3>
        <p>Alt indhold på MarketingNyt.dk er beskyttet af ophavsret. Du må ikke kopiere, distribuere eller genbruge indhold uden tilladelse.</p>
        <h3>Links til eksterne websites</h3>
        <p>MarketingNyt.dk indeholder links til eksterne websites. Vi er ikke ansvarlige for indholdet på disse websites.</p>
        <h3>Ansvarsfraskrivelse</h3>
        <p>Informationen på MarketingNyt.dk er til generel information. Vi garanterer ikke for nøjagtigheden eller fuldstændigheden af informationen.</p>
        '''
    }
]

print('=== OPRETTER FOOTER SIDER ===\n')

for page_data in pages_to_create:
    # Check if page already exists
    existing = Page.objects.filter(slug=page_data['slug']).first()
    if existing:
        print(f'⚠️  Side eksisterer allerede: {page_data["title"]} ({page_data["slug"]})')
        continue
    
    # Create new page
    from wagtail.models import Page as WagtailPage
    
    page = WagtailPage(
        title=page_data['title'],
        slug=page_data['slug'],
        show_in_menus=True,
    )
    
    # Add as child of home page
    home_page.add_child(instance=page)
    
    # Publish the page
    revision = page.save_revision()
    revision.publish()
    
    print(f'✅ Oprettet: {page_data["title"]} - /{page_data["slug"]}/')

print('\n=== FÆRDIG ===')
print('Alle footer sider er oprettet!')

