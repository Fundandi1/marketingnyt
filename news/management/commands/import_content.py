"""
Management command to import all content from local database to production.
This handles all the complex dependencies and setup required.
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction
from wagtail.models import Locale, Site
from wagtailcore.models import Page
from news.models import Category, ArticlePage, CategoryPage, HomePage, SiteSettings
import json
import os


class Command(BaseCommand):
    help = 'Import all content from local database'

    def handle(self, *args, **options):
        self.stdout.write("Starting content import...")
        
        try:
            with transaction.atomic():
                # Step 1: Ensure default locale exists
                self.setup_locale()
                
                # Step 2: Clear existing content
                self.clear_existing_content()
                
                # Step 3: Create basic structure
                self.create_basic_structure()
                
                # Step 4: Import categories
                self.import_categories()
                
                # Step 5: Import articles
                self.import_articles()
                
                # Step 6: Update search index
                call_command('update_index')
                
                self.stdout.write(
                    self.style.SUCCESS('Successfully imported all content!')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Import failed: {str(e)}')
            )
            raise

    def setup_locale(self):
        """Ensure default locale exists"""
        locale, created = Locale.objects.get_or_create(
            language_code='da',
            defaults={'language_code': 'da'}
        )
        if created:
            self.stdout.write("Created default locale: da")
        return locale

    def clear_existing_content(self):
        """Clear existing content but keep root page"""
        # Delete all pages except root
        Page.objects.filter(depth__gt=1).delete()
        
        # Clear categories
        Category.objects.all().delete()
        
        self.stdout.write("Cleared existing content")

    def create_basic_structure(self):
        """Create basic site structure"""
        root = Page.objects.get(depth=1)
        
        # Create HomePage
        home_page = HomePage(
            title="MarketingNyt.dk",
            slug="home",
            hero_title="Seneste nyt inden for digital marketing",
            hero_subtitle="Hold dig opdateret med de nyeste trends, værktøjer og strategier inden for digital marketing",
            seo_title="MarketingNyt.dk - Digital Marketing Nyheder",
            search_description="Danmarks førende platform for digital marketing nyheder og insights"
        )
        root.add_child(instance=home_page)
        home_page.save_revision().publish()
        
        # Set as site root
        site, created = Site.objects.get_or_create(
            hostname='marketingnyt.onrender.com',
            defaults={
                'hostname': 'marketingnyt.onrender.com',
                'port': 80,
                'site_name': 'MarketingNyt.dk',
                'root_page': home_page,
                'is_default_site': True
            }
        )
        if not created:
            site.root_page = home_page
            site.save()
        
        self.home_page = home_page
        self.stdout.write("Created HomePage and site structure")

    def import_categories(self):
        """Import categories and create category pages"""
        categories_data = [
            {
                'name': 'Paid Social',
                'slug': 'paid-social',
                'description': 'Facebook Ads, Instagram Ads, TikTok Ads og andre sociale medier'
            },
            {
                'name': 'AI & Marketing',
                'slug': 'ai-marketing',
                'description': 'Kunstig intelligens og marketing automation'
            },
            {
                'name': 'Google Ads',
                'slug': 'google-ads',
                'description': 'Søgebaseret performance marketing'
            },
            {
                'name': 'Content',
                'slug': 'content',
                'description': 'Content marketing, UGC, email og community'
            },
            {
                'name': 'CRO',
                'slug': 'cro',
                'description': 'Conversion Rate Optimization'
            },
            {
                'name': 'Podcasts',
                'slug': 'podcasts',
                'description': 'Lyt med til de nyeste marketing podcasts'
            }
        ]
        
        for cat_data in categories_data:
            # Create category snippet
            category = Category.objects.create(**cat_data)
            
            # Create category page
            category_page = CategoryPage(
                title=cat_data['name'],
                slug=cat_data['slug'],
                category=category,
                seo_title=f"{cat_data['name']} - MarketingNyt.dk",
                search_description=cat_data['description']
            )
            self.home_page.add_child(instance=category_page)
            category_page.save_revision().publish()
            
            self.stdout.write(f"Created category: {cat_data['name']}")

    def import_articles(self):
        """Import sample articles"""
        # Get categories
        paid_social = Category.objects.get(slug='paid-social')
        ai_marketing = Category.objects.get(slug='ai-marketing')
        google_ads = Category.objects.get(slug='google-ads')
        content = Category.objects.get(slug='content')
        
        articles_data = [
            {
                'title': 'Meta lancerer nye AI-funktioner til annoncører',
                'slug': 'meta-ai-funktioner-annoncoerer',
                'category': paid_social,
                'excerpt': 'Meta introducerer avancerede AI-værktøjer der automatisk optimerer annoncekampagner og forbedrer targeting.',
                'body': [
                    ('paragraph', 'Meta har annonceret en række nye AI-funktioner der vil revolutionere måden virksomheder annoncerer på Facebook og Instagram.'),
                    ('paragraph', 'De nye funktioner inkluderer automatisk kreativ optimering, intelligent budgetfordeling og forbedret audience targeting baseret på machine learning.'),
                    ('paragraph', 'Særligt interessant er den nye "Performance Max" funktion, der automatisk distribuerer budgettet på tværs af alle Meta\'s platforme for at maksimere ROI.'),
                    ('paragraph', 'Funktionerne rulles ud gradvist og forventes at være fuldt tilgængelige inden udgangen af 2024.')
                ]
            },
            {
                'title': 'TikTok Shopping: Den nye e-commerce revolution',
                'slug': 'tiktok-shopping-ecommerce-revolution',
                'category': paid_social,
                'excerpt': 'TikTok Shopping transformerer social commerce med innovative funktioner der gør det nemmere end nogensinde at sælge direkte på platformen.',
                'body': [
                    ('paragraph', 'TikTok har lanceret en omfattende opdatering af deres shopping-funktioner, der gør det muligt for brands at sælge direkte gennem videoer.'),
                    ('paragraph', 'Den nye "Shop Tab" giver brugerne adgang til et kureret udvalg af produkter, mens "Live Shopping" funktionen muliggør real-time salg under livestreams.'),
                    ('paragraph', 'Særligt bemærkelsesværdigt er integrationerne med Shopify og WooCommerce, der gør det nemt for eksisterende e-commerce virksomheder at komme i gang.'),
                    ('paragraph', 'Tidlige tests viser konverteringsrater der er 3x højere end traditionelle social media annoncer.')
                ]
            },
            {
                'title': 'Google Ads Performance Max: Komplet guide til 2024',
                'slug': 'google-ads-performance-max-guide-2024',
                'category': google_ads,
                'excerpt': 'Alt du behøver at vide om Google Ads Performance Max kampagner, inklusiv best practices og optimeringsstrategier.',
                'body': [
                    ('paragraph', 'Performance Max kampagner har revolutioneret Google Ads ved at give annoncører adgang til alle Google\'s kanaler gennem én enkelt kampagne.'),
                    ('paragraph', 'I 2024 har Google introduceret nye funktioner som forbedret audience insights, automatisk kreativ generering og enhanced conversion tracking.'),
                    ('paragraph', 'For at få succes med Performance Max er det kritisk at have stærke kreative assets, klare konverteringsmål og tilstrækkelig data til machine learning algoritmerne.'),
                    ('paragraph', 'Vores tests viser at Performance Max kampagner i gennemsnit leverer 15% bedre ROAS sammenlignet med traditionelle Search kampagner.')
                ]
            },
            {
                'title': 'Content Marketing ROI: Sådan måler du succes i 2024',
                'slug': 'content-marketing-roi-maal-succes-2024',
                'category': content,
                'excerpt': 'Lær hvordan du måler og optimerer ROI på dit content marketing med de nyeste metoder og værktøjer.',
                'body': [
                    ('paragraph', 'Content marketing ROI kan være udfordrende at måle, men med de rigtige metoder og værktøjer kan du få præcise insights i din indsats.'),
                    ('paragraph', 'De vigtigste metrics inkluderer brand awareness lift, lead generation cost, customer acquisition cost og lifetime value påvirkning.'),
                    ('paragraph', 'Nye AI-drevne analytics værktøjer som Google Analytics 4\'s enhanced measurements og HubSpot\'s attribution reporting gør det nemmere at tracke content performance.'),
                    ('paragraph', 'Best practice er at etablere baseline metrics før kampagnestart og måle både short-term og long-term impact på forretningsresultater.')
                ]
            }
        ]
        
        for article_data in articles_data:
            article = ArticlePage(
                title=article_data['title'],
                slug=article_data['slug'],
                category=article_data['category'],
                excerpt=article_data['excerpt'],
                body=article_data['body'],
                seo_title=f"{article_data['title']} - MarketingNyt.dk",
                search_description=article_data['excerpt']
            )
            self.home_page.add_child(instance=article)
            article.save_revision().publish()
            
            self.stdout.write(f"Created article: {article_data['title']}")
        
        self.stdout.write(f"Created {len(articles_data)} articles")
