#!/usr/bin/env python3
"""
Batch 1: Opdater CRO artikler med professionelt indhold
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketingnyt.settings')
django.setup()

from news.models import ArticlePage

print('=== OPDATERER CRO ARTIKLER (BATCH 1) ===\n')

# CRO Artikler
articles = {
    'ab-testing-guide-2025': '''<h2>Hvorfor A/B testing er din vigtigste marketing skill</h2>
<p>A/B testing er ikke gætteri - det er videnskab. Virksomheder der tester systematisk ser 30-40% højere ROI end dem der ikke gør. Amazon, Google, og Netflix tester ALTING. Du skal også.</p>

<h2>Hvad er A/B testing egentlig?</h2>
<p>A/B testing (split testing) sammenligner to versioner af en side, email, eller annonce for at se hvilken performer bedst. Version A (control) vs Version B (variant). Traffic splittes 50/50, og du måler hvilken version når dit mål bedst.</p>

<h2>Hvad skal du teste? (Prioriteret liste)</h2>

<h3>Høj impact tests (start her)</h3>
<p><strong>1. Headlines:</strong> Den vigtigste faktor for engagement. Kan ændre conversion med 50-200%.<br>
<strong>2. CTA buttons:</strong> Tekst, farve, størrelse, placering. Små ændringer = store resultater.<br>
<strong>3. Hero images/video:</strong> Visuel kommunikation driver emotion og trust.<br>
<strong>4. Pricing display:</strong> Hvordan du præsenterer pris påvirker perceived value.<br>
<strong>5. Form length:</strong> Antal felter har direkte impact på completion rate.</p>

<h3>Medium impact tests</h3>
<p><strong>6. Social proof type:</strong> Testimonials vs case studies vs kunde-logos.<br>
<strong>7. Copy length:</strong> Lang vs kort beskrivelse (afhænger af produkt-kompleksitet).<br>
<strong>8. Layout:</strong> Placering af elementer, white space, visual hierarchy.</p>

<h2>Sådan designer du en valid test</h2>

<h3>Step 1: Formuler en klar hypotese</h3>
<p>Dårlig hypotese: "Jeg tror en grøn knap vil virke bedre"<br>
God hypotese: "Jeg tror at en grøn CTA-knap vil øge clicks med minimum 10% fordi grøn signalerer 'go' og skaber højere kontrast mod vores blå baggrund."</p>

<p><strong>Hypotese-template:</strong> "Jeg tror at [ændring] vil føre til [målbart resultat] fordi [rationale baseret på data eller psykologi]."</p>

<h3>Step 2: Definer success metrics</h3>
<p><strong>Primær metric:</strong> Den ene ting du optimerer for (conversion rate, click-through rate, revenue per visitor).<br>
<strong>Sekundære metrics:</strong> Andre vigtige metrics der ikke må forværres (bounce rate, time on site).</p>

<h3>Step 3: Beregn nødvendig sample size</h3>
<p>Brug en sample size calculator. Du skal bruge: Baseline conversion rate, minimum detectable effect, statistical significance level (typisk 95%), statistical power (typisk 80%).</p>

<p><strong>Tommelfingerregel:</strong> Minimum 100 conversions per variation. Hvis din conversion rate er 2%, skal du have minimum 5.000 visitors per variation = 10.000 total.</p>

<h3>Step 4: Kør testen længe nok</h3>
<p><strong>Minimum varighed:</strong> 1-2 uger for at fange forskellige dage og tidspunkter.<br>
<strong>Fuld business cycle:</strong> For B2B, kør minimum 1 måned.<br>
<strong>Stop ALDRIG testen tidligt:</strong> Selv hvis du ser resultater efter 2 dage. Det er sandsynligvis noise, ikke signal.</p>

<h2>Common A/B testing mistakes</h2>

<h3>Mistake #1: Teste for mange ting på én gang</h3>
<p>❌ Ændre headline, CTA, og billede samtidig<br>
✅ Test én ting ad gangen, så du ved hvad der virker</p>

<h3>Mistake #2: Stoppe testen for tidligt</h3>
<p>❌ "Vi har 90% confidence efter 3 dage, lad os stoppe!"<br>
✅ Vent til du har nået planned sample size OG minimum varighed</p>

<h3>Mistake #3: Ikke have nok traffic</h3>
<p>❌ Teste med 100 visitors total<br>
✅ Beregn sample size først, vent med at teste hvis du ikke har nok traffic</p>

<h3>Mistake #4: Ignorere statistisk signifikans</h3>
<p>❌ "Variant B har 5% højere conversion, lad os implementere!"<br>
✅ Tjek om forskellen er statistisk signifikant (p-value < 0.05)</p>

<h2>Tools til A/B testing</h2>
<p><strong>Enterprise:</strong> Optimizely, VWO, Adobe Target<br>
<strong>Mid-market:</strong> Google Optimize (gratis!), Convert, Unbounce<br>
<strong>Email:</strong> Mailchimp, HubSpot, ActiveCampaign (built-in)<br>
<strong>Ads:</strong> Facebook Ads Manager, Google Ads (built-in split testing)</p>

<h2>Sådan bygger du en testing kultur</h2>
<p>1. <strong>Test roadmap:</strong> Prioriter tests baseret på potential impact og effort<br>
2. <strong>Weekly reviews:</strong> Gennemgå running tests og resultater<br>
3. <strong>Learning library:</strong> Dokumenter alle tests og learnings<br>
4. <strong>Celebrate failures:</strong> Negative results er også learnings<br>
5. <strong>Compound wins:</strong> Små forbedringer (5-10%) compound til massive gains</p>

<h2>Næste skridt</h2>
<p>Start med at teste din vigtigste landing page's headline. Det er høj impact og relativt nemt. Brug denne guide til at designe en valid test, og byg momentum derfra.</p>''',

    'checkout-optimization-guide': '''<h2>Hvorfor checkout optimization er kritisk</h2>
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

<h2>Checkout optimization strategi</h2>

<h3>1. Reducer antal steps til minimum</h3>
<p><strong>Ideal:</strong> Single-page checkout eller maximum 3 steps<br>
<strong>Steps:</strong> Shipping → Payment → Review<br>
<strong>Vis progress:</strong> Progress bar så kunden ved hvor langt de er</p>

<h3>2. Tilbyd guest checkout</h3>
<p>24% abandoner fordi de skal oprette account. Løsning: Guest checkout som default, med option til at gemme info efter køb.</p>

<h3>3. Vær transparent om alle omkostninger tidligt</h3>
<p>48% abandoner pga. uventede omkostninger. Vis shipping costs og fees så tidligt som muligt. Brug shipping calculator på product page.</p>

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
<p><strong>Sikkerhed:</strong> SSL badge, "Sikker betaling" messaging<br>
<strong>Garantier:</strong> "30 dages returret", "Pengene tilbage garanti"<br>
<strong>Social proof:</strong> "15.000+ tilfredse kunder"<br>
<strong>Support:</strong> Chat eller phone number synligt<br>
<strong>Shipping info:</strong> "Levering 1-3 dage", "Gratis retur"</p>

<h2>Advanced checkout tactics</h2>

<h3>Exit-intent popups</h3>
<p>Når kunden er ved at forlade checkout, vis et sidste tilbud: "Vent! Her er 10% rabat hvis du fuldfører nu" eller "Gratis fragt hvis du fuldfører inden 10 minutter".</p>

<p>Kan redde 5-15% af abandonments.</p>

<h3>Cart abandonment emails</h3>
<p><strong>Email 1:</strong> 1 time efter abandonment - "Du glemte noget i din kurv"<br>
<strong>Email 2:</strong> 24 timer efter - "Stadig interesseret? Her er 10% rabat"<br>
<strong>Email 3:</strong> 3 dage efter - "Sidste chance - dit item er næsten udsolgt"</p>

<p>Recovery rate: 10-30% af abandoned carts.</p>

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
✅ Abandonment email sequence</p>

<h2>Case study: 34% reduktion i abandonment</h2>
<p><strong>Før:</strong> 5-step checkout, tvungen account creation, skjulte shipping costs. Abandonment rate: 78%</p>

<p><strong>Ændringer:</strong> Reduceret til 3 steps, tilføjet guest checkout, shipping calculator på product page, tilføjet MobilePay og Apple Pay, exit-intent popup med 10% rabat, 3-email abandonment sequence.</p>

<p><strong>Efter:</strong> Abandonment rate: 51% (34% reduktion). Revenue impact: +2,1 millioner kr årligt.</p>

<h2>Næste skridt</h2>
<p>Start med at måle din nuværende abandonment rate og identificer hvor i flowet folk dropper fra. Implementer derefter de 3 vigtigste fixes: Guest checkout, transparent pricing, og færre steps.</p>'''
}

# Opdater artiklerne
for slug, content in articles.items():
    try:
        article = ArticlePage.objects.get(slug=slug)
        article.body = [('rich_text', content)]
        revision = article.save_revision()
        revision.publish()
        print(f'✅ Opdateret og published: {article.title}')
    except ArticlePage.DoesNotExist:
        print(f'❌ Artikel ikke fundet: {slug}')
    except Exception as e:
        print(f'❌ Fejl ved {slug}: {e}')

print('\n✅ Batch 1 færdig!')

