#!/usr/bin/env python3
"""
Script to fix all articles:
1. Remove duplicate images
2. Expand short articles with proper content
3. Ensure professional structure
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, '/Users/mikkelfunder/Marketingnyt.dk')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketingnyt.settings')
django.setup()

from news.models import ArticlePage

# Articles that need fixing with their full professional content
ARTICLE_CONTENT = {
    'chatgpt-content-marketing-guide': {
        'title': 'ChatGPT til content marketing: Komplet guide',
        'content': '''<h2>Hvorfor ChatGPT er game-changer for content marketing</h2>
<p>ChatGPT kan producere content 10x hurtigere end mennesker. Men kvalitet kræver de rigtige prompts og strategi.</p>

<p><strong>Fakta:</strong> 67% af marketers bruger allerede AI til content creation. De sparer gennemsnitligt 5 timer om ugen.</p>

<h2>Hvad ChatGPT kan (og ikke kan)</h2>

<h3>Hvad ChatGPT er god til:</h3>
<p>• Blog post outlines og strukturer<br>
• Email marketing copy<br>
• Social media captions<br>
• Product descriptions<br>
• Brainstorming ideer<br>
• Omskrivning og forbedring af eksisterende content<br>
• SEO meta descriptions</p>

<h3>Hvad ChatGPT IKKE er god til:</h3>
<p>• Original research og data<br>
• Brand voice uden træning<br>
• Faktuel nøjagtighed (hallucinerer nogle gange)<br>
• Nuanceret storytelling<br>
• Emotionel dybde</p>

<h2>De 5 vigtigste prompt-teknikker</h2>

<h3>1. Kontekst først</h3>
<p><strong>Dårlig prompt:</strong> "Skriv en blog post om SEO"</p>
<p><strong>God prompt:</strong> "Du er en SEO ekspert med 10 års erfaring. Skriv en 1500-ords blog post til B2B SaaS virksomheder om hvordan de kan forbedre deres on-page SEO. Målgruppen er marketing managers uden teknisk baggrund. Tone: Professionel men tilgængelig."</p>

<h3>2. Specificer format</h3>
<p>"Strukturer artiklen med: Intro (100 ord), 5 hovedsektioner med H2 headings, hver sektion 250 ord, afslut med 3 konkrete action steps."</p>

<h3>3. Giv eksempler</h3>
<p>"Her er et eksempel på vores brand voice: [indsæt eksempel]. Skriv i samme stil."</p>

<h3>4. Iterer og forbedr</h3>
<p>Start bredt, bed derefter om forbedringer: "Gør intro mere engaging", "Tilføj konkrete eksempler", "Gør sproget mere conversational".</p>

<h3>5. Fact-check altid</h3>
<p>ChatGPT kan lave fejl. Verificer altid facts, statistikker og claims.</p>

<h2>Content workflows med ChatGPT</h2>

<h3>Blog post workflow</h3>
<p><strong>Step 1:</strong> Keyword research (brug andre tools)<br>
<strong>Step 2:</strong> ChatGPT: "Lav 10 blog post ideer om [topic] der targeter keyword [keyword]"<br>
<strong>Step 3:</strong> ChatGPT: "Lav detaljeret outline til: [valgt ide]"<br>
<strong>Step 4:</strong> ChatGPT: "Skriv sektion 1 baseret på outline"<br>
<strong>Step 5:</strong> Manuelt: Rediger, tilføj brand voice, verificer facts<br>
<strong>Step 6:</strong> ChatGPT: "Skriv 5 meta descriptions (max 155 karakterer)"</p>

<h3>Email marketing workflow</h3>
<p><strong>Prompt:</strong> "Skriv 3 variationer af en promotional email for [produkt]. Målgruppe: [beskrivelse]. Inkluder: Catchy subject line, personlig intro, 3 benefits, clear CTA. Tone: [tone]. Max 150 ord."</p>

<h3>Social media workflow</h3>
<p><strong>Prompt:</strong> "Lav 10 LinkedIn posts baseret på denne blog post: [paste blog]. Hver post skal være 100-150 ord, inkludere en hook i første linje, og ende med et spørgsmål til engagement."</p>

<h2>Advanced ChatGPT teknikker</h2>

<h3>Custom instructions</h3>
<p>I ChatGPT settings, tilføj custom instructions med din brand voice, målgruppe, og preferred tone. Så behøver du ikke gentage det i hver prompt.</p>

<h3>Chain of thought prompting</h3>
<p>"Før du skriver artiklen, lav først: 1) Audience analysis, 2) Key messages, 3) Outline. Derefter skriv artiklen baseret på dette."</p>

<h3>Role-playing</h3>
<p>"Du er en erfaren copywriter der har skrevet for [brands]. Skriv som om du taler direkte til [persona]."</p>

<h2>ChatGPT + andre tools</h2>

<p><strong>ChatGPT + Surfer SEO:</strong> Brug Surfer til keyword research og content brief, ChatGPT til at skrive content baseret på briefen.</p>

<p><strong>ChatGPT + Grammarly:</strong> ChatGPT skriver, Grammarly polerer og tjekker tone.</p>

<p><strong>ChatGPT + Canva:</strong> ChatGPT laver social media copy, Canva laver visuals.</p>

<h2>Etik og best practices</h2>

<p><strong>Disclosure:</strong> Vær transparent hvis content er AI-genereret (afhænger af din industri og audience).</p>

<p><strong>Originalitet:</strong> Brug ChatGPT som starting point, ikke final product. Tilføj altid din egen ekspertise og perspektiv.</p>

<p><strong>Plagiarism check:</strong> Kør AI-genereret content gennem plagiarism checker.</p>

<p><strong>Human review:</strong> Lad altid en person reviewe før publicering.</p>

<h2>Måling af ROI</h2>

<p><strong>Metrics at tracke:</strong><br>
• Tid sparet per content piece<br>
• Content output (antal pieces per måned)<br>
• Engagement rates (sammenlign AI vs human content)<br>
• SEO performance<br>
• Conversion rates</p>

<p><strong>Typiske resultater:</strong><br>
• 50-70% tidsbesparelse<br>
• 3-5x mere content output<br>
• Engagement rates: Typisk 80-90% af human-written content (hvis godt redigeret)</p>

<h2>Næste skridt</h2>

<p>Start med én content type (f.eks. social media posts). Lav 10 pieces med ChatGPT denne uge. Mål engagement vs dine normale posts. Iterer baseret på results.</p>'''
    },
    
    'local-seo-guide': {
        'title': 'Local SEO: Dominér lokale søgninger',
        'content': '''<h2>Hvorfor Local SEO er kritisk</h2>
<p>For lokale virksomheder er Local SEO forskellen mellem succes og fiasko. 46% af alle Google søgninger har lokal intent, og 76% af folk der søger efter noget lokalt på deres smartphone besøger en virksomhed inden for 24 timer.</p>

<p><strong>Fakta:</strong> 28% af lokale søgninger resulterer i et køb samme dag.</p>

<h2>Google My Business: Fundamentet</h2>

<p>Din GMB profil er det vigtigste element i Local SEO. Den vises i Google Maps, local pack (de 3 virksomheder der vises øverst), og knowledge panel.</p>

<h3>GMB optimering checklist</h3>

<p><strong>1. Komplet profil:</strong><br>
• Virksomhedsnavn (præcis som på hjemmeside)<br>
• Kategori (primær + sekundære)<br>
• Adresse (verificeret)<br>
• Telefonnummer<br>
• Hjemmeside URL<br>
• Åbningstider (inkl. special hours for helligdage)<br>
• Beskrivelse (750 karakterer, keyword-optimeret)<br>
• Attributter (f.eks. "wheelchair accessible", "outdoor seating")</p>

<p><strong>2. Billeder:</strong><br>
• Upload minimum 10 high-quality billeder<br>
• Inkluder: Exterior, interior, produkter, team, logo<br>
• Upload nye billeder hver måned (Google favoriserer fresh content)<br>
• Optimal størrelse: 720x720 pixels minimum</p>

<p><strong>3. Posts:</strong><br>
• Post minimum 1x om ugen<br>
• Post types: Offers, events, products, updates<br>
• Inkluder CTA button<br>
• Brug keywords naturligt</p>

<p><strong>4. Q&A:</strong><br>
• Seed din egen Q&A sektion med common questions<br>
• Monitor og besvar nye spørgsmål inden for 24 timer</p>

<h2>NAP Consistency</h2>

<p>NAP = Name, Address, Phone number. Dette skal være 100% identisk på tværs af hele internettet.</p>

<p><strong>Hvor NAP skal være konsistent:</strong><br>
• Hjemmeside (footer, contact page, about page)<br>
• Google My Business<br>
• Facebook Business Page<br>
• Alle online directories (Yelp, Yellow Pages, etc.)<br>
• Citations<br>
• Schema markup på hjemmeside</p>

<p><strong>Common mistakes:</strong><br>
• "Street" vs "St."<br>
• "Suite 100" vs "#100"<br>
• Forskellige telefonnumre<br>
• Gamle adresser ikke opdateret</p>

<p><strong>Fix:</strong> Lav en NAP audit. Brug tools som Moz Local eller BrightLocal til at finde inconsistencies.</p>

<h2>Local Keywords</h2>

<p>Optimér for keywords der inkluderer location.</p>

<h3>Keyword typer</h3>

<p><strong>1. Explicit local keywords:</strong><br>
• "Frisør København"<br>
• "Restaurant Aarhus"<br>
• "Tømrer Odense"</p>

<p><strong>2. Implicit local keywords:</strong><br>
• "Frisør nær mig"<br>
• "Bedste restaurant"<br>
• "Tømrer i nærheden"</p>

<p><strong>3. Neighborhood keywords:</strong><br>
• "Frisør Vesterbro"<br>
• "Restaurant Nørrebro"<br>
• "Tømrer Frederiksberg"</p>

<h3>Hvor skal keywords være?</h3>

<p>• Title tags: "Frisør København | [Brand Name]"<br>
• H1: "Københavns bedste frisør"<br>
• Meta description<br>
• Content (naturligt, ikke keyword stuffing)<br>
• Image alt text<br>
• URL slugs</p>

<h2>Local Citations</h2>

<p>Citations = mentions af din virksomhed på andre websites (med NAP info).</p>

<h3>Typer af citations</h3>

<p><strong>1. Structured citations:</strong> Online directories<br>
• Yelp<br>
• Yellow Pages<br>
• Bing Places<br>
• Apple Maps<br>
• TripAdvisor (for restaurants/hotels)<br>
• Industry-specific directories</p>

<p><strong>2. Unstructured citations:</strong> Mentions i artikler, blog posts, news sites</p>

<h3>Citation building strategi</h3>

<p><strong>Step 1:</strong> Claim og optimér top directories (Google, Bing, Apple, Yelp)<br>
<strong>Step 2:</strong> Find industry-specific directories<br>
<strong>Step 3:</strong> Local directories (f.eks. lokale erhvervsforeninger)<br>
<strong>Step 4:</strong> Monitor for nye citation opportunities</p>

<p><strong>Kvalitet > Kvantitet:</strong> 10 high-quality citations er bedre end 100 spam directories.</p>

<h2>Reviews Management</h2>

<p>Reviews påvirker både rankings og conversion rates. 88% af consumers stoler på online reviews lige så meget som personal recommendations.</p>

<h3>Review acquisition strategi</h3>

<p><strong>1. Spørg på det rigtige tidspunkt:</strong><br>
• Efter positiv interaction<br>
• Efter succesfuld service/køb<br>
• Når kunden udtrykker tilfredshed</p>

<p><strong>2. Gør det nemt:</strong><br>
• Send direkte link til Google review<br>
• QR code i butik<br>
• Email follow-up med link<br>
• SMS reminder</p>

<p><strong>3. Incentivize (lovligt):</strong><br>
• Konkurrence blandt alle reviewers (ikke kun positive)<br>
• Donation til velgørenhed for hver review<br>
• IKKE: Betaling for positive reviews (imod Google's policies)</p>

<h3>Review response best practices</h3>

<p><strong>Positive reviews:</strong><br>
• Responder inden for 24-48 timer<br>
• Vær personlig (brug kundens navn)<br>
• Tak for specifik feedback<br>
• Inviter til at komme igen</p>

<p><strong>Negative reviews:</strong><br>
• Responder ASAP (inden for 24 timer)<br>
• Vær professionel og empatisk<br>
• Undskyld for problemet<br>
• Tilbyd løsning<br>
• Tag samtalen offline hvis nødvendigt<br>
• ALDRIG: Vær defensiv eller argumenter</p>

<h2>On-page Local SEO</h2>

<h3>Location pages</h3>

<p>Hvis du har flere locations, lav dedikeret page for hver:</p>

<p><strong>Struktur:</strong><br>
• Unique content (ikke duplicate)<br>
• NAP info<br>
• Embedded Google Map<br>
• Location-specific testimonials<br>
• Unique images fra den location<br>
• Driving directions<br>
• Parking info<br>
• Local landmarks</p>

<h3>Schema markup</h3>

<p>Implementer LocalBusiness schema:</p>

<p><strong>Inkluder:</strong><br>
• Name<br>
• Address<br>
• Phone<br>
• Opening hours<br>
• Price range<br>
• Accepted payment methods<br>
• Image<br>
• Geo coordinates</p>

<h2>Local link building</h2>

<p><strong>Strategier:</strong><br>
• Sponsor lokale events<br>
• Partner med andre lokale businesses<br>
• Skriv guest posts til lokale blogs<br>
• Få omtale i lokale medier<br>
• Join lokale erhvervsforeninger<br>
• Deltag i community events</p>

<h2>Tracking og metrics</h2>

<p><strong>Google My Business Insights:</strong><br>
• Search queries<br>
• Views (search vs maps)<br>
• Actions (calls, website clicks, direction requests)<br>
• Photo views</p>

<p><strong>Google Analytics:</strong><br>
• Organic traffic fra local keywords<br>
• Conversion rate fra local traffic</p>

<p><strong>Rank tracking:</strong><br>
• Track rankings for local keywords<br>
• Monitor local pack positions<br>
• Track competitors</p>

<h2>Næste skridt</h2>

<p>1. Claim og optimér din Google My Business profil<br>
2. Audit din NAP consistency<br>
3. Implementer review acquisition strategi<br>
4. Byg 10 high-quality citations denne måned</p>'''
    }
}

def fix_article(article):
    """Fix a single article"""
    slug = article.slug
    body_list = list(article.body.raw_data) if article.body else []
    
    # Check for duplicate images
    image_blocks = [b for b in body_list if b.get('type') == 'image']
    if len(image_blocks) > 0:
        image_ids = [b.get('value', {}).get('image') for b in image_blocks]
        if len(image_ids) != len(set(image_ids)):
            # Remove duplicate images - keep only unique ones
            seen_ids = set()
            new_body = []
            for block in body_list:
                if block.get('type') == 'image':
                    img_id = block.get('value', {}).get('image')
                    if img_id not in seen_ids:
                        seen_ids.add(img_id)
                        new_body.append(block)
                else:
                    new_body.append(block)
            body_list = new_body
            print(f'  → Removed duplicate images')
    
    # Check if article needs content expansion
    total_chars = sum(len(b.get('value', '')) for b in body_list if b.get('type') == 'rich_text')
    
    if slug in ARTICLE_CONTENT and total_chars < 3000:
        # Replace with full professional content
        content_data = ARTICLE_CONTENT[slug]
        body_list = [
            {
                'type': 'rich_text',
                'value': content_data['content'],
                'id': body_list[0]['id'] if body_list else str(__import__('uuid').uuid4())
            }
        ]
        # Keep the 2 images if they exist
        image_blocks = [b for b in list(article.body.raw_data) if b.get('type') == 'image']
        if len(image_blocks) >= 2:
            body_list.append(image_blocks[0])
            body_list.append(image_blocks[1])
        
        print(f'  → Expanded content from {total_chars} to {len(content_data["content"])} chars')
    
    return body_list

def main():
    print('=== FIXING ALL ARTICLES ===\n')
    
    articles = ArticlePage.objects.filter(live=True).exclude(category__slug='podcasts')
    fixed_count = 0
    
    for article in articles:
        body_list = list(article.body.raw_data) if article.body else []
        
        # Check if needs fixing
        image_ids = [b.get('value', {}).get('image') for b in body_list if b.get('type') == 'image']
        has_duplicates = len(image_ids) != len(set(image_ids))
        total_chars = sum(len(b.get('value', '')) for b in body_list if b.get('type') == 'rich_text')
        needs_expansion = article.slug in ARTICLE_CONTENT and total_chars < 3000
        
        if has_duplicates or needs_expansion:
            print(f'\nFixing: {article.title[:50]}...')
            new_body = fix_article(article)
            
            article.body = new_body
            revision = article.save_revision()
            revision.publish()
            
            fixed_count += 1
            print(f'  ✓ Published')
    
    print(f'\n=== FÆRDIG! {fixed_count} artikler fixet ===')

if __name__ == '__main__':
    main()

