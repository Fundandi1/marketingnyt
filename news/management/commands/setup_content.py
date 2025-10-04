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
            {'name': 'Digital Marketing', 'description': 'Alt om digital markedsføring'},
            {'name': 'Social Media', 'description': 'Sociale medier og trends'},
            {'name': 'SEO', 'description': 'Søgemaskineoptimering'},
            {'name': 'Content Marketing', 'description': 'Indholdsmarkedsføring'},
            {'name': 'E-commerce', 'description': 'Online handel og e-commerce'},
            {'name': 'Analytics', 'description': 'Data og analyse'},
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
        
        # Get root page
        root_page = Page.objects.get(id=1)
        
        # Create HomePage
        try:
            homepage = HomePage.objects.get(slug='home')
            self.stdout.write('HomePage already exists')
        except HomePage.DoesNotExist:
            homepage = HomePage(
                title='MarketingNyt.dk',
                slug='home',
                hero_title='Velkommen til MarketingNyt.dk',
                hero_subtitle='Din kilde til de seneste nyheder inden for digital marketing',
            )
            root_page.add_child(instance=homepage)
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
                'title': 'Google lancerer nye AI-funktioner til annoncører',
                'summary': 'Google introducerer avancerede AI-værktøjer der skal hjælpe annoncører med at optimere deres kampagner.',
                'category': 'Digital Marketing',
                'body': '<p>Google har annonceret en række nye AI-funktioner til Google Ads platformen. Disse værktøjer vil hjælpe annoncører med automatisk at optimere deres kampagner baseret på brugeradfærd og markedstrends.</p><p>De nye funktioner inkluderer automatisk budgivning, intelligent målgruppesegmentering og dynamisk annoncetilpasning.</p>',
                'author': 'MarketingNyt Redaktion',
            },
            {
                'title': 'TikTok introducerer nye shopping-funktioner',
                'summary': 'TikTok udvider sine e-commerce muligheder med nye shopping-funktioner der gør det nemmere for brands at sælge direkte på platformen.',
                'category': 'Social Media',
                'body': '<p>TikTok har lanceret en række nye shopping-funktioner der skal gøre det nemmere for virksomheder at sælge produkter direkte gennem platformen.</p><p>De nye funktioner inkluderer produktkataloger, live shopping events og forbedret integration med e-commerce platforme.</p>',
                'author': 'MarketingNyt Redaktion',
            },
            {
                'title': 'SEO trends for 2024: Hvad du skal vide',
                'summary': 'Eksperterne deler deres forudsigelser for de vigtigste SEO trends i 2024.',
                'category': 'SEO',
                'body': '<p>SEO landskabet fortsætter med at udvikle sig, og 2024 bringer nye udfordringer og muligheder for marketingfolk.</p><p>De vigtigste trends inkluderer øget fokus på AI-genereret indhold, voice search optimering og Core Web Vitals.</p>',
                'author': 'MarketingNyt Redaktion',
            },
            {
                'title': 'Content Marketing ROI: Sådan måler du succes',
                'summary': 'En guide til at måle og optimere dit content marketing ROI med de rigtige metrics og værktøjer.',
                'category': 'Content Marketing',
                'body': '<p>At måle ROI på content marketing kan være udfordrende, men med de rigtige metrics og værktøjer kan du få værdifuld indsigt i dine kampagners performance.</p><p>Fokuser på metrics som engagement rate, lead generation og customer lifetime value.</p>',
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
