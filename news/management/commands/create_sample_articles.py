from django.core.management.base import BaseCommand
from news.models import ArticlePage, HomePage, Category
from wagtail.rich_text import RichText
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Create sample articles for the website'

    def handle(self, *args, **options):
        # Get homepage and categories
        home = HomePage.objects.first()
        categories = list(Category.objects.all())

        # Create more articles
        new_articles = [
            {
                'title': 'Google Ads: Nye AI-funktioner revolutionerer PPC',
                'slug': 'google-ads-ai-funktioner-ppc',
                'summary': 'Google introducerer avancerede AI-værktøjer til Google Ads, der automatisk optimerer kampagner og forbedrer ROI med op til 40%.',
                'category': 'PPC',
                'author': 'Maria Nielsen',
                'days_ago': 1
            },
            {
                'title': 'Instagram Reels: Sådan øger du engagement med 300%',
                'slug': 'instagram-reels-engagement-guide',
                'summary': 'Lær de hemmeligheder, som top-influencere bruger til at skabe virale Instagram Reels og bygge en loyal følgerskare.',
                'category': 'Paid Social',
                'author': 'Thomas Larsen',
                'days_ago': 2
            },
            {
                'title': 'Email Marketing: Personalisering der konverterer',
                'slug': 'email-marketing-personalisering-2024',
                'summary': 'Opdagelse af avancerede personaliseringsteknikker, der kan øge email open rates med 45% og click-through rates med 60%.',
                'category': 'AI & Marketing',
                'author': 'Sarah Andersen',
                'days_ago': 3
            },
            {
                'title': 'LinkedIn B2B Marketing: Strategier for 2024',
                'slug': 'linkedin-b2b-marketing-strategier',
                'summary': 'Komplet guide til LinkedIn marketing for B2B virksomheder, inklusive organisk vækst og paid advertising strategier.',
                'category': 'Paid Social',
                'author': 'Michael Jensen',
                'days_ago': 4
            },
            {
                'title': 'Voice Search SEO: Optimer for fremtidens søgninger',
                'slug': 'voice-search-seo-optimering',
                'summary': 'Med stigningen i voice search bliver det kritisk at optimere dit indhold. Lær hvordan du forbereder din SEO-strategi.',
                'category': 'SEO',
                'author': 'Anna Christensen',
                'days_ago': 5
            },
            {
                'title': 'Marketing Automation: ROI-guide til små virksomheder',
                'slug': 'marketing-automation-roi-sma-virksomheder',
                'summary': 'Hvordan små virksomheder kan implementere marketing automation uden store budgetter og stadig opnå imponerende resultater.',
                'category': 'AI & Marketing',
                'author': 'Peter Møller',
                'days_ago': 6
            },
            {
                'title': 'YouTube Shorts vs TikTok: Hvor skal du investere?',
                'slug': 'youtube-shorts-vs-tiktok-marketing',
                'summary': 'Sammenligning af YouTube Shorts og TikTok som marketingplatforme - hvilken giver det bedste ROI for din virksomhed?',
                'category': 'Paid Social',
                'author': 'Lisa Hansen',
                'days_ago': 7
            },
            {
                'title': 'Conversion Rate Optimization: A/B test guide',
                'slug': 'conversion-rate-optimization-ab-test',
                'summary': 'Systematisk tilgang til CRO med praktiske A/B test eksempler, der har øget konverteringsrater med over 200%.',
                'category': 'SEO',
                'author': 'David Sørensen',
                'days_ago': 8
            }
        ]

        self.stdout.write('Creating new articles...')

        for i, article_data in enumerate(new_articles, 1):
            # Check if article already exists
            if ArticlePage.objects.filter(slug=article_data['slug']).exists():
                self.stdout.write(f'  {i}. Skipped (exists): {article_data["title"]}')
                continue

            # Find or create category
            category = None
            for cat in categories:
                if cat.name == article_data['category']:
                    category = cat
                    break
            
            if not category:
                category = categories[0]  # Use first category as fallback

            # Create article with simple approach
            article = ArticlePage(
                title=article_data['title'],
                slug=article_data['slug'],
                summary=article_data['summary'],
                body=[
                    ('paragraph', RichText(f'<p>Dette er en detaljeret artikel om {article_data["title"].lower()}. Artiklen indeholder omfattende information og praktiske tips til marketingprofessionelle.</p>')),
                    ('paragraph', RichText('<p>Her finder du de nyeste trends og strategier inden for digital marketing, som kan hjælpe din virksomhed med at opnå bedre resultater.</p>')),
                    ('paragraph', RichText('<p>Artiklen er skrevet af eksperter med mange års erfaring inden for området og indeholder konkrete eksempler og case studies.</p>'))
                ],
                category=category,
                author=article_data['author'],
                published_at=datetime.now() - timedelta(days=article_data['days_ago']),
                is_featured=False
            )

            # Save as child of homepage
            home.add_child(instance=article)
            
            # Publish the article
            revision = article.save_revision()
            revision.publish()

            self.stdout.write(f'  {i}. Created: {article.title}')

        self.stdout.write(self.style.SUCCESS('Done creating articles!'))
