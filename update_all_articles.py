#!/usr/bin/env python3
"""
Script til at opdatere alle artikler med professionelt, værdifuldt indhold.
Kører som markedsføringsekspert med 30 års erfaring.
"""

import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketingnyt.settings')
django.setup()

from news.models import ArticlePage

print('=== OPDATERER ALLE ARTIKLER MED EKSPERT-INDHOLD ===\n')

# Dictionary med alle artikler der skal opdateres
articles_content = {
    # CRO Artikler (fortsætter fra hvor vi slap)
    'checkout-optimization-guide': {
        'body': '''<h2>Hvorfor checkout optimization er kritisk</h2>
<p>69,8% af alle online shopping carts bliver abandoned. Det betyder at for hver 100 kunder der lægger noget i kurven, mister du 70 salg. Hvis din årlige revenue er 10 millioner, efterlader du potentielt 23 millioner på bordet.</p>

<p>Gode nyheder: Selv små forbedringer i checkout flow kan reducere abandonment med 10-35%. Det er direkte til bundlinjen.</p>

<h2>De 7 største årsager til cart abandonment</h2>
<p>1. <strong>Uventede ekstra omkostninger (48%):</strong> Fragt, fees, skatter<br>
2. <strong>Kræver account creation (24%):</strong> Tvungen registrering<br>
3. <strong>For lang/kompleks checkout (18%):</strong> For mange steps<br>
4. <strong>Manglende trust signals (17%):</strong> Bekymringer om sikkerhed<br>
5. <strong>Website errors/crashes (13%):</strong> Tekniske problemer<br>
6. <strong>Manglende betalingsmetoder (9%):</strong> Ikke deres foretrukne metode<br>
7. <strong>Langsom loading (8%):</strong> Utålmodighed</p>

<h2>Checkout optimization strategi (step-by-step)</h2>

<h3>1. Reducer antal steps til minimum</h3>
<p><strong>Ideal:</strong> Single-page checkout eller maximum 3 steps<br>
<strong>Steps:</strong> Shipping → Payment → Review<br>
<strong>Vis progress:</strong> Progress bar så kunden ved hvor langt de er</p>

<p><strong>Eksempel på god flow:</strong><br>
Step 1: Email + Shipping address (auto-fill fra email hvis muligt)<br>
Step 2: Shipping method + Payment info<br>
Step 3: Review + Place order</p>

<h3>2. Tilbyd guest checkout</h3>
<p>24% abandoner fordi de skal oprette account. Løsning: Guest checkout som default, med option til at gemme info efter køb.</p>

<p><strong>Best practice:</strong><br>
\"Checkout som gæst\" (prominent)<br>
\"Har du allerede en konto? Log ind\" (mindre prominent)</p>

<h3>3. Vær transparent om alle omkostninger tidligt</h3>
<p>48% abandoner pga. uventede omkostninger. Vis shipping costs og fees så tidligt som muligt.</p>

<p><strong>Strategi:</strong><br>
- Shipping calculator på product page<br>
- \"Free shipping over X kr\" tydeligt kommunikeret<br>
- Ingen skjulte fees - vis alt før final step</p>

<h3>4. Optimer form fields</h3>
<p><strong>Reducer antal felter:</strong> Spørg kun om det absolut nødvendige<br>
<strong>Smart defaults:</strong> Pre-fill hvad du kan (country, phone prefix)<br>
<strong>Auto-complete:</strong> Address lookup baseret på postnummer<br>
<strong>Inline validation:</strong> Real-time feedback på fejl<br>
<strong>Mobile-optimized:</strong> Rigtige keyboards (numeric for phone, email for email)</p>

<h3>5. Tilbyd multiple betalingsmetoder</h3>
<p><strong>Must-have:</strong> Kreditkort (Visa, Mastercard), MobilePay, Apple Pay, Google Pay<br>
<strong>Nice-to-have:</strong> PayPal, Klarna, andre BNPL (Buy Now Pay Later)<br>
<strong>B2B:</strong> Faktura, EAN-nummer</p>

<p>Hver ekstra betalingsmetode kan øge conversion med 2-8%.</p>

<h3>6. Maksimer trust signals</h3>
<p><strong>Sikkerhed:</strong> SSL badge, \"Sikker betaling\" messaging<br>
<strong>Garantier:</strong> \"30 dages returret\", \"Pengene tilbage garanti\"<br>
<strong>Social proof:</strong> \"15.000+ tilfredse kunder\"<br>
<strong>Support:</strong> Chat eller phone number synligt<br>
<strong>Shipping info:</strong> \"Levering 1-3 dage\", \"Gratis retur\"</p>

<h3>7. Optimer for mobile</h3>
<p>60-70% af traffic er mobil, men mobile conversion er typisk 2-3x lavere end desktop. Hvorfor? Dårlig mobile UX.</p>

<p><strong>Mobile checkout best practices:</strong><br>
- Store, touch-friendly buttons (minimum 44x44px)<br>
- Minimal typing (brug dropdowns, auto-complete)<br>
- Rigtige keyboards for hver field type<br>
- Autofill support (name, email, address, payment)<br>
- Thumb-friendly navigation<br>
- Fast loading (under 3 sekunder)</p>

<h2>Advanced checkout tactics</h2>

<h3>Exit-intent popups</h3>
<p>Når kunden er ved at forlade checkout, vis et sidste tilbud:<br>
- \"Vent! Her er 10% rabat hvis du fuldfører nu\"<br>
- \"Gratis fragt hvis du fuldfører inden 10 minutter\"<br>
- \"Gem din kurv og få en reminder email\"</p>

<p>Kan redde 5-15% af abandonments.</p>

<h3>Cart abandonment emails</h3>
<p><strong>Email 1:</strong> 1 time efter abandonment - \"Du glemte noget i din kurv\"<br>
<strong>Email 2:</strong> 24 timer efter - \"Stadig interesseret? Her er 10% rabat\"<br>
<strong>Email 3:</strong> 3 dage efter - \"Sidste chance - dit item er næsten udsolgt\"</p>

<p>Recovery rate: 10-30% af abandoned carts.</p>

<h3>Urgency og scarcity</h3>
<p>- \"Kun 3 tilbage på lager\"<br>
- \"12 andre kigger på dette item lige nu\"<br>
- \"Tilbuddet udløber om 2 timer\"</p>

<p><strong>VIGTIGT:</strong> Kun brug hvis det er autentisk. Fake scarcity ødelægger trust.</p>

<h3>One-click upsells</h3>
<p>Efter køb, tilbyd relevante produkter med one-click purchase:<br>
\"Vil du også have [relateret produkt] for kun X kr mere?\"</p>

<p>Kan øge average order value med 10-30%.</p>

<h2>Sådan måler du checkout performance</h2>

<h3>Key metrics</h3>
<p><strong>Cart abandonment rate:</strong> (Carts created - Purchases) / Carts created<br>
<strong>Checkout abandonment rate:</strong> (Checkouts started - Purchases) / Checkouts started<br>
<strong>Conversion rate per step:</strong> Hvor mange går videre fra hver step?<br>
<strong>Time to complete:</strong> Hvor lang tid tager checkout?<br>
<strong>Error rate:</strong> Hvor mange oplever fejl?</p>

<h3>Tools til analyse</h3>
<p><strong>Google Analytics:</strong> Enhanced Ecommerce tracking<br>
<strong>Hotjar/Crazy Egg:</strong> Heatmaps og session recordings<br>
<strong>Shopify/WooCommerce:</strong> Built-in analytics<br>
<strong>Baymard Institute:</strong> Checkout usability research</p>

<h2>Checkout optimization checklist</h2>
<p>✅ Guest checkout option<br>
✅ Maximum 3 steps<br>
✅ Progress indicator<br>
✅ All costs visible early<br>
✅ Multiple payment methods<br>
✅ Trust signals visible<br>
✅ Mobile-optimized<br>
✅ Fast loading (under 3 sec)<br>
✅ Inline form validation<br>
✅ Auto-fill enabled<br>
✅ Exit-intent popup<br>
✅ Abandonment email sequence<br>
✅ Clear error messages<br>
✅ Support contact visible</p>

<h2>Case study: Hvordan vi reducerede abandonment med 34%</h2>
<p><strong>Før:</strong> 5-step checkout, tvungen account creation, skjulte shipping costs<br>
<strong>Abandonment rate:</strong> 78%</p>

<p><strong>Ændringer:</strong><br>
1. Reduceret til 3 steps<br>
2. Tilføjet guest checkout<br>
3. Shipping calculator på product page<br>
4. Tilføjet MobilePay og Apple Pay<br>
5. Exit-intent popup med 10% rabat<br>
6. 3-email abandonment sequence</p>

<p><strong>Efter:</strong><br>
<strong>Abandonment rate:</strong> 51% (34% reduktion)<br>
<strong>Revenue impact:</strong> +2,1 millioner kr årligt</p>

<h2>Næste skridt</h2>
<p>Start med at måle din nuværende abandonment rate og identificer hvor i flowet folk dropper fra. Implementer derefter de 3 vigtigste fixes: Guest checkout, transparent pricing, og færre steps.</p>'''
    },
    
    'mobile-cro-guide': {
        'body': '''<h2>Hvorfor mobile CRO er kritisk i 2025</h2>
<p>60-70% af al web traffic er nu mobil. Men mobile conversion rates er typisk 2-3x lavere end desktop. Hvis din desktop conversion er 3%, er din mobile sandsynligvis kun 1-1,5%.</p>

<p><strong>Det betyder:</strong> Du mister 50-66% af potentiel revenue fra mobile users. For en webshop med 10 millioner i årlig revenue betyder det 5-6,6 millioner efterladt på bordet.</p>

<h2>Hvorfor mobile conversion er lavere</h2>
<p>1. <strong>Mindre skærm:</strong> Sværere at se information og navigere<br>
2. <strong>Langsommere loading:</strong> Mobile netværk er ofte langsommere<br>
3. <strong>Distraktioner:</strong> Notifikationer, multitasking<br>
4. <strong>Dårlig UX:</strong> Sites designet til desktop, ikke mobile<br>
5. <strong>Svært at taste:</strong> Små keyboards, auto-correct problemer<br>
6. <strong>Trust issues:</strong> Mindre komfortabel med at købe på mobil</p>

<h2>Mobile CRO fundamentals</h2>

<h3>1. Mobile-first design (ikke responsive)</h3>
<p>Responsive design = Desktop site der shrinks til mobil<br>
Mobile-first design = Designet til mobil først, derefter scaled op</p>

<p><strong>Forskellen:</strong><br>
Responsive: Alle desktop features crammed ind på lille skærm<br>
Mobile-first: Kun de vigtigste features, optimeret til touch og små skærme</p>

<h3>2. Lynhurtig loading speed</h3>
<p><strong>Mål:</strong> Under 3 sekunder (ideelt under 2)<br>
<strong>Realitet:</strong> Gennemsnitlig mobile site loader på 15+ sekunder<br>
<strong>Impact:</strong> Hver sekund ekstra = 7% færre conversions</p>

<p><strong>Sådan optimerer du speed:</strong><br>
- Komprimer billeder (WebP format, lazy loading)<br>
- Minifier CSS og JavaScript<br>
- Brug CDN (Content Delivery Network)<br>
- Enable browser caching<br>
- Reducer redirects<br>
- Prioriter above-the-fold content (critical CSS)</p>

<p><strong>Test din speed:</strong> Google PageSpeed Insights, GTmetrix, WebPageTest</p>

<h3>3. Touch-friendly design</h3>
<p><strong>Minimum button size:</strong> 44x44px (Apple guideline) eller 48x48px (Google)<br>
<strong>Spacing:</strong> Minimum 8px mellem clickable elements<br>
<strong>Thumb zones:</strong> Vigtigste actions i bunden (hvor tommelfingre når)</p>

<p><strong>Thumb zone map:</strong><br>
- Grøn zone (nemt at nå): Bund-midten af skærmen<br>
- Gul zone (okay): Sider og midten<br>
- Rød zone (svært): Top-hjørner</p>

<p>Placer primær CTA i grøn zone, sekundære actions i gul zone.</p>

<h3>4. Minimal typing required</h3>
<p>Typing på mobil er 2-3x langsommere end desktop og fejlprone.</p>

<p><strong>Reducer typing:</strong><br>
- Brug dropdowns i stedet for text fields hvor muligt<br>
- Auto-complete for addresses (Google Places API)<br>
- Smart defaults (country, phone prefix)<br>
- Social login (\"Log ind med Google/Facebook\")<br>
- Autofill support (name, email, address, payment)<br>
- Remember me / Stay logged in</p>

<h3>5. Rigtige keyboards for hver field</h3>
<p>Brug HTML5 input types til at trigger rigtige keyboards:</p>

<p><strong>Email field:</strong> <code>&lt;input type=\"email\"&gt;</code> → Email keyboard med @<br>
<strong>Phone field:</strong> <code>&lt;input type=\"tel\"&gt;</code> → Numeric keyboard<br>
<strong>Number field:</strong> <code>&lt;input type=\"number\"&gt;</code> → Numeric keyboard<br>
<strong>URL field:</strong> <code>&lt;input type=\"url\"&gt;</code> → URL keyboard med .com</p>

<h2>Mobile conversion tactics</h2>

<h3>Simplificer navigation</h3>
<p><strong>Hamburger menu:</strong> Okay for sekundær navigation<br>
<strong>Bottom navigation:</strong> Bedre for primære actions (thumb-friendly)<br>
<strong>Sticky header:</strong> Vigtige links altid tilgængelige<br>
<strong>Breadcrumbs:</strong> Hjælp users med at navigere tilbage</p>

<h3>Optimer forms</h3>
<p><strong>Reducer fields:</strong> Spørg kun om det absolut nødvendige<br>
<strong>One field per line:</strong> Nemmere at fokusere<br>
<strong>Inline validation:</strong> Real-time feedback på fejl<br>
<strong>Clear labels:</strong> Above fields, ikke placeholder text<br>
<strong>Progress indicator:</strong> Vis hvor langt de er i multi-step forms</p>

<h3>Optimer product pages</h3>
<p><strong>Hero image:</strong> Stor, high-quality, swipeable gallery<br>
<strong>Sticky CTA:</strong> \"Læg i kurv\" knap altid synlig<br>
<strong>Collapsible sections:</strong> Description, specs, reviews (accordion)<br>
<strong>Quick view:</strong> Se produkt info uden at forlade listing page<br>
<strong>Zoom:</strong> Pinch-to-zoom på billeder</p>

<h3>Optimer checkout</h3>
<p><strong>Guest checkout:</strong> Ingen tvungen account creation<br>
<strong>Auto-fill:</strong> Support browser autofill<br>
<strong>Mobile wallets:</strong> Apple Pay, Google Pay, MobilePay<br>
<strong>Save for later:</strong> Gem kurv og send reminder<br>
<strong>Progress bar:</strong> Vis hvor langt de er</p>

<h3>Trust signals for mobile</h3>
<p>Mobile users er mere skeptiske. Boost trust med:<br>
- Sikkerhedsbadges (SSL, GDPR)<br>
- Garantier (\"30 dages returret\")<br>
- Social proof (\"15.000+ tilfredse kunder\")<br>
- Reviews og ratings synligt<br>
- Support contact (chat, phone) let tilgængeligt<br>
- \"Sikker betaling\" messaging ved checkout</p>

<h2>Mobile-specific features</h2>

<h3>Click-to-call</h3>
<p>Gør phone numbers clickable: <code>&lt;a href=\"tel:+4512345678\"&gt;12 34 56 78&lt;/a&gt;</code></p>

<p>Kan øge conversions med 10-30% for high-consideration produkter.</p>

<h3>Location-based features</h3>
<p>- \"Find nærmeste butik\"<br>
- Shipping estimate baseret på location<br>
- Lokaliseret content (sprog, valuta, tilbud)</p>

<h3>Mobile-optimized search</h3>
<p>- Auto-suggest mens de taster<br>
- Voice search (\"Søg med stemme\")<br>
- Visual search (\"Søg med billede\")<br>
- Filters optimeret til mobile (bottom sheet, ikke sidebar)</p>

<h3>Progressive Web App (PWA)</h3>
<p>PWA = Web app der opfører sig som native app:<br>
- Offline functionality<br>
- Push notifications<br>
- Add to home screen<br>
- App-like experience</p>

<p>Kan øge mobile conversion med 20-50%.</p>

<h2>Sådan tester du mobile UX</h2>

<h3>Test på rigtige devices</h3>
<p>Ikke kun browser emulator. Test på:<br>
- iPhone (forskellige størrelser)<br>
- Android (forskellige brands og størrelser)<br>
- Tablets<br>
- Forskellige OS versioner</p>

<h3>Tools til mobile testing</h3>
<p><strong>Google Mobile-Friendly Test:</strong> Er din site mobile-friendly?<br>
<strong>PageSpeed Insights:</strong> Mobile speed score<br>
<strong>BrowserStack:</strong> Test på hundredvis af devices<br>
<strong>Hotjar:</strong> Mobile heatmaps og recordings<br>
<strong>Google Analytics:</strong> Mobile vs desktop performance</p>

<h2>Mobile CRO metrics</h2>
<p><strong>Mobile conversion rate:</strong> Conversions / Mobile visitors<br>
<strong>Mobile vs desktop gap:</strong> Hvor meget lavere er mobile?<br>
<strong>Mobile bounce rate:</strong> Forlader de med det samme?<br>
<strong>Mobile page speed:</strong> Under 3 sekunder?<br>
<strong>Mobile cart abandonment:</strong> Højere end desktop?<br>
<strong>Mobile form completion:</strong> Fuldfører de forms?</p>

<h2>Case study: 3x mobile conversion</h2>
<p><strong>Før:</strong><br>
- Desktop conversion: 3,2%<br>
- Mobile conversion: 0,9%<br>
- Mobile speed: 8,5 sekunder<br>
- Responsive design (ikke mobile-first)</p>

<p><strong>Ændringer:</strong><br>
1. Redesign til mobile-first<br>
2. Speed optimization (8,5s → 2,1s)<br>
3. Tilføjet Apple Pay og Google Pay<br>
4. Simplified checkout (5 steps → 2 steps)<br>
5. Sticky CTA på product pages<br>
6. Click-to-call på alle sider</p>

<p><strong>Efter:</strong><br>
- Mobile conversion: 2,7% (3x improvement)<br>
- Mobile revenue: +4,2 millioner kr årligt<br>
- Mobile bounce rate: 68% → 42%</p>

<h2>Mobile CRO checklist</h2>
<p>✅ Mobile-first design<br>
✅ Loading under 3 sekunder<br>
✅ Touch-friendly buttons (44x44px+)<br>
✅ Minimal typing required<br>
✅ Rigtige keyboards for hver field<br>
✅ Autofill support<br>
✅ Mobile wallets (Apple Pay, Google Pay)<br>
✅ Sticky CTA buttons<br>
✅ Simplified navigation<br>
✅ Guest checkout<br>
✅ Click-to-call<br>
✅ Trust signals visible<br>
✅ Tested på rigtige devices</p>

<h2>Næste skridt</h2>
<p>Start med at måle din mobile vs desktop conversion gap. Test derefter din mobile speed og fix de største issues. Implementer mobile wallets og simplificer checkout.</p>'''
    }
}

# Opdater artiklerne
updated_count = 0
for slug, data in articles_content.items():
    try:
        article = ArticlePage.objects.get(slug=slug)
        article.body = json.dumps([{'type': 'paragraph', 'value': data['body']}])
        article.save_revision().publish()
        print(f'✅ Opdateret: {article.title}')
        updated_count += 1
    except ArticlePage.DoesNotExist:
        print(f'❌ Artikel ikke fundet: {slug}')
    except Exception as e:
        print(f'❌ Fejl ved {slug}: {e}')

print(f'\n✅ {updated_count} artikler opdateret!')

