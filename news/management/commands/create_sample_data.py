"""
Management command to create sample data for development.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from wagtail.models import Site

from news.models import ArticlePage, Category, HomePage, SiteSettings


class Command(BaseCommand):
    help = "Create sample data for development"
    
    def handle(self, *args, **options):
        # Create site settings
        site_settings, created = SiteSettings.objects.get_or_create(
            defaults={
                "site_name": "MarketingNyt.dk",
                "default_meta_title": "MarketingNyt.dk - Danmarks førende marketing platform",
                "default_meta_description": "Få de seneste nyheder, trends og insights inden for marketing, digital markedsføring og reklame på MarketingNyt.dk",
                "social_twitter": "marketingnyt",
                "social_facebook": "marketingnyt",
                "social_linkedin": "marketingnyt",
            }
        )
        
        if created:
            self.stdout.write("Created site settings")
        
        # Create categories
        categories_data = [
            {
                "name": "SEO",
                "slug": "seo",
                "description": "Alt om søgemaskineoptimering, Google algoritmer og organisk trafik"
            },
            {
                "name": "Paid Social",
                "slug": "paid-social",
                "description": "Facebook Ads, Instagram markedsføring og sociale medier annoncering"
            },
            {
                "name": "AI & Marketing",
                "slug": "ai-marketing",
                "description": "Kunstig intelligens i marketing, automatisering og nye teknologier"
            }
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data["slug"],
                defaults={
                    "name": cat_data["name"],
                    "description": cat_data["description"]
                }
            )
            categories[cat_data["slug"]] = category
            if created:
                self.stdout.write(f"Created category: {category.name}")
        
        # Get home page
        site = Site.objects.get(is_default_site=True)
        home_page = site.root_page.specific
        
        # Create sample articles
        articles_data = [
            {
                "title": "Google lancerer ny Core Web Vitals opdatering",
                "slug": "google-core-web-vitals-opdatering",
                "summary": "Google annoncerer vigtige ændringer til Core Web Vitals som vil påvirke søgerangeringer fra marts 2024. Lær hvad du skal gøre for at forberede din hjemmeside.",
                "category": "seo",
                "author": "Sarah Nielsen",
                "body": "Google har netop annonceret en stor opdatering til deres Core Web Vitals metrics, som vil træde i kraft i marts 2024. Denne opdatering vil have betydelig indflydelse på hvordan hjemmesider rangerer i søgeresultaterne.\n\nDe nye metrics fokuserer særligt på brugeroplevelsen på mobile enheder, hvor Google har observeret at mange hjemmesider stadig ikke lever op til deres standarder for hastighed og responsivitet.\n\nVigtigste ændringer:\n- Ny INP (Interaction to Next Paint) metric erstatter FID\n- Skærpede krav til LCP (Largest Contentful Paint)\n- Forbedret måling af CLS (Cumulative Layout Shift)\n\nFor at forberede din hjemmeside anbefaler vi at du starter med at analysere dine nuværende Core Web Vitals scores i Google Search Console og PageSpeed Insights.",
                "is_featured": True
            },
            {
                "title": "Facebook Ads: 5 strategier der virker i 2024",
                "slug": "facebook-ads-strategier-2024",
                "summary": "Opdagede de mest effektive Facebook Ads strategier for 2024. Fra creative testing til audience targeting - her er hvad der virkelig flytter nålen.",
                "category": "paid-social",
                "author": "Michael Larsen",
                "body": "Facebook advertising landskabet ændrer sig konstant, og 2024 er ingen undtagelse. Med iOS 14.5+ privacy ændringer og stigende konkurrence, skal marketers tænke smartere om deres Facebook Ads strategi.\n\nHer er de 5 strategier som viser de bedste resultater:\n\n1. **Broad Targeting med Creative Testing**\nI stedet for snæver targeting, lad Facebooks algoritme finde din målgruppe gennem omfattende creative testing.\n\n2. **Video-First Approach**\nVideo content performer konsistent bedre end statiske billeder, især på mobile enheder.\n\n3. **Conversion API Implementation**\nServer-side tracking bliver kritisk for præcis måling og optimering.\n\n4. **UGC (User Generated Content)**\nAutentisk indhold fra rigtige kunder skaber højere engagement og konverteringer.\n\n5. **Retention Campaigns**\nFokus på eksisterende kunder gennem email lists og custom audiences giver højere ROI.",
                "is_featured": True
            },
            {
                "title": "ChatGPT til content marketing: Komplet guide",
                "slug": "chatgpt-content-marketing-guide",
                "summary": "Lær hvordan du bruger ChatGPT og andre AI-tools til at skabe bedre content marketing. Praktiske tips, prompts og workflows der sparer tid og forbedrer kvaliteten.",
                "category": "ai-marketing",
                "author": "Anna Christensen",
                "body": "Kunstig intelligens revolutionerer content marketing, og ChatGPT er i front. Men hvordan bruger du det effektivt uden at miste den menneskelige touch?\n\n**Content Ideation**\nBrug ChatGPT til at generere content ideer baseret på din målgruppe og branche. Prøv prompts som: 'Generer 10 blog post ideer for B2B SaaS virksomheder der fokuserer på produktivitet'\n\n**Content Outline**\nLad AI hjælpe med at strukturere dit indhold. Giv det dit emne og målgruppe, og få en detaljeret outline.\n\n**SEO Optimering**\nChatGPT kan hjælpe med keyword research, meta descriptions og title tags der både appellerer til søgemaskiner og mennesker.\n\n**Social Media Posts**\nGenerer variationer af sociale medier posts til forskellige platforme baseret på dit hovedindhold.\n\n**Email Marketing**\nSkab personaliserede email sekvenser og subject lines der øger åbningsrater.\n\nHusk: AI er et værktøj, ikke en erstatning. Tilføj altid din ekspertise og brand voice til det AI-genererede indhold.",
                "is_featured": False
            },
            {
                "title": "TikTok Ads: Begynderguide til success",
                "slug": "tiktok-ads-begynderguide",
                "summary": "TikTok Ads bliver stadig vigtigere for brands. Her er din komplette guide til at komme i gang med TikTok advertising og skabe campaigns der konverterer.",
                "category": "paid-social",
                "author": "Jonas Pedersen",
                "body": "TikTok er ikke længere bare for Gen Z. Platformen har over 1 milliard aktive brugere og tilbyder unikke muligheder for brands der vil nå nye målgrupper.\n\n**Kom i gang med TikTok Ads Manager**\nOpret din TikTok Ads Manager konto og forbind den til din TikTok Business profil. Sørg for at have dine tracking pixels installeret.\n\n**Campaign Objectives**\nTikTok tilbyder forskellige campaign mål:\n- Awareness: Brand awareness og reach\n- Consideration: Traffic, app installs, video views\n- Conversion: Conversions, catalog sales\n\n**Creative Best Practices**\n- Vertikalt format (9:16)\n- Autentisk, ikke-poleret indhold\n- Hook seerne inden for de første 3 sekunder\n- Brug trending sounds og hashtags\n- Test UGC-style content\n\n**Targeting Options**\nTikTok tilbyder demografisk, interesse-baseret og behavioral targeting. Start bredt og lad algoritmen optimere.\n\n**Budget og Bidding**\nStart med mindst 50 USD per dag per ad group for at give algoritmen nok data til optimering.",
                "is_featured": False
            },
            {
                "title": "Local SEO: Dominér lokale søgninger",
                "slug": "local-seo-guide-2024",
                "summary": "Local SEO er kritisk for lokale virksomheder. Lær de vigtigste strategier til at rangere højt i lokale søgninger og Google My Business optimering.",
                "category": "seo",
                "author": "Lars Hansen",
                "body": "For lokale virksomheder er Local SEO forskellen mellem succes og fiasko. 46% af alle Google søgninger har lokal intent, så det er kritisk at optimere for lokale søgninger.\n\n**Google My Business Optimering**\nDin GMB profil er fundamentet for Local SEO:\n- Udfyld alle felter komplet\n- Upload high-quality billeder regelmæssigt\n- Saml og besvar anmeldelser\n- Post opdateringer og tilbud\n- Brug relevante kategorier\n\n**NAP Consistency**\nSørg for at dit navn, adresse og telefonnummer (NAP) er identisk på tværs af alle online platforme:\n- Hjemmeside\n- Social media profiler\n- Online directories\n- Citations\n\n**Lokale Keywords**\nOptimér for keywords der inkluderer din by eller område:\n- 'Frisør København'\n- 'Restaurant Aarhus'\n- 'Tømrer nær mig'\n\n**Local Citations**\nByg citations på relevante lokale directories og branche-specifikke sites. Kvalitet er vigtigere end kvantitet.\n\n**Reviews Management**\nAnmeldelser påvirker både rankings og konverteringer. Implementer en strategi for at få flere positive anmeldelser.",
                "is_featured": False
            },
            {
                "title": "Marketing Automation: ROI guide 2024",
                "slug": "marketing-automation-roi-guide",
                "summary": "Marketing automation kan øge din ROI med op til 451%. Her er hvordan du implementerer automation workflows der virkelig flytter bundlinjen.",
                "category": "ai-marketing",
                "author": "Maria Sørensen",
                "body": "Marketing automation er ikke længere nice-to-have - det er en nødvendighed for virksomheder der vil skalere effektivt. Studier viser at virksomheder der bruger marketing automation ser en gennemsnitlig ROI stigning på 451%.\n\n**Email Automation Workflows**\nStart med disse grundlæggende workflows:\n- Welcome series for nye subscribers\n- Abandoned cart recovery\n- Post-purchase follow-up\n- Re-engagement campaigns\n- Birthday/anniversary emails\n\n**Lead Scoring**\nImplementer lead scoring for at identificere sales-ready leads:\n- Website aktivitet (sider besøgt, tid på site)\n- Email engagement (åbninger, clicks)\n- Content downloads\n- Webinar deltagelse\n- Social media interaktioner\n\n**Personalisering**\nBrug data til at personalisere oplevelsen:\n- Dynamisk content baseret på interesser\n- Produktanbefalinger\n- Geografisk tilpasset indhold\n- Behavioral triggers\n\n**Integration med CRM**\nSørg for seamless integration mellem marketing automation og dit CRM system for at sikre data konsistens og bedre lead handoff til sales.\n\n**Måling og Optimering**\nTrack key metrics som:\n- Email open rates og click-through rates\n- Conversion rates per workflow\n- Lead-to-customer conversion\n- Customer lifetime value\n- Revenue attribution",
                "is_featured": True
            }
        ]
        
        created_count = 0
        for article_data in articles_data:
            # Check if article already exists
            if ArticlePage.objects.filter(slug=article_data["slug"]).exists():
                continue
            
            category = categories[article_data["category"]]
            
            # Create rich text body
            body_content = []
            paragraphs = article_data["body"].split("\n\n")
            
            for paragraph in paragraphs:
                if paragraph.strip():
                    if paragraph.startswith("**") and paragraph.endswith("**"):
                        # Convert to heading
                        heading_text = paragraph.strip("*").strip()
                        body_content.append(("heading", {"level": "h2", "text": heading_text}))
                    else:
                        body_content.append(("rich_text", f"<p>{paragraph}</p>"))
            
            article = ArticlePage(
                title=article_data["title"],
                slug=article_data["slug"],
                summary=article_data["summary"],
                body=body_content,
                category=category,
                author=article_data["author"],
                published_at=timezone.now(),
                is_featured=article_data["is_featured"]
            )
            
            home_page.add_child(instance=article)
            article.save_revision().publish()
            
            # Add some tags
            if article_data["category"] == "seo":
                article.tags.add("SEO", "Google", "Søgemaskineoptimering")
            elif article_data["category"] == "paid-social":
                article.tags.add("Facebook Ads", "Social Media", "Paid Advertising")
            elif article_data["category"] == "ai-marketing":
                article.tags.add("AI", "Automation", "ChatGPT", "Marketing Technology")
            
            created_count += 1
            self.stdout.write(f"Created article: {article.title}")
        
        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {created_count} sample articles")
        )
