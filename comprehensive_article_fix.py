"""
Comprehensive script to fix all articles:
1. Remove duplicate images from all articles
2. Expand short articles with professional content
"""

from news.models import ArticlePage
import uuid

print('=== COMPREHENSIVE ARTICLE FIX ===\n')

# Step 1: Fix duplicate images in ALL articles
print('Step 1: Removing duplicate images...\n')
articles = ArticlePage.objects.filter(live=True).exclude(category__slug='podcasts')
duplicate_fixed = 0

for article in articles:
    body_list = list(article.body.raw_data) if article.body else []
    
    # Check for duplicate images
    image_ids = [b.get('value', {}).get('image') for b in body_list if b.get('type') == 'image']
    if len(image_ids) != len(set(image_ids)) and len(image_ids) > 0:
        # Remove duplicates
        seen_ids = set()
        new_body = []
        removed_count = 0
        
        for block in body_list:
            if block.get('type') == 'image':
                img_id = block.get('value', {}).get('image')
                if img_id not in seen_ids:
                    seen_ids.add(img_id)
                    new_body.append(block)
                else:
                    removed_count += 1
            else:
                new_body.append(block)
        
        if removed_count > 0:
            article.body = new_body
            revision = article.save_revision()
            revision.publish()
            duplicate_fixed += 1
            print(f'✓ {article.title[:45]}... → Removed {removed_count} duplicate images')

print(f'\n→ Fixed {duplicate_fixed} articles with duplicate images\n')

# Step 2: Expand short articles
print('Step 2: Expanding short articles...\n')

# Short article content - only the most critical ones
SHORT_ARTICLES = {
    'chatgpt-content-marketing-guide': '''<h2>Hvorfor ChatGPT revolutionerer content marketing</h2>
<p>ChatGPT kan producere content 10x hurtigere end mennesker, men kvalitet kræver de rigtige prompts og strategi. 67% af marketers bruger allerede AI til content creation og sparer gennemsnitligt 5 timer om ugen.</p>

<h2>Hvad ChatGPT kan og ikke kan</h2>
<p><strong>Hvad ChatGPT er god til:</strong> Blog post outlines, email marketing copy, social media captions, product descriptions, brainstorming ideer, omskrivning af eksisterende content, og SEO meta descriptions.</p>

<p><strong>Hvad ChatGPT IKKE er god til:</strong> Original research og data, brand voice uden træning, faktuel nøjagtighed (hallucinerer nogle gange), nuanceret storytelling, og emotionel dybde.</p>

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
<p>ChatGPT kan lave fejl. Verificer altid facts, statistikker og claims før publicering.</p>

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

<h2>Måling af ROI</h2>
<p><strong>Metrics at tracke:</strong> Tid sparet per content piece, content output (antal pieces per måned), engagement rates (sammenlign AI vs human content), SEO performance, og conversion rates.</p>

<p><strong>Typiske resultater:</strong> 50-70% tidsbesparelse, 3-5x mere content output, engagement rates typisk 80-90% af human-written content (hvis godt redigeret).</p>

<h2>Næste skridt</h2>
<p>Start med én content type (f.eks. social media posts). Lav 10 pieces med ChatGPT denne uge. Mål engagement vs dine normale posts. Iterer baseret på results.</p>''',
    
    'local-seo-guide-2024': '''<h2>Hvorfor Local SEO er kritisk</h2>
<p>For lokale virksomheder er Local SEO forskellen mellem succes og fiasko. 46% af alle Google søgninger har lokal intent, og 76% af folk der søger efter noget lokalt på deres smartphone besøger en virksomhed inden for 24 timer. 28% af lokale søgninger resulterer i et køb samme dag.</p>

<h2>Google My Business: Fundamentet</h2>
<p>Din GMB profil er det vigtigste element i Local SEO. Den vises i Google Maps, local pack (de 3 virksomheder der vises øverst), og knowledge panel.</p>

<h3>GMB optimering checklist</h3>
<p><strong>1. Komplet profil:</strong> Virksomhedsnavn (præcis som på hjemmeside), kategori (primær + sekundære), adresse (verificeret), telefonnummer, hjemmeside URL, åbningstider (inkl. special hours for helligdage), beskrivelse (750 karakterer, keyword-optimeret), og attributter (f.eks. "wheelchair accessible", "outdoor seating").</p>

<p><strong>2. Billeder:</strong> Upload minimum 10 high-quality billeder. Inkluder: Exterior, interior, produkter, team, logo. Upload nye billeder hver måned (Google favoriserer fresh content). Optimal størrelse: 720x720 pixels minimum.</p>

<p><strong>3. Posts:</strong> Post minimum 1x om ugen. Post types: Offers, events, products, updates. Inkluder CTA button og brug keywords naturligt.</p>

<p><strong>4. Q&A:</strong> Seed din egen Q&A sektion med common questions. Monitor og besvar nye spørgsmål inden for 24 timer.</p>

<h2>NAP Consistency</h2>
<p>NAP = Name, Address, Phone number. Dette skal være 100% identisk på tværs af hele internettet: Hjemmeside (footer, contact page, about page), Google My Business, Facebook Business Page, alle online directories (Yelp, Yellow Pages, etc.), citations, og schema markup på hjemmeside.</p>

<p><strong>Common mistakes:</strong> "Street" vs "St.", "Suite 100" vs "#100", forskellige telefonnumre, gamle adresser ikke opdateret.</p>

<p><strong>Fix:</strong> Lav en NAP audit. Brug tools som Moz Local eller BrightLocal til at finde inconsistencies.</p>

<h2>Local Keywords</h2>
<p><strong>Explicit local keywords:</strong> "Frisør København", "Restaurant Aarhus", "Tømrer Odense"</p>
<p><strong>Implicit local keywords:</strong> "Frisør nær mig", "Bedste restaurant", "Tømrer i nærheden"</p>
<p><strong>Neighborhood keywords:</strong> "Frisør Vesterbro", "Restaurant Nørrebro", "Tømrer Frederiksberg"</p>

<h3>Hvor skal keywords være?</h3>
<p>Title tags: "Frisør København | [Brand Name]", H1: "Københavns bedste frisør", meta description, content (naturligt, ikke keyword stuffing), image alt text, og URL slugs.</p>

<h2>Local Citations</h2>
<p>Citations = mentions af din virksomhed på andre websites (med NAP info).</p>

<p><strong>Structured citations:</strong> Online directories som Yelp, Yellow Pages, Bing Places, Apple Maps, TripAdvisor (for restaurants/hotels), og industry-specific directories.</p>

<p><strong>Unstructured citations:</strong> Mentions i artikler, blog posts, news sites.</p>

<h3>Citation building strategi</h3>
<p><strong>Step 1:</strong> Claim og optimér top directories (Google, Bing, Apple, Yelp)<br>
<strong>Step 2:</strong> Find industry-specific directories<br>
<strong>Step 3:</strong> Local directories (f.eks. lokale erhvervsforeninger)<br>
<strong>Step 4:</strong> Monitor for nye citation opportunities</p>

<p><strong>Kvalitet > Kvantitet:</strong> 10 high-quality citations er bedre end 100 spam directories.</p>

<h2>Reviews Management</h2>
<p>Reviews påvirker både rankings og conversion rates. 88% af consumers stoler på online reviews lige så meget som personal recommendations.</p>

<h3>Review acquisition strategi</h3>
<p><strong>1. Spørg på det rigtige tidspunkt:</strong> Efter positiv interaction, efter succesfuld service/køb, når kunden udtrykker tilfredshed.</p>

<p><strong>2. Gør det nemt:</strong> Send direkte link til Google review, QR code i butik, email follow-up med link, SMS reminder.</p>

<p><strong>3. Incentivize (lovligt):</strong> Konkurrence blandt alle reviewers (ikke kun positive), donation til velgørenhed for hver review. IKKE: Betaling for positive reviews (imod Google's policies).</p>

<h3>Review response best practices</h3>
<p><strong>Positive reviews:</strong> Responder inden for 24-48 timer, vær personlig (brug kundens navn), tak for specifik feedback, inviter til at komme igen.</p>

<p><strong>Negative reviews:</strong> Responder ASAP (inden for 24 timer), vær professionel og empatisk, undskyld for problemet, tilbyd løsning, tag samtalen offline hvis nødvendigt. ALDRIG: Vær defensiv eller argumenter.</p>

<h2>On-page Local SEO</h2>
<h3>Location pages</h3>
<p>Hvis du har flere locations, lav dedikeret page for hver med: Unique content (ikke duplicate), NAP info, embedded Google Map, location-specific testimonials, unique images fra den location, driving directions, parking info, og local landmarks.</p>

<h3>Schema markup</h3>
<p>Implementer LocalBusiness schema med: Name, address, phone, opening hours, price range, accepted payment methods, image, og geo coordinates.</p>

<h2>Tracking og metrics</h2>
<p><strong>Google My Business Insights:</strong> Search queries, views (search vs maps), actions (calls, website clicks, direction requests), photo views.</p>

<p><strong>Google Analytics:</strong> Organic traffic fra local keywords, conversion rate fra local traffic.</p>

<p><strong>Rank tracking:</strong> Track rankings for local keywords, monitor local pack positions, track competitors.</p>

<h2>Næste skridt</h2>
<p>1. Claim og optimér din Google My Business profil<br>
2. Audit din NAP consistency<br>
3. Implementer review acquisition strategi<br>
4. Byg 10 high-quality citations denne måned</p>'''
}

expanded_count = 0

for slug, content in SHORT_ARTICLES.items():
    try:
        article = ArticlePage.objects.get(slug=slug)
        body_list = list(article.body.raw_data) if article.body else []
        
        # Check if article is short
        total_chars = sum(len(b.get('value', '')) for b in body_list if b.get('type') == 'rich_text')
        
        if total_chars < 3000:
            # Keep existing images
            existing_images = [b for b in body_list if b.get('type') == 'image']
            
            # Create new body with expanded content
            new_body = [
                {
                    'type': 'rich_text',
                    'value': content,
                    'id': body_list[0]['id'] if body_list else str(uuid.uuid4())
                }
            ]
            
            # Add back the images
            for img in existing_images[:2]:  # Keep max 2 images
                new_body.append(img)
            
            article.body = new_body
            revision = article.save_revision()
            revision.publish()
            expanded_count += 1
            print(f'✓ {article.title[:45]}... → Expanded from {total_chars} to {len(content)} chars')
    except ArticlePage.DoesNotExist:
        print(f'✗ Article not found: {slug}')

print(f'\n→ Expanded {expanded_count} short articles\n')

print('=== DONE! ===')
print(f'Total fixes: {duplicate_fixed} duplicates removed, {expanded_count} articles expanded')

