"""
Management command to set up initial content for the site.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from wagtail.models import Site, Page
from news.models import HomePage, ArticlePage, CategoryPage, Category, SiteSettings


class Command(BaseCommand):
    help = 'Set up initial content for the site'

    def handle(self, *args, **options):
        self.stdout.write('Setting up initial content...')
        
        # Create categories
        categories_data = [
            {'name': 'Paid Social', 'description': 'Facebook Ads, Instagram Ads, TikTok Ads og andre sociale medier'},
            {'name': 'AI & Marketing', 'description': 'Kunstig intelligens og marketing automation'},
            {'name': 'Google Ads', 'description': 'Søgebaseret performance marketing'},
            {'name': 'Content', 'description': 'Content marketing, UGC, email og community'},
            {'name': 'CRO', 'description': 'Conversion Rate Optimization'},
            {'name': 'Podcasts', 'description': 'Lyt med til de nyeste marketing podcasts'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create site settings
        site_settings, created = SiteSettings.objects.get_or_create(
            id=1,
            defaults={
                'site_name': 'MarketingNyt.dk',
                'default_meta_title': 'MarketingNyt.dk - Nyheder om marketing',
                'default_meta_description': 'Få de seneste nyheder om digital marketing, SEO, social media og meget mere.',
            }
        )
        if created:
            self.stdout.write('Created site settings')
        
        # Get or create root page
        root_page = Page.objects.filter(depth=1).first()
        if not root_page:
            # Create root page if it doesn't exist
            root_page = Page(
                title='Root',
                slug='root',
                path='0001',
                depth=1,
                numchild=0,
                url_path='/',
            )
            root_page.save()
            self.stdout.write('Created root page')

        # Create HomePage - check if any HomePage exists first
        homepage = HomePage.objects.first()
        if homepage:
            self.stdout.write(f'HomePage already exists: {homepage.title}')
        else:
            # Check if there's already a page with slug 'home'
            existing_home = Page.objects.filter(slug='home').first()
            if existing_home:
                # Convert existing page to HomePage if it's not already
                if not isinstance(existing_home.specific, HomePage):
                    self.stdout.write('Converting existing home page to HomePage')
                    # Delete the existing page and create new HomePage
                    existing_home.delete()
                else:
                    homepage = existing_home.specific
                    self.stdout.write('Found existing HomePage')

            if not homepage:
                homepage = HomePage(
                    title='MarketingNyt.dk',
                    slug='home',  # Use simple slug
                    hero_title='Velkommen til MarketingNyt.dk',
                    hero_subtitle='Din kilde til de seneste nyheder inden for digital marketing',
                )
                # Use a different method to add the page
                homepage.path = '00010001'
                homepage.depth = 2
                homepage.save()

                # Update root page numchild
                root_page.numchild = 1
                root_page.save()

                homepage.save_revision().publish()
                self.stdout.write('Created HomePage')
        
        # Create category pages
        for cat_name, category in categories.items():
            try:
                cat_page = CategoryPage.objects.get(slug=category.slug)
                self.stdout.write(f'CategoryPage for {cat_name} already exists')
            except CategoryPage.DoesNotExist:
                cat_page = CategoryPage(
                    title=f'{cat_name} Nyheder',
                    slug=category.slug,
                    category=category,
                    intro=f'Seneste nyheder inden for {cat_name.lower()}',
                )
                homepage.add_child(instance=cat_page)
                cat_page.save_revision().publish()
                self.stdout.write(f'Created CategoryPage for {cat_name}')
        
        # Create sample articles
        articles_data = [
            {
                'title': 'Meta lancerer nye AI-funktioner til annoncører',
                'summary': 'Meta introducerer avancerede AI-værktøjer der automatisk optimerer annoncekampagner og forbedrer targeting.',
                'category': 'Paid Social',
                'body': [
                    ('paragraph', 'Meta har annonceret en række nye AI-funktioner der vil revolutionere måden virksomheder annoncerer på Facebook og Instagram.'),
                    ('paragraph', 'De nye funktioner inkluderer automatisk kreativ optimering, intelligent budgetfordeling og forbedret audience targeting baseret på machine learning.')
                ],
                'author': 'MarketingNyt Redaktion',
            },
            {
                'title': 'TikTok Shopping: Den nye e-commerce revolution',
                'summary': 'TikTok Shopping transformerer social commerce med innovative funktioner der gør det nemmere end nogensinde at sælge direkte på platformen.',
                'category': 'Paid Social',
                'body': [
                    ('paragraph', 'TikTok har lanceret en omfattende opdatering af deres shopping-funktioner, der gør det muligt for brands at sælge direkte gennem videoer.'),
                    ('paragraph', 'Den nye "Shop Tab" giver brugerne adgang til et kureret udvalg af produkter, mens "Live Shopping" funktionen muliggør real-time salg under livestreams.')
                ],
                'author': 'MarketingNyt Redaktion',
            },
            {
                'title': 'Google Ads Performance Max: Komplet guide til 2024',
                'summary': 'Alt du behøver at vide om Google Ads Performance Max kampagner, inklusiv best practices og optimeringsstrategier.',
                'category': 'Google Ads',
                'body': [
                    ('paragraph', 'Performance Max kampagner har revolutioneret Google Ads ved at give annoncører adgang til alle Google\'s kanaler gennem én enkelt kampagne.'),
                    ('paragraph', 'I 2024 har Google introduceret nye funktioner som forbedret audience insights, automatisk kreativ generering og enhanced conversion tracking.')
                ],
                'author': 'MarketingNyt Redaktion',
            },
            {
                'title': 'Content Marketing ROI: Sådan måler du succes i 2024',
                'summary': 'Lær hvordan du måler og optimerer ROI på dit content marketing med de nyeste metoder og værktøjer.',
                'category': 'Content',
                'body': [
                    ('paragraph', 'Content marketing ROI kan være udfordrende at måle, men med de rigtige metoder og værktøjer kan du få præcise insights i din indsats.'),
                    ('paragraph', 'De vigtigste metrics inkluderer brand awareness lift, lead generation cost, customer acquisition cost og lifetime value påvirkning.')
                ],
                'author': 'MarketingNyt Redaktion',
            },
        ]
        
        for article_data in articles_data:
            category = categories[article_data['category']]
            try:
                article = ArticlePage.objects.get(title=article_data['title'])
                self.stdout.write(f'Article "{article_data["title"]}" already exists')
            except ArticlePage.DoesNotExist:
                article = ArticlePage(
                    title=article_data['title'],
                    summary=article_data['summary'],
                    body=article_data['body'],
                    category=category,
                    author=article_data['author'],
                    published_at=timezone.now(),
                )
                homepage.add_child(instance=article)
                article.save_revision().publish()
                self.stdout.write(f'Created article: {article_data["title"]}')
        
        # Update site to use HomePage as root
        try:
            site = Site.objects.get(hostname='localhost')
            site.root_page = homepage
            site.hostname = 'marketingnyt.onrender.com'
            site.port = 80
            site.save()
            self.stdout.write('Updated site settings')
        except Site.DoesNotExist:
            Site.objects.create(
                hostname='marketingnyt.onrender.com',
                port=80,
                root_page=homepage,
                is_default_site=True,
                site_name='MarketingNyt.dk'
            )
            self.stdout.write('Created new site')
        
        self.stdout.write(self.style.SUCCESS('Successfully set up initial content!'))
        self.stdout.write(f'HomePage: {homepage.title}')
        self.stdout.write(f'Categories: {len(categories)}')
        self.stdout.write(f'Articles: {len(articles_data)}')
