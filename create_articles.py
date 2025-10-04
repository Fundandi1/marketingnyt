#!/usr/bin/env python
import os
import django
import json
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketingnyt.settings')
django.setup()

from news.models import ArticlePage, Category, HomePage
from wagtail.images.models import Image

# Hent kategorier
categories = {
    'ai': Category.objects.get(slug='ai-marketing'),
    'google_ads': Category.objects.get(slug='google-ads'),
    'content': Category.objects.get(slug='content'),
    'cro': Category.objects.get(slug='cro'),
    'paid_social': Category.objects.get(slug='paid-social'),
}

homepage = HomePage.objects.first()
default_image = Image.objects.first()

# Tæl eksisterende artikler per kategori
existing_counts = {
    'ai': ArticlePage.objects.filter(category=categories['ai']).count(),
    'google_ads': ArticlePage.objects.filter(category=categories['google_ads']).count(),
    'content': ArticlePage.objects.filter(category=categories['content']).count(),
    'cro': ArticlePage.objects.filter(category=categories['cro']).count(),
    'paid_social': ArticlePage.objects.filter(category=categories['paid_social']).count(),
}

print("=== EKSISTERENDE ARTIKLER ===")
for cat_key, count in existing_counts.items():
    print(f"{cat_key}: {count} artikler")

# Artikler til Content kategori (mangler 4 mere)
content_articles = [
    {
        'title': 'Community Marketing: Byg en loyal fanbase der sælger for dig',
        'slug': 'community-marketing-strategi',
        'summary': 'Community marketing skaber langsigtede relationer og brand ambassadører. Lær hvordan du bygger et engageret fællesskab.',
        'body': '<h2>Hvad er community marketing?</h2><p>Community marketing handler om at skabe et fællesskab omkring dit brand hvor medlemmerne interagerer med hinanden - ikke kun med dit brand. Det er forskellen mellem at have følgere og at have fans.</p><h2>Hvorfor community marketing virker</h2><p>Et stærkt community giver dig gratis marketing gennem word-of-mouth, værdifuld feedback på produkter, højere customer lifetime value, og lavere customer acquisition costs.</p><h2>Platforme til community building</h2><p><strong>Facebook Groups:</strong> Stadig den største platform for communities. Gratis og nem at starte.<br><strong>Discord:</strong> Populær blandt yngre målgrupper. God til real-time chat.<br><strong>Slack:</strong> Professionel og struktureret. God til B2B communities.<br><strong>Circle/Mighty Networks:</strong> Dedikerede community platforme med flere features.</p><h2>5 regler for succesfuldt community</h2><p>1. <strong>Vær aktiv selv:</strong> Du skal være til stede og deltage dagligt i starten.<br>2. <strong>Skab værdi først:</strong> Giv mere end du tager. Del viden, svar på spørgsmål.<br>3. <strong>Faciliter samtaler:</strong> Stil spørgsmål, start diskussioner, tag medlemmer.<br>4. <strong>Fejr medlemmer:</strong> Highlight succeshistorier og aktive medlemmer.<br>5. <strong>Hav klare regler:</strong> Definer hvad der er okay og ikke okay.</p>',
        'category': categories['content'],
    },
    {
        'title': 'Content Repurposing: Få 10x mere værdi ud af dit content',
        'slug': 'content-repurposing-guide',
        'summary': 'Stop med at skabe nyt content hele tiden. Lær hvordan du genbruger eksisterende content på tværs af platforme.',
        'body': '<h2>Hvad er content repurposing?</h2><p>Content repurposing er kunsten at tage ét stykke content og omdanne det til multiple formater til forskellige platforme. En blog post kan blive til: LinkedIn posts, Instagram carousel, YouTube video, podcast episode, email newsletter, Twitter thread, og TikTok video.</p><h2>Hvorfor repurpose content?</h2><p>Det sparer tid og ressourcer, når du ikke skal skabe nyt content fra bunden hver gang. Du når forskellige målgrupper der foretrækker forskellige formater. Og du forstærker dit budskab gennem gentagelse.</p><h2>Content repurposing framework</h2><p><strong>Trin 1: Start med pillar content</strong><br>Skab ét stort, grundigt stykke content (blog post, video, podcast). Dette er dit "master content".</p><p><strong>Trin 2: Identificer key takeaways</strong><br>Find 5-10 vigtige pointer fra dit master content.</p><p><strong>Trin 3: Tilpas til platforme</strong><br>- LinkedIn: Skriv en post om hver key takeaway<br>- Instagram: Lav en carousel med tips<br>- YouTube Shorts: Lav korte videoer om hvert tip<br>- Email: Send en serie med dybdegående forklaringer<br>- Twitter: Lav en thread med alle tips</p><h2>Tools til repurposing</h2><p><strong>Descript:</strong> Transskriber video/audio til tekst automatisk<br><strong>Canva:</strong> Lav hurtigt visuelle assets til sociale medier<br><strong>Repurpose.io:</strong> Automatiser distribution på tværs af platforme</p>',
        'category': categories['content'],
    },
    {
        'title': 'SEO Content Strategy: Skriv content der ranker OG konverterer',
        'slug': 'seo-content-strategy',
        'summary': 'SEO content skal både ranke på Google og konvertere læsere til kunder. Lær den komplette strategi.',
        'body': '<h2>SEO content i 2025</h2><p>Google er blevet meget bedre til at forstå brugerintention. Det betyder at keyword stuffing ikke virker længere. I stedet skal du fokusere på at skabe genuint værdifuldt content der besvarer brugerens spørgsmål.</p><h2>Keyword research: Find de rigtige emner</h2><p><strong>1. Start med seed keywords</strong><br>Brug tools som Ahrefs, SEMrush eller gratis Google Keyword Planner til at finde relevante keywords.</p><p><strong>2. Analyser search intent</strong><br>Er brugeren i informational, navigational, commercial eller transactional mode? Tilpas dit content derefter.</p><p><strong>3. Find long-tail keywords</strong><br>Long-tail keywords (3-5 ord) har lavere konkurrence og højere conversion rate.</p><h2>Content struktur der ranker</h2><p><strong>Title tag:</strong> Inkluder primary keyword tidligt. Hold det under 60 tegn.<br><strong>H1:</strong> Skal matche title tag eller være en variation.<br><strong>H2-H6:</strong> Brug subheadings til at strukturere content. Inkluder relaterede keywords.<br><strong>Intro:</strong> Hook læseren i første 2-3 linjer. Forklar hvad de får ud af at læse.<br><strong>Body:</strong> Brug korte afsnit (2-3 linjer). Inkluder bullet points og lister.<br><strong>Konklusion:</strong> Opsummer key takeaways og inkluder en CTA.</p><h2>On-page SEO checklist</h2><p>✓ Primary keyword i title, H1, første afsnit og konklusion<br>✓ Relaterede keywords naturligt spredt i teksten<br>✓ Internal links til andre relevante sider<br>✓ External links til autoritative kilder<br>✓ Optimerede billeder med alt text<br>✓ Meta description der lokker til klik<br>✓ URL slug der er kort og beskrivende</p>',
        'category': categories['content'],
    },
    {
        'title': 'Video Marketing: Hvorfor video er fremtidens content format',
        'slug': 'video-marketing-strategi',
        'summary': 'Video content får 1200% mere engagement end tekst og billeder tilsammen. Lær hvordan du kommer i gang.',
        'body': '<h2>Video marketing statistikker</h2><p>86% af businesses bruger video som marketing tool. Video på landing pages kan øge conversion med 80%. Social media posts med video får 48% mere views. Og 72% af kunder foretrækker at lære om produkter gennem video.</p><h2>Typer af marketing video</h2><p><strong>Explainer videos:</strong> Forklar dit produkt eller service på 60-90 sekunder.<br><strong>Product demos:</strong> Vis hvordan dit produkt virker i praksis.<br><strong>Customer testimonials:</strong> Lad tilfredse kunder fortælle deres historie.<br><strong>Behind-the-scenes:</strong> Vis hvem der er bag brandet.<br><strong>Educational content:</strong> Undervis din målgruppe i relevante emner.<br><strong>Live video:</strong> Q&As, product launches, events.</p><h2>Platforme til video marketing</h2><p><strong>YouTube:</strong> Verdens næststørste søgemaskine. Perfekt til long-form content (10+ minutter).<br><strong>TikTok:</strong> Kort, underholdende content (15-60 sekunder). Yngre målgruppe.<br><strong>Instagram Reels:</strong> Lignende TikTok. God til at nå eksisterende følgere.<br><strong>LinkedIn:</strong> Professionelt content. B2B marketing.<br><strong>Facebook:</strong> Bred målgruppe. God til at nå ældre demografier.</p><h2>Video produktion på budget</h2><p>Du behøver ikke dyrt udstyr for at komme i gang:<br>- Brug din smartphone (moderne phones har fremragende kameraer)<br>- Naturligt lys er gratis og ser godt ud<br>- Gratis editing tools: CapCut, iMovie, DaVinci Resolve<br>- Brug stock music fra Epidemic Sound eller Artlist<br>- Teleprompter apps hjælper dig med at huske tekst</p>',
        'category': categories['content'],
    },
]

# Artikler til CRO kategori (mangler 6)
cro_articles = [
    {
        'title': 'Landing Page Optimization: 15 elementer der øger conversion',
        'slug': 'landing-page-optimization',
        'summary': 'En optimeret landing page kan fordoble din conversion rate. Lær de 15 vigtigste elementer.',
        'body': '<h2>Hvad er en landing page?</h2><p>En landing page er en standalone side designet til ét formål: at konvertere besøgende til leads eller kunder. I modsætning til din hjemmeside har en landing page ingen navigation eller distraktioner - kun én klar call-to-action.</p><h2>De 15 vigtigste elementer</h2><p><strong>1. Stærk headline:</strong> Kommunikér værdien i 5-10 ord.<br><strong>2. Subheadline:</strong> Uddyb værdien i 1-2 linjer.<br><strong>3. Hero image/video:</strong> Vis dit produkt i brug.<br><strong>4. Social proof:</strong> Testimonials, reviews, logos af kendte kunder.<br><strong>5. Benefits over features:</strong> Forklar hvad kunden får ud af det.<br><strong>6. Clear CTA:</strong> Én primær knap der skiller sig ud.<br><strong>7. Above the fold:</strong> Vigtigste info skal være synlig uden scroll.<br><strong>8. Trust signals:</strong> Sikkerhedsbadges, garantier, certificeringer.<br><strong>9. Urgency/scarcity:</strong> Tidsbegrænsede tilbud, begrænset lager.<br><strong>10. Mobile optimization:</strong> 60% af traffic er mobil.<br><strong>11. Fast loading:</strong> Hver sekund ekstra loading tid = 7% færre conversions.<br><strong>12. Minimal form fields:</strong> Jo færre felter, jo højere conversion.<br><strong>13. Exit-intent popup:</strong> Sidste chance for at konvertere.<br><strong>14. Live chat:</strong> Besvar spørgsmål i real-time.<br><strong>15. A/B testing:</strong> Test altid forskellige variationer.</p><h2>Landing page formler</h2><p><strong>PAS (Problem-Agitate-Solution):</strong><br>1. Identificér problemet<br>2. Gør problemet værre (agitate)<br>3. Præsentér din løsning</p><p><strong>AIDA (Attention-Interest-Desire-Action):</strong><br>1. Fang attention med stærk headline<br>2. Skab interest med benefits<br>3. Byg desire med social proof<br>4. Kald til action med klar CTA</p>',
        'category': categories['cro'],
    },
    {
        'title': 'A/B Testing Guide: Sådan tester du som en pro',
        'slug': 'ab-testing-guide',
        'summary': 'A/B testing er den eneste måde at vide hvad der virker. Lær hvordan du designer og kører valide tests.',
        'body': '<h2>Hvad er A/B testing?</h2><p>A/B testing (split testing) er metoden hvor du sammenligner to versioner af en side, email eller annonce for at se hvilken performer bedst. Version A (control) vs. Version B (variant).</p><h2>Hvad skal du teste?</h2><p><strong>Headlines:</strong> Den vigtigste faktor for engagement.<br><strong>CTA buttons:</strong> Tekst, farve, størrelse, placering.<br><strong>Images:</strong> Product shots vs. lifestyle images.<br><strong>Copy length:</strong> Kort vs. lang beskrivelse.<br><strong>Form fields:</strong> Antal felter påvirker conversion.<br><strong>Pricing:</strong> Forskellige prisstrukturer.<br><strong>Layout:</strong> Placering af elementer.<br><strong>Social proof:</strong> Type og placering af testimonials.</p><h2>Sådan designer du en valid test</h2><p><strong>1. Formuler en hypotese:</strong><br>Jeg tror at en groen CTA-knap vil oege clicks med 10 procent fordi groen signalerer go og skiller sig mere ud end vores nuvaerende blaa knap.</p><p><strong>2. Definer success metrics:</strong><br>Hvad maaler du? Click-through rate, conversion rate, revenue per visitor?</p><p><strong>3. Beregn sample size:</strong><br>Brug en sample size calculator til at finde ud af hvor meget traffic du skal bruge. Typisk skal du have minimum 100 conversions per variation.</p><p><strong>4. Koer testen laenge nok:</strong><br>Minimum 1-2 uger for at fange forskellige dage og tidspunkter. Stop ikke testen tidligt selvom du ser resultater.</p><p><strong>5. Analyser resultaterne:</strong><br>Er forskellen statistisk signifikant? Brug en significance calculator. Typisk skal du have minimum 95 procent confidence level.</p><h2>Common A/B testing mistakes</h2><p>Teste for mange ting paa en gang. Stoppe testen for tidligt. Ikke have nok traffic. Ignorere statistisk signifikans. Ikke dokumentere learnings.</p>',
        'category': categories['cro'],
    },
]

print("\n📝 Opretter artikler...")

# Opret Content artikler
for i, article_data in enumerate(content_articles, 1):
    try:
        body_json = json.dumps([{'type': 'paragraph', 'value': article_data['body']}])
        article = ArticlePage(
            title=article_data['title'],
            slug=article_data['slug'],
            summary=article_data['summary'],
            body=body_json,
            cover_image=default_image,
            category=article_data['category'],
            author='Redaktionen',
            published_at=datetime.now() - timedelta(days=i),
            live=True
        )
        homepage.add_child(instance=article)
        article.save_revision().publish()
        print(f"✅ Content: {article.title}")
    except Exception as e:
        print(f"❌ Fejl ved {article_data['title']}: {e}")

# Opret CRO artikler
for i, article_data in enumerate(cro_articles, 1):
    try:
        body_json = json.dumps([{'type': 'paragraph', 'value': article_data['body']}])
        article = ArticlePage(
            title=article_data['title'],
            slug=article_data['slug'],
            summary=article_data['summary'],
            body=body_json,
            cover_image=default_image,
            category=article_data['category'],
            author='Redaktionen',
            published_at=datetime.now() - timedelta(days=i+10),
            live=True
        )
        homepage.add_child(instance=article)
        article.save_revision().publish()
        print(f"✅ CRO: {article.title}")
    except Exception as e:
        print(f"❌ Fejl ved {article_data['title']}: {e}")

print("\n✅ Artikler oprettet! Tjekker status...")

# Vis status
for cat_key, cat in categories.items():
    count = ArticlePage.objects.filter(category=cat).count()
    print(f"{cat.name}: {count} artikler")

print(f"\nTotal artikler: {ArticlePage.objects.live().count()}")

