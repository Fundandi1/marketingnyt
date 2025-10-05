"""
Management command to create legal pages (privacy policy, cookie policy, terms).
"""

from django.core.management.base import BaseCommand
from news.models import BasicPage, HomePage


class Command(BaseCommand):
    help = 'Create legal pages (privacy policy, cookie policy, terms)'

    def handle(self, *args, **options):
        self.stdout.write('Creating legal pages...')
        
        # Get HomePage
        homepage = HomePage.objects.first()
        if not homepage:
            self.stdout.write(self.style.ERROR('HomePage not found. Run setup_content first.'))
            return
        
        # Legal pages data
        legal_pages = [
            {
                'title': 'Privatlivspolitik',
                'slug': 'privatlivspolitik',
                'content': '''
                <h1>Privatlivspolitik</h1>
                <p>Denne privatlivspolitik beskriver, hvordan MarketingNyt.dk indsamler, bruger og beskytter dine personlige oplysninger.</p>
                
                <h2>Hvilke oplysninger indsamler vi?</h2>
                <p>Vi indsamler kun de oplysninger, der er nødvendige for at levere vores tjenester, herunder:</p>
                <ul>
                    <li>E-mailadresse ved nyhedsbrevstilmelding</li>
                    <li>Anonyme brugsstatistikker via Google Analytics</li>
                    <li>Cookies til forbedring af brugeroplevelsen</li>
                </ul>
                
                <h2>Hvordan bruger vi dine oplysninger?</h2>
                <p>Dine oplysninger bruges til:</p>
                <ul>
                    <li>At sende dig vores nyhedsbrev (kun hvis du har tilmeldt dig)</li>
                    <li>At forbedre vores hjemmeside og tjenester</li>
                    <li>At analysere trafik og brugeradfærd anonymt</li>
                </ul>
                
                <h2>Kontakt</h2>
                <p>Har du spørgsmål til vores privatlivspolitik, kan du kontakte os på info@marketingnyt.dk</p>
                '''
            },
            {
                'title': 'Cookiepolitik',
                'slug': 'cookiepolitik',
                'content': '''
                <h1>Cookiepolitik</h1>
                <p>MarketingNyt.dk bruger cookies for at forbedre din oplevelse på vores hjemmeside.</p>
                
                <h2>Hvad er cookies?</h2>
                <p>Cookies er små tekstfiler, der gemmes på din computer eller mobile enhed, når du besøger en hjemmeside.</p>
                
                <h2>Hvilke cookies bruger vi?</h2>
                <ul>
                    <li><strong>Nødvendige cookies:</strong> Sikrer grundlæggende funktionalitet</li>
                    <li><strong>Analytiske cookies:</strong> Google Analytics til at forstå, hvordan besøgende bruger siden</li>
                    <li><strong>Funktionelle cookies:</strong> Husker dine præferencer</li>
                </ul>
                
                <h2>Hvordan administrerer du cookies?</h2>
                <p>Du kan til enhver tid slette eller blokere cookies gennem din browsers indstillinger.</p>
                
                <h2>Kontakt</h2>
                <p>Har du spørgsmål til vores cookiepolitik, kan du kontakte os på info@marketingnyt.dk</p>
                '''
            },
            {
                'title': 'Handelsbetingelser',
                'slug': 'handelsbetingelser',
                'content': '''
                <h1>Handelsbetingelser</h1>
                <p>Disse handelsbetingelser gælder for brugen af MarketingNyt.dk</p>
                
                <h2>Brug af hjemmesiden</h2>
                <p>Ved at bruge MarketingNyt.dk accepterer du disse betingelser. Hjemmesiden er gratis at bruge til personlige og kommercielle formål.</p>
                
                <h2>Indhold</h2>
                <p>Alt indhold på MarketingNyt.dk er beskyttet af ophavsret. Du må gerne dele og citere vores artikler med korrekt kildeangivelse.</p>
                
                <h2>Ansvarsfraskrivelse</h2>
                <p>MarketingNyt.dk stræber efter at levere korrekte og opdaterede informationer, men kan ikke garantere for indholdet.</p>
                
                <h2>Ændringer</h2>
                <p>Vi forbeholder os retten til at ændre disse betingelser til enhver tid.</p>
                
                <h2>Kontakt</h2>
                <p>Har du spørgsmål til vores handelsbetingelser, kan du kontakte os på info@marketingnyt.dk</p>
                '''
            }
        ]
        
        # Create legal pages
        for page_data in legal_pages:
            try:
                # Check if page already exists
                existing_page = BasicPage.objects.filter(slug=page_data['slug']).first()
                if existing_page:
                    self.stdout.write(f'Page "{page_data["title"]}" already exists')
                    continue
                
                # Create new page
                legal_page = BasicPage(
                    title=page_data['title'],
                    slug=page_data['slug'],
                    content=page_data['content'],
                    seo_title=f"{page_data['title']} - MarketingNyt.dk",
                    search_description=f"Læs vores {page_data['title'].lower()} på MarketingNyt.dk"
                )
                homepage.add_child(instance=legal_page)
                legal_page.save_revision().publish()
                self.stdout.write(f'Created page: {page_data["title"]}')
                
            except Exception as e:
                self.stdout.write(f'Error creating {page_data["title"]}: {e}')
        
        self.stdout.write(self.style.SUCCESS('Legal pages setup complete!'))
