#!/usr/bin/env python3
"""Translate /index.html → /en/index.html with full content translation.

Idempotent: re-running on already-translated /en/index.html re-applies all
replacements (no-op for already-translated text). The dictionary covers:
- HTML structural meta (lang, canonical, hreflang, og:*, twitter:*)
- All JSON-LD schema blocks (Organization, WebSite, full @graph)
- All visible Georgian text in body (hero, sections, FAQ, footer)
- Internal link rewrites (KA → /en/ where EN page exists; skipped → root)
- Calendly URL swap (30-seo-clone → quick-seo-consultation-15-minutes)
- Lang switcher (KA active → EN active)
- USD pricing (no GEL parenthetical per user decision 2026-05-10)

Run: python3 scripts/translate-index.py [--dry-run]
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KA_FILE = ROOT / 'index.html'
EN_FILE = ROOT / 'en' / 'index.html'

# Pages that have EN translations — internal links rewrite to /en/ counterparts.
TRANSLATED_PAGES = {
    'index.html', 'services.html', 'about-us.html', 'contact-us.html',
    'vacancies.html', 'lead-form.html', 'portfolio.html',
    'seo-strategy.html', 'seo-audit.html', 'seo-consultation.html',
    'seo-management.html', 'seo-copywriting.html', 'copywriting.html',
    'cro.html', 'google-ads.html', 'ai-seo.html', 'ra-aris-seo.html',
    'seo-course.html', 'roi-calculator.html', 'seo-tools.html',
    'case-studies.html', '404.html',
}
TRANSLATED_PREFIXES = ('case-studies/', 'tools/', 'industries/')

# Pages skipped from translation — internal links stay at root with hreflang="ka"
KA_ONLY_PAGES = {'blog.html', 'seo-leqsikoni.html', 'ai-leqsikoni.html', 'startup-leqsikoni.html'}
KA_ONLY_PREFIXES = ('blog/',)


def is_translated_target(href):
    """Check if a relative href points to a page with an EN counterpart."""
    if href.startswith(('http://', 'https://', '#', 'mailto:', 'tel:', '//', 'data:', 'javascript:')):
        return False
    if href in KA_ONLY_PAGES:
        return False
    if any(href.startswith(p) for p in KA_ONLY_PREFIXES):
        return False
    if href in TRANSLATED_PAGES:
        return True
    if any(href.startswith(p) for p in TRANSLATED_PREFIXES):
        return True
    return False


# ==============================================================
# REPLACEMENTS — applied in order. Each is (find_str, replace_str).
# Order matters: more specific patterns first to avoid double-replacement.
# ==============================================================

REPLACEMENTS = []


def add(old, new):
    """Register a replacement."""
    REPLACEMENTS.append((old, new))


# -------- 1. STRUCTURAL META --------

add('<html lang="ka" class="dark scroll-smooth"',
    '<html lang="en" class="dark scroll-smooth"')

add('<a href="#main-content" class="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-[9999] focus:bg-primary focus:text-white focus:px-4 focus:py-2 focus:rounded-lg">გადახტომა მთავარ შინაარსზე</a>',
    '<a href="#main-content" class="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-[9999] focus:bg-primary focus:text-white focus:px-4 focus:py-2 focus:rounded-lg">Skip to main content</a>')

add('<title>SEO სააგენტო - 10xSEO</title>',
    '<title>#1 SEO Agency in Georgia | Rank on Google &amp; ChatGPT — 10xSEO</title>')

add('<meta name="description" content="SEO სააგენტო -10xSEO საქართველოში საუკეთესო სეო სააგენტოა. ითანამშრომლე ჩვენთან - იყავი პირველი.">',
    '<meta name="description" content="Top SEO agency in Tbilisi, Georgia. 10xSEO delivers #1 rankings on Google, ChatGPT, Perplexity &amp; all AI search. Book a free 15-min consult today.">')

add('<meta property="og:locale" content="ka_GE">',
    '<meta property="og:locale" content="en_US">\n<meta property="og:locale:alternate" content="ka_GE">')

add('<meta property="og:title" content="SEO სააგენტო - 10xSEO">',
    '<meta property="og:title" content="#1 SEO Agency in Georgia | Rank on Google &amp; ChatGPT — 10xSEO">')

add('<meta property="og:description" content="SEO სააგენტო - 10xSEO საქართველოში საუკეთესო სეო სააგენტოა. ითანამშრომლე ჩვენთან - იყავი პირველი.">',
    '<meta property="og:description" content="Top SEO agency in Tbilisi, Georgia. 10xSEO delivers #1 rankings on Google, ChatGPT, Perplexity &amp; all AI search. Book a free 15-min consult today.">')

add('<meta property="og:url" content="https://10xseo.ge/">',
    '<meta property="og:url" content="https://10xseo.ge/en/">')

# Canonical + hreflang (insert hreflang block after canonical)
add('<link rel="canonical" href="https://10xseo.ge/">',
    '<link rel="canonical" href="https://10xseo.ge/en/">\n'
    '<link rel="alternate" hreflang="ka" href="https://10xseo.ge/">\n'
    '<link rel="alternate" hreflang="en" href="https://10xseo.ge/en/">\n'
    '<link rel="alternate" hreflang="x-default" href="https://10xseo.ge/">')

# -------- 2. CALENDLY URL SWAP --------
# Per user decision 2026-05-10: EN uses quick-seo-consultation-15-minutes
add("calendly.com/10xseo-sales/30-seo-clone", "calendly.com/10xseo-sales/quick-seo-consultation-15-minutes")

# -------- 3. ORGANIZATION JSON-LD (lines 222-258) --------
add('"description": "SEO სააგენტო — 10xSEO საქართველოში საუკეთესო სეო სააგენტოა. Google-ში, ChatGPT-ში და ყველა AI პლატფორმაზე პირველობის მოპოვება.",\n  "foundingDate": "2011",',
    '"description": "10xSEO is the leading SEO agency in Georgia. We help Tbilisi businesses rank #1 on Google, ChatGPT, and every AI search platform.",\n  "foundingDate": "2011",')

add('"streetAddress": "ბახტრიონის ქუჩა 8",\n    "addressLocality": "თბილისი",',
    '"streetAddress": "8 Bakhtrioni Street",\n    "addressLocality": "Tbilisi",')

# -------- 4. WEBSITE JSON-LD --------
add('"description": "#1 SEO სააგენტო საქართველოში",',
    '"description": "#1 SEO Agency in Georgia",')

# -------- 5. MAIN @graph JSON-LD (line 273 — full replacement) --------
# We replace the entire single-line JSON-LD with an English version.
KA_GRAPH_NEEDLE = '"@graph":[{"@type":"WebPage","@id":"https://10xseo.ge/#webpage","url":"https://10xseo.ge/","name":"SEO სააგენტო - 10xSEO","description":"SEO სააგენტო — 10xSEO საქართველოში საუკეთესო სეო სააგენტოა. Google-ში, ChatGPT-ში და ყველა AI პლატფორმაზე პირველობის მოპოვება.","inLanguage":"ka-GE"'

EN_GRAPH_NEEDLE = '"@graph":[{"@type":"WebPage","@id":"https://10xseo.ge/en/#webpage","url":"https://10xseo.ge/en/","name":"#1 SEO Agency in Georgia | Rank on Google & ChatGPT — 10xSEO","description":"Top SEO agency in Tbilisi, Georgia. 10xSEO delivers #1 rankings on Google, ChatGPT, Perplexity & all AI search. Book a free 15-min consult today.","inLanguage":"en-US"'

add(KA_GRAPH_NEEDLE, EN_GRAPH_NEEDLE)

# WebPage isPartOf URL stays root domain (parent site)
# But breadcrumb: replace "მთავარი" → "Home" + URL → /en/
add('{"@type":"BreadcrumbList","@id":"https://10xseo.ge/#breadcrumbs","itemListElement":[{"@type":"ListItem","position":1,"name":"მთავარი","item":"https://10xseo.ge/"}]}',
    '{"@type":"BreadcrumbList","@id":"https://10xseo.ge/en/#breadcrumbs","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://10xseo.ge/en/"}]}')

# Person — Davit Tsilosani
add('"@id":"https://10xseo.ge/about-us/#davit-tsilosani","name":"დავით წილოსანი","alternateName":"Davit Tsilosani","jobTitle":"SEO ექსპერტი, 10xSEO-ს დამფუძნებელი","description":"14 წლის SEO და ციფრული მარკეტინგის გამოცდილება. 100+ პროფესიონალური SEO აუდიტი, ორგანული ტრაფიკის ზრდა 15+ ინდუსტრიაში."',
    '"@id":"https://10xseo.ge/en/about-us/#davit-tsilosani","name":"Davit Tsilosani","alternateName":"დავით წილოსანი","jobTitle":"SEO Expert & Founder of 10xSEO","description":"14 years of SEO and digital marketing experience. 100+ professional SEO audits, organic traffic growth across 15+ industries."')

add('"knowsAbout":["SEO","ტექნიკური SEO","On-Page SEO","Link Building","Content Marketing","Keyword Research","AEO","GEO","Local SEO"]',
    '"knowsAbout":["SEO","Technical SEO","On-Page SEO","Link Building","Content Marketing","Keyword Research","AEO","GEO","Local SEO"]')

# ItemList — services
add('"@id":"https://10xseo.ge/#services","name":"10xSEO სერვისები","itemListElement":[{"@type":"ListItem","position":1,"item":{"@type":"Service","name":"SEO მომსახურება","url":"https://10xseo.ge/seo-management/","provider":{"@type":"Organization","name":"10XSEO"}}},{"@type":"ListItem","position":2,"item":{"@type":"Service","name":"SEO კონსულტაცია","url":"https://10xseo.ge/seo-consultation/","provider":{"@type":"Organization","name":"10XSEO"}}},{"@type":"ListItem","position":3,"item":{"@type":"Service","name":"SEO სტრატეგია","url":"https://10xseo.ge/seo-strategy/","provider":{"@type":"Organization","name":"10XSEO"}}},{"@type":"ListItem","position":4,"item":{"@type":"Service","name":"SEO კოპირაიტინგი","url":"https://10xseo.ge/seo-copywriting/","provider":{"@type":"Organization","name":"10XSEO"}}},{"@type":"ListItem","position":5,"item":{"@type":"Service","name":"UI/UX Copywriting","url":"https://10xseo.ge/copywriting/","provider":{"@type":"Organization","name":"10XSEO"}}},{"@type":"ListItem","position":6,"item":{"@type":"Service","name":"AI SEO","url":"https://10xseo.ge/ai-seo/","provider":{"@type":"Organization","name":"10XSEO"}}},{"@type":"ListItem","position":7,"item":{"@type":"Service","name":"CRO","url":"https://10xseo.ge/cro/","provider":{"@type":"Organization","name":"10XSEO"}}},{"@type":"ListItem","position":8,"item":{"@type":"Service","name":"Google Ads","url":"https://10xseo.ge/google-ads/","provider":{"@type":"Organization","name":"10XSEO"}}},{"@type":"ListItem","position":9,"item":{"@type":"Course","name":"SEO კურსი","url":"https://10xseo.ge/seo-course/","provider":{"@type":"Organization","name":"10XSEO"}}}]}',
    '"@id":"https://10xseo.ge/en/#services","name":"10xSEO Services","itemListElement":[{"@type":"ListItem","position":1,"item":{"@type":"Service","name":"SEO Management","url":"https://10xseo.ge/en/seo-management.html","provider":{"@type":"Organization","name":"10XSEO"}}},{"@type":"ListItem","position":2,"item":{"@type":"Service","name":"SEO Consultation","url":"https://10xseo.ge/en/seo-consultation.html","provider":{"@type":"Organization","name":"10XSEO"}}},{"@type":"ListItem","position":3,"item":{"@type":"Service","name":"SEO Strategy","url":"https://10xseo.ge/en/seo-strategy.html","provider":{"@type":"Organization","name":"10XSEO"}}},{"@type":"ListItem","position":4,"item":{"@type":"Service","name":"SEO Copywriting","url":"https://10xseo.ge/en/seo-copywriting.html","provider":{"@type":"Organization","name":"10XSEO"}}},{"@type":"ListItem","position":5,"item":{"@type":"Service","name":"UI/UX Copywriting","url":"https://10xseo.ge/en/copywriting.html","provider":{"@type":"Organization","name":"10XSEO"}}},{"@type":"ListItem","position":6,"item":{"@type":"Service","name":"AI SEO","url":"https://10xseo.ge/en/ai-seo.html","provider":{"@type":"Organization","name":"10XSEO"}}},{"@type":"ListItem","position":7,"item":{"@type":"Service","name":"CRO","url":"https://10xseo.ge/en/cro.html","provider":{"@type":"Organization","name":"10XSEO"}}},{"@type":"ListItem","position":8,"item":{"@type":"Service","name":"Google Ads","url":"https://10xseo.ge/en/google-ads.html","provider":{"@type":"Organization","name":"10XSEO"}}},{"@type":"ListItem","position":9,"item":{"@type":"Course","name":"SEO Course","url":"https://10xseo.ge/en/seo-course.html","provider":{"@type":"Organization","name":"10XSEO"}}}]}')

# FAQPage opening — just rewrite the @id to /en/
add('"@type":"FAQPage","@id":"https://10xseo.ge/#faq"',
    '"@type":"FAQPage","@id":"https://10xseo.ge/en/#faq"')

# FAQ Q1 (the FAQPage's first question)
add('{"@type":"Question","name":"რას აკეთებს SEO სააგენტო?","acceptedAnswer":{"@type":"Answer","text":"სეო სააგენტოს ამოცანა თქვენი ციფრული ხილვადობის მაქსიმალური გაზრდაა. ჩვენ ვიკვლევთ თქვენი მომხმარებლების ქცევას და საიტს ისე ვაწყობთ, რომ საძიებო სისტემებმა იგი საუკეთესო წყაროდ მიიჩნიონ. მუშაობას ვიწყებთ თქვენი ბიზნესის მიზნების შესწავლით და ვქმნით ინდივიდუალურ გეგმას, რომელიც გაზომვად შედეგებზეა ორიენტირებული."}}',
    '{"@type":"Question","name":"What does an SEO agency do?","acceptedAnswer":{"@type":"Answer","text":"An SEO agency\'s job is to maximize your digital visibility. We study your customers\' behavior and structure your website so search engines treat it as the best source. We start by understanding your business goals, then build a custom plan focused on measurable outcomes."}}')

add('{"@type":"Question","name":"რამდენი ხანი სჭირდება SEO შედეგების მიღებას?","acceptedAnswer":{"@type":"Answer","text":"SEO გრძელვადიანი ინვესტიციაა. პირველი ხელშესახები ცვლილებები, როგორც წესი, 3-დან 6 თვემდე პერიოდში ჩნდება, თუმცა ზუსტი ვადები დამოკიდებულია იმაზე, თუ რამდენად დიდია კონკურენცია თქვენს სფეროში და რა მდგომარეობაშია საიტი მუშაობის დაწყების მომენტში."}}',
    '{"@type":"Question","name":"How long does it take to see SEO results?","acceptedAnswer":{"@type":"Answer","text":"SEO is a long-term investment. The first noticeable changes typically appear within 3 to 6 months, though exact timing depends on competition in your industry and the starting condition of your website."}}')

add('{"@type":"Question","name":"რა ღირს SEO მომსახურება?","acceptedAnswer":{"@type":"Answer","text":"10xSEO-ში SEO მომსახურების ღირებულება 1880 ლარიდან იწყება. საბოლოო ფასი დამოკიდებულია სამუშაოს სპეციფიკასა და თქვენ მიერ დასახულ მიზნებზე. ჩვენ მაქსიმალურად ვერგებით პარტნიორი კომპანიის ინტერესებს, რათა თანამშრომლობა ორივე მხარისთვის მომგებიანი იყოს."}}',
    '{"@type":"Question","name":"How much does SEO cost?","acceptedAnswer":{"@type":"Answer","text":"At 10xSEO, SEO services start from $695/month. The final price depends on the scope of work and your specific goals. We adapt to each partner\'s needs to ensure the engagement is profitable for both sides."}}')

add('{"@type":"Question","name":"როგორ იზომება შედეგები?","acceptedAnswer":{"@type":"Answer","text":"წარმატებას სამი ძირითადი კრიტერიუმით ვზომავთ:</p><ul><li>თქვენი პოზიციები Google-ში</li><li>საიტზე შემოსული ადამიანების რაოდენობა</li><li>მათი ქცევა</li></ul><p>ჩვენი მიზანია, საიტზე მოვიზიდოთ არა უბრალოდ ბევრი, არამედ თქვენი პროდუქტით რეალურად დაინტერესებული ადამიანები."}}',
    '{"@type":"Question","name":"How do you measure results?","acceptedAnswer":{"@type":"Answer","text":"We measure success by three core criteria:</p><ul><li>Your Google rankings</li><li>The volume of visitors coming to your site</li><li>Their on-site behavior</li></ul><p>Our goal is not just to attract many people, but to bring in users genuinely interested in your product."}}')

add('{"@type":"Question","name":"რატომ უნდა ავირჩიოთ სააგენტო და არა In-House გუნდი?","acceptedAnswer":{"@type":"Answer","text":"პირველ რიგში, სირთულეს წააწყდებით კადრების აყვანის დროს. SEO კომპლექსური პროცესია სადაც პროექტზე გუნდი მუშაობს – SEO სპეციალისტი, სტრატეგოსი, კონტენტის მწერალი და ვებდეველოპერი."}}',
    '{"@type":"Question","name":"Why hire an agency instead of building an in-house team?","acceptedAnswer":{"@type":"Answer","text":"First, hiring is hard. SEO is a complex process that requires a full team — an SEO specialist, strategist, content writer, and web developer all working together. An agency gives you all of that on day one."}}')

add('{"@type":"Question","name":"რატომ არის 10xSEO საქართველოში საუკეთესო SEO სააგენტო?","acceptedAnswer":{"@type":"Answer","text":"ჩვენ არ გთავაზობთ მხოლოდ SEO სერვისს – ჩვენ ვმუშაობთ თქვენი ბიზნესის რეალური მიზნებისა და შედეგებისთვის. გვაქვს სრულფასოვანი \\"Done-for-You\\" პაკეტი, რომელიც AI-ით მხარდაჭერილ AEO/GEO ოპტიმიზაციას, დეტალურად გაზომვად შედეგებსა და მაღალკვალიფიციურ პროექტ მენეჯმენტს მოიცავს. ჩვენი გუნდი შედგება 12+ წლიანი გამოცდილების მქონე სპეციალისტებისგან. დაბოლოს, თუ თავად გადაწყვეტთ სეო სააგენტოების შედარებას, მარტივად დარწმუნდებით, რომ ჩვენი სერვისი უნიკალურია."}}',
    '{"@type":"Question","name":"Why is 10xSEO the best SEO agency in Georgia?","acceptedAnswer":{"@type":"Answer","text":"We don\'t just sell SEO services — we work toward your real business goals and outcomes. Our \\"Done-for-You\\" package combines AI-powered AEO/GEO optimization, granular measurement, and senior project management. Our team has 12+ years of experience. Compare us against any SEO agency in Tbilisi or Georgia and you\'ll see our service is unique."}}')

add('{"@type":"Question","name":"რა სახის ანგარიშებს მივიღებ და რა სიხშირით?","acceptedAnswer":{"@type":"Answer","text":"თქვენ გექნებათ მუდმივი წვდომა მონაცემთა პანელზე, სადაც შედეგებს რეალურ დროში ნახავთ. ამასთან, ყოველ ორ კვირაში მოგაწვდით ინფორმაციას პოზიციების განახლების შესახებ, ხოლო თვის ბოლოს მიიღებთ შემაჯამებელ, დეტალურ ვიდეომიმოხილვას. ნებისმიერ კითხვაზე პასუხს კი სამუშაო საათებში მაქსიმუმ 10 წუთში დაგიბრუნებთ."}}',
    '{"@type":"Question","name":"What kind of reports will I receive and how often?","acceptedAnswer":{"@type":"Answer","text":"You\'ll have constant access to a live data dashboard where you can see results in real time. Every two weeks we send a ranking update, and at month-end you get a comprehensive video review. We respond to any question within 10 minutes during business hours."}}')

add('{"@type":"Question","name":"როგორ ზომავთ SEO-ს ROI-ს?","acceptedAnswer":{"@type":"Answer","text":"როცა საკმარისი მონაცემები გვაქვს, ROI-ს ვზომავთ რეალური გაყიდვებით — რამდენი შემოსავალი შემოვიდა ორგანული არხიდან. თუ მონაცემები ჯერ საკმარისი არ არის, საზომად ვიყენებთ საკვანძო სიტყვების საშუალო პოზიციის ზრდას ან ორგანული ტრაფიკის მატებას."}}',
    '{"@type":"Question","name":"How do you measure SEO ROI?","acceptedAnswer":{"@type":"Answer","text":"When we have enough data, we measure ROI by actual sales — how much revenue came through the organic channel. If data is still limited, we benchmark by average keyword position improvement or organic traffic growth."}}')

add('{"@type":"Question","name":"რა გჭირდებათ ჩემგან, რომ დავიწყოთ?","acceptedAnswer":{"@type":"Answer","text":"მინიმალური ჩართულობა. თქვენგან გვჭირდება მხოლოდ ბიზნესის სპეციფიკის ცოდნა, კონტენტის თემების დამტკიცება და ტექნიკური წვდომა (Google Analytics, Search Console, საიტის ადმინი). დანარჩენს — სტრატეგიას, კონტენტს, ოპტიმიზაციას, რეპორტინგს — ჩვენ ვაკეთებთ."}}',
    '{"@type":"Question","name":"What do you need from me to get started?","acceptedAnswer":{"@type":"Answer","text":"Minimal involvement. We need only your domain knowledge, content topic approval, and technical access (Google Analytics, Search Console, site admin). Everything else — strategy, content, optimization, reporting — we handle."}}')

add('{"@type":"Question","name":"ვინ არის ის კლიენტი, ვისაც არ აიყვანდით — და რატომ?","acceptedAnswer":{"@type":"Answer","text":"ხშირად უარს ვამბობთ კლიენტებზე, რომლებსაც: (1) ბიზნეს-მოდელი ჯერ არ აქვთ გამართული, მაგრამ უცხო ბაზრებზე გასვლა უნდათ; (2) საიტის კოდზე წვდომას არ გვაძლევენ და მაინც ტექნიკურ SEO-ს ითხოვენ; (3) უკვე უარყოფითი ბრენდის რეპუტაცია აქვთ, რომელიც PR-ს მოითხოვს, არა SEO-ს. პირველი 30-წუთიანი ზარი ყოველთვის ორმხრივი შესაბამისობის შემოწმებაა — თქვენ გვაფასებთ ჩვენ, ჩვენ კი — თქვენ."}}',
    '{"@type":"Question","name":"Which clients do you turn away — and why?","acceptedAnswer":{"@type":"Answer","text":"We often decline clients who: (1) don\'t have their business model figured out yet but want to expand internationally; (2) refuse code access yet expect technical SEO; (3) already have negative brand reputation that requires PR, not SEO. The first 15-minute call is always a mutual fit check — you evaluate us, we evaluate you."}}')

add('{"@type":"Question","name":"როცა კონტრაქტი დასრულდება — რა მოხდება ჩემი რანკინგებით?","acceptedAnswer":{"@type":"Answer","text":"რანკინგი რჩება, თუ ბექლინკები რეალურია და კონტენტი სრულფასოვანი — ჩვენი 100% white-hat მიდგომით სწორედ ასე გექნებათ. მონიტორინგისა და ახალი კონტენტის გარეშე კონკურენტებმა თანდათან შეიძლება გადაგასწრონ, მაგრამ ეს ნელი პროცესია — არა მკვეთრი ვარდნა, რომელიც PBN-ის ან ყალბი ბექლინკების გათიშვისას ხდება ხოლმე."}}',
    '{"@type":"Question","name":"What happens to my rankings when our contract ends?","acceptedAnswer":{"@type":"Answer","text":"Rankings stay if the backlinks are real and the content is solid — that\'s exactly what our 100% white-hat approach delivers. Without monitoring and fresh content, competitors may slowly catch up, but it\'s a gradual decline — not the cliff drop that happens when a PBN or fake backlinks get cut off."}}')

add('{"@type":"Question","name":"შესაძლებელია თუ არა თქვენთან გადმოსვლა, თუ უკვე ვმუშაობ სხვა SEO სააგენტოსთან?","acceptedAnswer":{"@type":"Answer","text":"დიახ, პროცესში ჩართვა ნებისმიერ ეტაპზე შეგვიძლია. პირველ ორ კვირაში ჩავატარებთ წინა სამუშაო პროცესის სრულ აუდიტს და მოვაწესრიგებთ ყველა ტექნიკურ საკითხს. ამის შემდეგ კი გამოვასწორებთ იმ შეცდომებს, რომლებიც აქამდე შედეგის მიღებაში გიშლიდათ ხელს."}}',
    '{"@type":"Question","name":"Can I switch to you if I\'m already working with another SEO agency?","acceptedAnswer":{"@type":"Answer","text":"Yes, we can pick up at any stage. The first two weeks we run a complete audit of the prior workflow and clean up all technical issues. After that, we fix the mistakes that have been blocking your results."}}')

add('{"@type":"Question","name":"წინა სააგენტო Black-hat ლინკებს ყიდდა — დაწყებამდე შეგიძლიათ შეაფასოთ, მემუქრება თუ არა Google-ის ჯარიმა?","acceptedAnswer":{"@type":"Answer","text":"კი. პირველი 7 დღე — ბექლინკების ტოქსიკურობის აუდიტი (Ahrefs + SEMrush + ხელით შემოწმება). თუ რისკი გამოვლინდება, disavow ფაილს ვამზადებთ Google-სთვის. ეს ჩვენი თანამშრომლობამდე ჩატარებული დიაგნოსტიკის ნაწილია — დამატებითი ფასის გარეშე. ამის მიზანი — Google-ის შესაძლო ჯარიმისგან თქვენი რეპუტაციის დაცვაა."}}',
    '{"@type":"Question","name":"My previous agency bought black-hat links — can you assess my Google penalty risk before we start?","acceptedAnswer":{"@type":"Answer","text":"Yes. The first 7 days are a backlink toxicity audit (Ahrefs + SEMrush + manual review). If risk is detected, we prepare a disavow file for Google. This pre-engagement diagnostic is included free — its purpose is to protect your reputation from a potential Google penalty."}}')

add('{"@type":"Question","name":"ვაკეთებ საიტის რემონტს ან მიგრაციას — რანკინგის შენარჩუნებაზე ვინ არის პასუხისმგებელი, დეველოპერი თუ თქვენ?","acceptedAnswer":{"@type":"Answer","text":"ჩვენ. დეველოპერთან ერთად მუშაობს ჩვენი ტექნიკური SEO სპეციალისტი — მიგრაციამდე აუდიტი, URL mapping და 301 redirect-ების ფაილი, სატესტო გარემოს შემოწმება გაშვებამდე, გაშვების შემდგომი მონიტორინგი 30 დღის განმავლობაში. ჩვენი შესრულებული მიგრაციების საშუალო ტრაფიკის კლება <5%-ია (ინდუსტრიის საშუალო 30-50%)."}}',
    '{"@type":"Question","name":"I\'m doing a site rebuild or migration — who owns ranking preservation, the developer or you?","acceptedAnswer":{"@type":"Answer","text":"We do. Our technical SEO specialist works alongside your developer — pre-migration audit, URL mapping and a 301 redirect file, staging environment QA before launch, post-launch monitoring for 30 days. Our average migration traffic loss is <5% (industry average: 30-50%)."}}')


# -------- 6. AUTO-SWAP data-ka/data-en INNER TEXT --------
# For elements with data-ka="X" data-en="Y" attributes whose inner text
# matches the data-ka value, swap inner text to the data-en value.
# Handles both single-line and multi-line element bodies.

def swap_data_en_inner_text(html):
    """Swap inner text with data-en value where it matches data-ka value.
    Patterns handled:
      <tag attrs data-ka="X" data-en="Y" attrs>X</tag>
      <tag attrs data-ka="X" data-en="Y" attrs>\\n  X\\n  </tag>
    Returns (html, count_of_swaps).
    """
    pattern = re.compile(
        r'(data-ka="([^"]+)"\s+data-en="([^"]+)"[^>]*>)(\s*)([^<]*?)(\s*)(</[a-zA-Z]+>)',
        re.DOTALL
    )

    swaps = [0]  # closure box

    def replacer(m):
        opening = m.group(1)
        ka_text = m.group(2)
        en_text = m.group(3)
        leading_ws = m.group(4)
        inner = m.group(5)
        trailing_ws = m.group(6)
        closing = m.group(7)

        # Decode common HTML entities for comparison
        ka_decoded = ka_text.replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
        inner_decoded = inner.replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")

        if inner_decoded.strip() == ka_decoded.strip():
            swaps[0] += 1
            return f'{opening}{leading_ws}{en_text}{trailing_ws}{closing}'
        return m.group(0)

    new_html = pattern.sub(replacer, html)
    return new_html, swaps[0]


# -------- 7. EXPLICIT BODY TRANSLATIONS (visible text not covered by data-en) --------

BODY_TRANSLATIONS = {
    # ARIA labels
    'aria-label="მთავარი ნავიგაცია"': 'aria-label="Main navigation"',
    'aria-label="მობილური ნავიგაცია"': 'aria-label="Mobile navigation"',
    'aria-label="მენიუს გახსნა"': 'aria-label="Open menu"',
    'aria-label="ხმის ჩართვა/გამორთვა"': 'aria-label="Toggle sound"',
    'aria-label="წინა პლატფორმა"': 'aria-label="Previous platform"',
    'aria-label="შემდეგი პლატფორმა"': 'aria-label="Next platform"',
    'aria-label="წინა review"': 'aria-label="Previous review"',
    'aria-label="შემდეგი review"': 'aria-label="Next review"',
    'aria-label="დარეკე: +995 510 10 15 17"': 'aria-label="Call: +995 510 10 15 17"',
    'aria-label="ვიდეო პასუხი — ყოველკვირეული რეპორტები"': 'aria-label="Video response — Weekly reports"',
    'aria-label="ვიდეო პასუხი — სრული გამჭვირვალობა"': 'aria-label="Video response — Full transparency"',
    'aria-label="ვიდეო პასუხი — AI-ით გაძლიერებული SEO"': 'aria-label="Video response — AI-powered SEO"',
    'aria-label="ვიდეო პასუხი — ROI-ზე ფოკუსი"': 'aria-label="Video response — ROI focus"',
    'aria-label="ვიდეო პასუხი — სწრაფი რეაგირება"': 'aria-label="Video response — Fast response"',
    'aria-label="ვიდეო პასუხი — მონაცემებზე დაფუძნებული"': 'aria-label="Video response — Data-driven"',

    # Header nav direct content (without data-en) — industries inner text
    '>სამშენებლო &amp; უძრავი ქონება<': '>Construction &amp; Real Estate<',
    '>კლინიკები &amp; ჯანდაცვა<': '>Healthcare &amp; Clinics<',
    '>ფინანსური სერვისები<': '>Financial Services<',
    '<p class="menu-link text-xs font-semibold text-body-dark/40 uppercase tracking-wider mt-2 mb-1 pl-4" style="transition-delay:0.25s">კოპირაიტინგი</p>':
        '<p class="menu-link text-xs font-semibold text-body-dark/40 uppercase tracking-wider mt-2 mb-1 pl-4" style="transition-delay:0.25s">Copywriting</p>',
    '<p class="menu-link text-xs font-semibold text-body-dark/80 uppercase tracking-wider mt-2 mb-1" style="transition-delay:0.43s">ინდუსტრიები</p>':
        '<p class="menu-link text-xs font-semibold text-body-dark/80 uppercase tracking-wider mt-2 mb-1" style="transition-delay:0.43s">Industries</p>',

    # Hero section
    '<img src="images/pyramid-top.webp" alt="SEO პოზიციები"': '<img src="images/pyramid-top.webp" alt="SEO rankings — be #1"',
    'იყავი<br>პირველი': 'Be<br>#1',

    # H1 (V3 user pick: "AI-Powered" instead of "The AI Era's")
    "The AI Era's": "AI-Powered",

    # Hero subheading (with international angle per user request)
    "Georgia's #1 SEO Agency — We put brands where customers search for answers.":
        "Georgia's SEO agency for Tbilisi and international brands. We rank you #1 on Google, ChatGPT & every AI search platform.",

    # Image alts (clients)
    'alt="ფარმადეპო"': 'alt="Pharmadepo"',
    'alt="თოდუას კლინიკა"': 'alt="Todua Clinic"',
    'alt="კოორდინატი"': 'alt="Koordinati"',
    'alt="ქრონომეტრი"': 'alt="Chronometer"',

    # Ticker brand names
    '<span class="text-white/80 text-sm font-medium tracking-wide">ფარმადეპო</span>':
        '<span class="text-white/80 text-sm font-medium tracking-wide">Pharmadepo</span>',

    # Services preview section (id="services") — visible text
    '>აირჩიეთ სასურველი მიმართულება<': '>Choose your direction<',
    '>მენეჯმენტი<': '>Management<',
    '>ხილვადობა ChatGPT-ში, Gemini-სა და AI ძიებაში<': '>Visibility in ChatGPT, Gemini, and AI search<',
    '>კონვერსიის ოპტიმიზაცია<': '>Conversion Optimization<',
    '>ვარიანტების შედარება, UX, კლიენტების მოზიდვა<': '>A/B testing, UX, lead acquisition<',
    '>SEO კონსულტაცია<': '>SEO Consultation<',
    '>1-საათიანი სტრატეგიული სესია ექსპერტთან<': '>1-hour strategy session with an expert<',

    # Results section
    'ჩვენი კლიენტების წარმატების მაჩვენებლები': "Our clients' success metrics",
    'ყველა მეტრიკა რეალურია — Google Analytics და Search Console-ის მონაცემები.':
        'Every metric is real — sourced from Google Analytics and Search Console.',
    'ტრაფიკის გაორმაგება': 'Traffic doubled',
    'ზრდა 28 დღეში': 'Growth in 28 days',
    'ტრაფიკის ზრდა': 'Traffic growth',
    'სამშენებლო | 3 თვე': 'Construction | 3 months',
    'სამშენებლო | 28 დღე': 'Construction | 28 days',
    '<div><span class="text-body-dark/80">გვერდები</span></div>': '<div><span class="text-body-dark/80">Pages</span></div>',
    '<div><span class="text-body-dark/80">გაყიდვა</span></div>': '<div><span class="text-body-dark/80">Sales</span></div>',
    'ლოკალური SEO': 'Local SEO',
    'ქართული ბრენდი | GMB': 'Georgian brand | GMB',
    '<p class="text-[11px] text-body-dark">ბმულზე გადასვლა</p>': '<p class="text-[11px] text-body-dark">Click-through</p>',
    '<p class="text-[11px] text-body-dark">ხილვადობა</p>': '<p class="text-[11px] text-body-dark">Visibility</p>',
    'ვიზიტორი 4 თვეში': 'Visitors in 4 months',
    'მედიცინა | 0-დან': 'Healthcare | from zero',
    'სტომატოლოგია': 'Dentistry',
    'მედიცინა | იმპლანტაცია': 'Healthcare | implants',
    '<span class="text-body-dark/80">ვიზიტორი</span>': '<span class="text-body-dark/80">Visitors</span>',
    '<span class="text-body-dark/80">ხილვადობა</span>': '<span class="text-body-dark/80">Visibility</span>',
    'სრული პორტფოლიო': 'Full portfolio',
    '35+ პარტნიორი • საშუალო ზრდა +430%': '35+ partners • Average growth +430%',

    # Process section
    'პროცესი': 'Process',
    'როგორ ვმუშაობთ': 'How we work',
    'აუდიტი & სტრატეგია': 'Audit & Strategy',
    'საქმეს ვიწყებთ სიღრმისეული ტექნიკური ანალიზითა და კონკურენტების შესწავლით. ვქმნით პერსონალიზებულ სტრატეგიას, რომელიც ზუსტად პასუხობს თქვენს მიზნებს':
        'We start with deep technical analysis and competitor research. We build a personalized strategy that answers your goals exactly.',
    'იმპლემენტაცია': 'Implementation',
    'On-page ოპტიმიზაცია, მაღალი ავტორიტეტის მქონე კონტენტის შექმნა და იმ ტექნიკური პარამეტრების სინქრონიზაცია, რაც თქვენს საიტს AI-სა და საძიებო სისტემებისთვის პრიორიტეტულ წყაროდ აქცევს':
        'On-page optimization, authoritative content creation, and the technical sync that makes your site a priority source for AI and search engines.',
    'ყოველკვირეული ანგარიში და შედეგების მიმოხილვა': 'Weekly Report & Results Review',
    'ყოველ კვირას მიიღებთ დეტალურ ინფორმაციას იმის შესახებ, თუ რა გაკეთდა, რა შედეგები გვაქვს მოცემულ მომენტში და როგორია ჩვენი სამოქმედო გეგმა მომდევნო დღეებისთვის':
        'Every week you receive detailed information on what was done, where results stand, and the action plan for the days ahead.',
    'ჩვენი გამორჩეულობა': 'What sets us apart',
    'შედეგი და განვითარება': 'Results & Growth',
    'ჩვენი მთავარი მიზანი ვიზიტორების რაოდენობის, საძიებო პოზიციებისა და რეალური გაყიდვების სტაბილური, თვიდან თვემდე მზარდი დინამიკაა':
        'Our core goal: stable, month-over-month growth in visitors, search positions, and real sales.',

    # Why us section
    '<p class="text-sm font-semibold text-primary dark:text-primary-light uppercase tracking-wider mb-3">რატომ ჩვენ</p>':
        '<p class="text-sm font-semibold text-primary dark:text-primary-light uppercase tracking-wider mb-3">Why us</p>',
    'რატომ <span class="gradient-text">10XSEO</span>?': 'Why <span class="gradient-text">10XSEO</span>?',
    'რა გამოგვარჩევს — 6 მიზეზი, თუ რატომ ირჩევენ ბიზნესები პირველობისკენ მიმავალ გუნდს':
        '6 reasons why businesses choose the team that takes them to #1.',
    '<h3 class="font-heading text-lg font-bold text-heading dark:text-heading-dark mb-3 mt-8">ყოველკვირეული რეპორტები</h3>':
        '<h3 class="font-heading text-lg font-bold text-heading dark:text-heading-dark mb-3 mt-8">Weekly Reports</h3>',
    'ყოველ კვირა მიიღებთ დეტალურ ანგარიშს — რა გაკეთდა, რა შეიცვალა და რა არის შემდეგი ნაბიჯი.':
        'Every week, you get a detailed report — what was done, what changed, and what comes next.',
    '<h3 class="font-heading text-lg font-bold text-heading dark:text-heading-dark mb-3 mt-8">სრული გამჭვირვალობა</h3>':
        '<h3 class="font-heading text-lg font-bold text-heading dark:text-heading-dark mb-3 mt-8">Full Transparency</h3>',
    'Google Search Console, Analytics — ყველაფერს ხედავთ რეალურ დროში.':
        'Google Search Console, Analytics — you see everything in real time.',
    '<h3 class="font-heading text-lg font-bold text-heading dark:text-heading-dark mb-3 mt-8">AI-ით გაძლიერებული SEO</h3>':
        '<h3 class="font-heading text-lg font-bold text-heading dark:text-heading-dark mb-3 mt-8">AI-Powered SEO</h3>',
    'ChatGPT, Gemini ოპტიმიზაცია ჩვენს სტრატეგიაში — GEO და AEO ინტეგრირებული.':
        'ChatGPT and Gemini optimization built into our strategy — GEO and AEO integrated.',
    '<h3 class="font-heading text-lg font-bold text-heading dark:text-heading-dark mb-3 mt-8">ROI-ზე ფოკუსი</h3>':
        '<h3 class="font-heading text-lg font-bold text-heading dark:text-heading-dark mb-3 mt-8">ROI Focus</h3>',
    'ტრაფიკი კი არა, შემოსავალი. სტრატეგია რეალურ ზრდაზეა ორიენტირებული.':
        'Not just traffic — revenue. The strategy is built around real growth.',
    '<h3 class="font-heading text-lg font-bold text-heading dark:text-heading-dark mb-3 mt-8">სწრაფი რეაგირება</h3>':
        '<h3 class="font-heading text-lg font-bold text-heading dark:text-heading-dark mb-3 mt-8">Fast Response</h3>',
    '10 წუთი საშუალო response time სამუშაო საათებში.': '10-minute average response time during business hours.',
    '<h3 class="font-heading text-lg font-bold text-heading dark:text-heading-dark mb-3 mt-8">მონაცემებზე დაფუძნებული</h3>':
        '<h3 class="font-heading text-lg font-bold text-heading dark:text-heading-dark mb-3 mt-8">Data-Driven</h3>',
    'A/B ტესტინგი, Heatmaps, Keyword Research — ყველა გადაწყვეტილება ემყარება მონაცემებს, არა ვარაუდებს.':
        'A/B testing, heatmaps, keyword research — every decision is based on data, not assumptions.',

    # Team section
    '<p class="text-sm font-semibold text-primary dark:text-primary-light uppercase tracking-wider mb-3">გუნდი</p>':
        '<p class="text-sm font-semibold text-primary dark:text-primary-light uppercase tracking-wider mb-3">Team</p>',
    'გუნდი, რომელიც <span class="gradient-text">მასშტაბურ შედეგებს</span> აღწევს':
        'The team that delivers <span class="gradient-text">scalable results</span>',
    '7+ წლის გამოცდილება, 50+ კლიენტი — პროფესიონალთა გუნდი, რომელიც თქვენი ბიზნესის ზრდაზე ზრუნავს':
        '7+ years of experience, 50+ clients — a team of professionals invested in your business growth.',
    'დავით წილოსანი': 'Davit Tsilosani',
    '<p class="text-primary font-semibold mb-4">დამფუძნებელი და ხელმძღვანელი</p>':
        '<p class="text-primary font-semibold mb-4">Founder & CEO</p>',
    '7+ წელი ციფრულ ინდუსტრიაში და 50-ზე მეტი წარმატებული პროექტი. Google-ის მიერ აღიარებული სპეციალისტი, რომელმაც საქართველოში SEO-ს განვითარებას ერთ-ერთმა პირველმა ჩაუყარა საფუძველი':
        '7+ years in the digital industry and 50+ successful projects. A Google-recognized specialist who was among the first to lay the foundation of SEO in Georgia.',
    '<h4 class="font-semibold text-heading dark:text-heading-dark text-sm">SEO სპეციალისტი</h4>':
        '<h4 class="font-semibold text-heading dark:text-heading-dark text-sm">SEO Specialist</h4>',
    '<h4 class="font-semibold text-heading dark:text-heading-dark text-sm">ქოფირაითერი</h4>':
        '<h4 class="font-semibold text-heading dark:text-heading-dark text-sm">Copywriter</h4>',
    '<h4 class="font-semibold text-heading dark:text-heading-dark text-sm">ვებდეველოპერი</h4>':
        '<h4 class="font-semibold text-heading dark:text-heading-dark text-sm">Web Developer</h4>',
    '<h4 class="font-semibold text-heading dark:text-heading-dark text-sm">ანალიტიკოსი</h4>':
        '<h4 class="font-semibold text-heading dark:text-heading-dark text-sm">Analyst</h4>',
    'შემოუერთდით 10x-ის გუნდს': 'Join the 10x team',

    # Testimonials section
    '<p class="text-sm font-semibold text-primary dark:text-primary-light uppercase tracking-wider mb-3">ტესტიმონიალები</p>':
        '<p class="text-sm font-semibold text-primary dark:text-primary-light uppercase tracking-wider mb-3">Testimonials</p>',
    'რას ამბობენ ჩვენი კლიენტები': 'What our clients say',
    '>ყველა review Clutch.co-ზე<': '>All reviews on Clutch.co<',

    # YouTube video section
    'playlabel="Local SEO: როგორ გახდეთ #1 Google Maps-ზე"': 'playlabel="Local SEO: How to become #1 on Google Maps"',
    '15:10 | Local SEO: როგორ გახდეთ #1 Google Maps-ზე | სრული გზამკვლევი 2026':
        '15:10 | Local SEO: How to become #1 on Google Maps | Complete Guide 2026',
    '<p class="text-sm font-semibold uppercase tracking-wider text-red-500 mb-3">YouTube არხი</p>':
        '<p class="text-sm font-semibold uppercase tracking-wider text-red-500 mb-3">YouTube Channel</p>',
    'SEO & AI <span class="bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">ვიდეო გაკვეთილები</span>':
        'SEO & AI <span class="bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">Video Lessons</span>',
    'ისწავლეთ SEO, AI მარკეტინგი და ბიზნეს სტრატეგიები ჩვენი უფასო ვიდეო კონტენტით. ახალი ვიდეო ყოველ კვირას.':
        'Learn SEO, AI marketing, and business strategy from our free video content. New video every week.',
    '<p class="text-xs text-body dark:text-body-dark">ვიდეო</p>': '<p class="text-xs text-body dark:text-body-dark">Videos</p>',
    '<p class="text-xs text-body dark:text-body-dark">გამომწერი</p>': '<p class="text-xs text-body dark:text-body-dark">Subscribers</p>',
    '<p class="text-xs text-body dark:text-body-dark">წლიდან</p>': '<p class="text-xs text-body dark:text-body-dark">Since</p>',
    'გამოიწერეთ არხი': 'Subscribe to the channel',
    '>ყველა ვიდეოს ნახვა &rarr;<': '>View all videos &rarr;<',

    # CTA banner before FAQ
    'მზად ხარ იყო <span class="bg-gradient-to-r from-yellow-200 to-amber-400 bg-clip-text text-transparent drop-shadow-sm">პირველი</span>?':
        'Ready to be <span class="bg-gradient-to-r from-yellow-200 to-amber-400 bg-clip-text text-transparent drop-shadow-sm">#1</span>?',
    'დაჯავშნეთ უფასო კონსულტაცია და გაიგეთ როგორ შეიძლება ორგანული ტრაფიკის გაზრდა.':
        'Book a free consultation and learn how to grow your organic traffic.',
    # "დაჯავშნეთ კონსულტაცია" appears in many places — handled by data-en swap

    # FAQ section visible
    '>ხშირად დასმული კითხვები<': '>Frequently Asked Questions<',
    '<span id="v29-more-txt">დანარჩენი 1 კითხვის ნახვა</span>':
        '<span id="v29-more-txt">View 1 more question</span>',
    '<span id="v29-more-txt">დანარჩენი 8 კითხვის ნახვა</span>':
        '<span id="v29-more-txt">View 8 more questions</span>',
    "moreTxt.textContent = expanded ? 'ნაკლების ჩვენება' : ('დანარჩენი ' + remainder + ' კითხვის ნახვა');":
        "moreTxt.textContent = expanded ? 'Show less' : ('View ' + remainder + ' more questions');",

    # FAQ tabs (also appear in JS object literals)
    '{name:"ყველა", key:"all"}, {name:"ზოგადი", key:"general"}, {name:"ფასი", key:"price"}, {name:"შედეგები", key:"results"}':
        '{name:"All", key:"all"}, {name:"General", key:"general"}, {name:"Pricing", key:"price"}, {name:"Results", key:"results"}',
    "var tabs=document.getElementById('v29-tabs'), list=document.getElementById('v29-items'), activeCat='ყველა';":
        "var tabs=document.getElementById('v29-tabs'), list=document.getElementById('v29-items'), activeCat='All';",
    "t.className='v29-tab'+(cat==='ყველა'?' v29-active':'');":
        "t.className='v29-tab'+(cat==='All'?' v29-active':'');",
    'var catKeyMap={"ზოგადი":"general","ფასი":"price","შედეგები":"results"};':
        'var catKeyMap={"General":"general","Pricing":"price","Results":"results"};',
    "var match = activeCat==='ყველა' || el.getAttribute('data-cat')===activeCat;":
        "var match = activeCat==='All' || el.getAttribute('data-cat')===activeCat;",

    # Body FAQ items (visible — separate from schema)
    'cat: "ზოგადი"': 'cat: "General"',
    'cat: "შედეგები"': 'cat: "Results"',
    'cat: "ფასი"': 'cat: "Pricing"',

    # Body FAQ Q&A (these match the schema, but the visible body has them too)
    'q: "რას აკეთებს SEO სააგენტო?"': 'q: "What does an SEO agency do?"',
    'a: "სეო სააგენტოს ამოცანა თქვენი ციფრული ხილვადობის მაქსიმალური გაზრდაა. ჩვენ ვიკვლევთ თქვენი მომხმარებლების ქცევას და საიტს ისე ვაწყობთ, რომ საძიებო სისტემებმა იგი საუკეთესო წყაროდ მიიჩნიონ. მუშაობას ვიწყებთ თქვენი ბიზნესის მიზნების შესწავლით და ვქმნით ინდივიდუალურ გეგმას, რომელიც გაზომვად შედეგებზეა ორიენტირებული."':
        'a: "An SEO agency\'s job is to maximize your digital visibility. We study your customers\' behavior and structure your website so search engines treat it as the best source. We start by understanding your business goals, then build a custom plan focused on measurable outcomes."',
    'q: "რამდენი ხანი სჭირდება SEO შედეგების მიღებას?"': 'q: "How long does it take to see SEO results?"',
    'a: "SEO გრძელვადიანი ინვესტიციაა. პირველი ხელშესახები ცვლილებები, როგორც წესი, 3-დან 6 თვემდე პერიოდში ჩნდება, თუმცა ზუსტი ვადები დამოკიდებულია იმაზე, თუ რამდენად დიდია კონკურენცია თქვენს სფეროში და რა მდგომარეობაშია საიტი მუშაობის დაწყების მომენტში."':
        'a: "SEO is a long-term investment. The first noticeable changes typically appear within 3 to 6 months, though exact timing depends on competition in your industry and the starting condition of your website."',
    'q: "რა ღირს SEO მომსახურება?"': 'q: "How much does SEO cost?"',
    'a: "10xSEO-ში SEO მომსახურების ღირებულება 1880 ლარიდან იწყება. საბოლოო ფასი დამოკიდებულია სამუშაოს სპეციფიკასა და თქვენ მიერ დასახულ მიზნებზე. ჩვენ მაქსიმალურად ვერგებით პარტნიორი კომპანიის ინტერესებს, რათა თანამშრომლობა ორივე მხარისთვის მომგებიანი იყოს."':
        'a: "At 10xSEO, SEO services start from $695/month. The final price depends on the scope of work and your specific goals. We adapt to each partner\'s needs to ensure the engagement is profitable for both sides."',
    'q: "როგორ იზომება შედეგები?"': 'q: "How do you measure results?"',
    'a: "წარმატებას სამი ძირითადი კრიტერიუმით ვზომავთ:</p><ul><li>თქვენი პოზიციები Google-ში</li><li>საიტზე შემოსული ადამიანების რაოდენობა</li><li>მათი ქცევა</li></ul><p>ჩვენი მიზანია, საიტზე მოვიზიდოთ არა უბრალოდ ბევრი, არამედ თქვენი პროდუქტით რეალურად დაინტერესებული ადამიანები."':
        'a: "We measure success by three core criteria:</p><ul><li>Your Google rankings</li><li>The volume of visitors coming to your site</li><li>Their on-site behavior</li></ul><p>Our goal is not just to attract many people, but to bring in users genuinely interested in your product."',
    'q: "რატომ უნდა ავირჩიოთ სააგენტო და არა In-House გუნდი?"': 'q: "Why hire an agency instead of building an in-house team?"',
    'a: "პირველ რიგში, სირთულეს წააწყდებით კადრების აყვანის დროს. SEO კომპლექსური პროცესია სადაც პროექტზე გუნდი მუშაობს – SEO სპეციალისტი, სტრატეგოსი, კონტენტის მწერალი და ვებდეველოპერი."':
        'a: "First, hiring is hard. SEO is a complex process that requires a full team — an SEO specialist, strategist, content writer, and web developer all working together. An agency gives you all of that on day one."',
    'q: "რატომ არის 10xSEO საქართველოში საუკეთესო SEO სააგენტო?"': 'q: "Why is 10xSEO the best SEO agency in Georgia?"',
    'a: "ჩვენ არ გთავაზობთ მხოლოდ SEO სერვისს – ჩვენ ვმუშაობთ თქვენი ბიზნესის რეალური მიზნებისა და შედეგებისთვის. გვაქვს სრულფასოვანი \\"Done-for-You\\" პაკეტი, რომელიც AI-ით მხარდაჭერილ AEO/GEO ოპტიმიზაციას, დეტალურად გაზომვად შედეგებსა და მაღალკვალიფიციურ პროექტ მენეჯმენტს მოიცავს. ჩვენი გუნდი შედგება 12+ წლიანი გამოცდილების მქონე სპეციალისტებისგან. დაბოლოს, თუ თავად გადაწყვეტთ სეო სააგენტოების შედარებას, მარტივად დარწმუნდებით, რომ ჩვენი სერვისი უნიკალურია."':
        'a: "We don\'t just sell SEO services — we work toward your real business goals and outcomes. Our \\"Done-for-You\\" package combines AI-powered AEO/GEO optimization, granular measurement, and senior project management. Our team has 12+ years of experience. Compare us against any SEO agency in Tbilisi or Georgia and you\'ll see our service is unique."',
    'q: "რა სახის ანგარიშებს მივიღებ და რა სიხშირით?"': 'q: "What kind of reports will I receive and how often?"',
    'a: "თქვენ გექნებათ მუდმივი წვდომა მონაცემთა პანელზე, სადაც შედეგებს რეალურ დროში ნახავთ. ამასთან, ყოველ ორ კვირაში მოგაწვდით ინფორმაციას პოზიციების განახლების შესახებ, ხოლო თვის ბოლოს მიიღებთ შემაჯამებელ, დეტალურ ვიდეომიმოხილვას. ნებისმიერ კითხვაზე პასუხს კი სამუშაო საათებში მაქსიმუმ 10 წუთში დაგიბრუნებთ."':
        'a: "You\'ll have constant access to a live data dashboard where you can see results in real time. Every two weeks we send a ranking update, and at month-end you get a comprehensive video review. We respond to any question within 10 minutes during business hours."',
    'q: "როგორ ზომავთ SEO-ს ROI-ს?"': 'q: "How do you measure SEO ROI?"',
    'a: "როცა საკმარისი მონაცემები გვაქვს, ROI-ს ვზომავთ რეალური გაყიდვებით — რამდენი შემოსავალი შემოვიდა ორგანული არხიდან. თუ მონაცემები ჯერ საკმარისი არ არის, საზომად ვიყენებთ საკვანძო სიტყვების საშუალო პოზიციის ზრდას ან ორგანული ტრაფიკის მატებას."':
        'a: "When we have enough data, we measure ROI by actual sales — how much revenue came through the organic channel. If data is still limited, we benchmark by average keyword position improvement or organic traffic growth."',
    'q: "რა გჭირდებათ ჩემგან, რომ დავიწყოთ?"': 'q: "What do you need from me to get started?"',
    'a: "მინიმალური ჩართულობა. თქვენგან გვჭირდება მხოლოდ ბიზნესის სპეციფიკის ცოდნა, კონტენტის თემების დამტკიცება და ტექნიკური წვდომა (Google Analytics, Search Console, საიტის ადმინი). დანარჩენს — სტრატეგიას, კონტენტს, ოპტიმიზაციას, რეპორტინგს — ჩვენ ვაკეთებთ."':
        'a: "Minimal involvement. We need only your domain knowledge, content topic approval, and technical access (Google Analytics, Search Console, site admin). Everything else — strategy, content, optimization, reporting — we handle."',
    'q: "ვინ არის ის კლიენტი, ვისაც არ აიყვანდით — და რატომ?"': 'q: "Which clients do you turn away — and why?"',
    'a: "ხშირად უარს ვამბობთ კლიენტებზე, რომლებსაც: (1) ბიზნეს-მოდელი ჯერ არ აქვთ გამართული, მაგრამ უცხო ბაზრებზე გასვლა უნდათ; (2) საიტის კოდზე წვდომას არ გვაძლევენ და მაინც ტექნიკურ SEO-ს ითხოვენ; (3) უკვე უარყოფითი ბრენდის რეპუტაცია აქვთ, რომელიც PR-ს მოითხოვს, არა SEO-ს. პირველი 30-წუთიანი ზარი ყოველთვის ორმხრივი შესაბამისობის შემოწმებაა — თქვენ გვაფასებთ ჩვენ, ჩვენ კი — თქვენ."':
        'a: "We often decline clients who: (1) don\'t have their business model figured out yet but want to expand internationally; (2) refuse code access yet expect technical SEO; (3) already have negative brand reputation that requires PR, not SEO. The first 15-minute call is always a mutual fit check — you evaluate us, we evaluate you."',
    'q: "როცა კონტრაქტი დასრულდება — რა მოხდება ჩემი რანკინგებით?"': 'q: "What happens to my rankings when our contract ends?"',
    'a: "რანკინგი რჩება, თუ ბექლინკები რეალურია და კონტენტი სრულფასოვანი — ჩვენი 100% white-hat მიდგომით სწორედ ასე გექნებათ. მონიტორინგისა და ახალი კონტენტის გარეშე კონკურენტებმა თანდათან შეიძლება გადაგასწრონ, მაგრამ ეს ნელი პროცესია — არა მკვეთრი ვარდნა, რომელიც PBN-ის ან ყალბი ბექლინკების გათიშვისას ხდება ხოლმე."':
        'a: "Rankings stay if the backlinks are real and the content is solid — that\'s exactly what our 100% white-hat approach delivers. Without monitoring and fresh content, competitors may slowly catch up, but it\'s a gradual decline — not the cliff drop that happens when a PBN or fake backlinks get cut off."',
    'q: "შესაძლებელია თუ არა თქვენთან გადმოსვლა, თუ უკვე ვმუშაობ სხვა SEO სააგენტოსთან?"': 'q: "Can I switch to you if I\'m already working with another SEO agency?"',
    'a: "დიახ, პროცესში ჩართვა ნებისმიერ ეტაპზე შეგვიძლია. პირველ ორ კვირაში ჩავატარებთ წინა სამუშაო პროცესის სრულ აუდიტს და მოვაწესრიგებთ ყველა ტექნიკურ საკითხს. ამის შემდეგ კი გამოვასწორებთ იმ შეცდომებს, რომლებიც აქამდე შედეგის მიღებაში გიშლიდათ ხელს."':
        'a: "Yes, we can pick up at any stage. The first two weeks we run a complete audit of the prior workflow and clean up all technical issues. After that, we fix the mistakes that have been blocking your results."',
    'q: "წინა სააგენტო Black-hat ლინკებს ყიდდა — დაწყებამდე შეგიძლიათ შეაფასოთ, მემუქრება თუ არა Google-ის ჯარიმა?"': 'q: "My previous agency bought black-hat links — can you assess my Google penalty risk before we start?"',
    'a: "კი. პირველი 7 დღე — ბექლინკების ტოქსიკურობის აუდიტი (Ahrefs + SEMrush + ხელით შემოწმება). თუ რისკი გამოვლინდება, disavow ფაილს ვამზადებთ Google-სთვის. ეს ჩვენი თანამშრომლობამდე ჩატარებული დიაგნოსტიკის ნაწილია — დამატებითი ფასის გარეშე. ამის მიზანი — Google-ის შესაძლო ჯარიმისგან თქვენი რეპუტაციის დაცვაა."':
        'a: "Yes. The first 7 days are a backlink toxicity audit (Ahrefs + SEMrush + manual review). If risk is detected, we prepare a disavow file for Google. This pre-engagement diagnostic is included free — its purpose is to protect your reputation from a potential Google penalty."',
    'q: "ვაკეთებ საიტის რემონტს ან მიგრაციას — რანკინგის შენარჩუნებაზე ვინ არის პასუხისმგებელი, დეველოპერი თუ თქვენ?"': 'q: "I\'m doing a site rebuild or migration — who owns ranking preservation, the developer or you?"',
    'a: "ჩვენ. დეველოპერთან ერთად მუშაობს ჩვენი ტექნიკური SEO სპეციალისტი — მიგრაციამდე აუდიტი, URL mapping და 301 redirect-ების ფაილი, სატესტო გარემოს შემოწმება გაშვებამდე, გაშვების შემდგომი მონიტორინგი 30 დღის განმავლობაში. ჩვენი შესრულებული მიგრაციების საშუალო ტრაფიკის კლება <5%-ია (ინდუსტრიის საშუალო 30-50%)."':
        'a: "We do. Our technical SEO specialist works alongside your developer — pre-migration audit, URL mapping and a 301 redirect file, staging environment QA before launch, post-launch monitoring for 30 days. Our average migration traffic loss is <5% (industry average: 30-50%)."',

    # Blog section
    '<p class="text-sm font-semibold text-primary dark:text-primary-light uppercase tracking-wider mb-3">ბლოგი</p>':
        '<p class="text-sm font-semibold text-primary dark:text-primary-light uppercase tracking-wider mb-3">Blog</p>',
    '>ბოლო სტატიები<': '>Latest Articles<',
    'ყველა სტატია': 'All articles',
    'alt="ქოფირაითინგი"': 'alt="Copywriting strategy"',
    '<span>2026 მარტი</span>': '<span>March 2026</span>',
    '<span>2026 თებერვალი</span>': '<span>February 2026</span>',
    '<span>6 წუთი</span>': '<span>6 min</span>',
    '<span>5 წუთი</span>': '<span>5 min</span>',
    '<span>8 წუთი</span>': '<span>8 min</span>',
    'ქოფირაითინგი: სტრატეგია ეფექტური კომუნიკაციისთვის': 'Copywriting: A strategy for effective communication',
    'ეფექტური ქოფირაითინგი ბიზნესისთვის: გაიგეთ, როგორ შეიძლება სიტყვებმა გაყიდოს პროდუქტი...':
        'Effective copywriting for business: learn how words can sell a product...',
    'alt="ლოკალური SEO"': 'alt="Local SEO"',
    'ლოკალური SEO - როგორ მოვიზიდოთ კლიენტები Google Maps-დან': 'Local SEO — How to attract customers from Google Maps',
    'ლოკალური SEO-ს სტრატეგიები, პრაქტიკული რჩევები და ინსტრუმენტები...':
        'Local SEO strategies, practical tips, and tools...',
    'alt="საუკეთესო SEO სააგენტო საქართველოში"': 'alt="Best SEO agency in Georgia"',
    'რატომ არის 10xSEO საუკეთესო SEO სააგენტო საქართველოში?': 'Why is 10xSEO the best SEO agency in Georgia?',
    'რატომ ირჩევენ ლიდერები 10xSEO-ს? რადგან ეს არის საქართველოში #1 SEO სააგენტო...':
        'Why do leaders choose 10xSEO? Because it is the #1 SEO agency in Georgia...',

    # Contact section
    '<p class="text-sm text-body dark:text-body-dark">ტელეფონი</p>': '<p class="text-sm text-body dark:text-body-dark">Phone</p>',
    '<p class="text-sm text-body dark:text-body-dark">ემაილი</p>': '<p class="text-sm text-body dark:text-body-dark">Email</p>',
    '<p class="text-sm text-body dark:text-body-dark">მისამართი</p>': '<p class="text-sm text-body dark:text-body-dark">Address</p>',
    'ბახტრიონის ქუჩა 8, თბილისი 0194': '8 Bakhtrioni Street, Tbilisi 0194, Georgia',
    '<p class="text-sm text-body dark:text-body-dark">სამუშაო საათები</p>': '<p class="text-sm text-body dark:text-body-dark">Business hours</p>',
    'ორშ-პარ:': 'Mon-Fri:',
    '<p class="font-heading text-xl font-bold text-heading dark:text-heading-dark mb-8">დაჯავშნეთ შეხვედრა</p>':
        '<p class="font-heading text-xl font-bold text-heading dark:text-heading-dark mb-8">Book a meeting</p>',
    '>აირჩიეთ<': '>Choose<',
    '15-წუთიანი უფასო კონსულტაცია': '15-minute free consultation',

    # Footer columns
    '<p class="font-heading text-white font-semibold text-sm uppercase tracking-wider mb-4">სერვისები</p>':
        '<p class="font-heading text-white font-semibold text-sm uppercase tracking-wider mb-4">Services</p>',
    '<a href="seo-management.html" class="hover:text-white transition-colors">SEO მომსახურება</a>':
        '<a href="seo-management.html" class="hover:text-white transition-colors">SEO Management</a>',
    '<a href="seo-consultation.html" class="hover:text-white transition-colors">SEO კონსულტაცია</a>':
        '<a href="seo-consultation.html" class="hover:text-white transition-colors">SEO Consultation</a>',
    '<a href="seo-strategy.html" class="hover:text-white transition-colors">SEO სტრატეგია</a>':
        '<a href="seo-strategy.html" class="hover:text-white transition-colors">SEO Strategy</a>',
    '<a href="seo-audit.html" class="hover:text-white transition-colors">უფასო SEO აუდიტი</a>':
        '<a href="seo-audit.html" class="hover:text-white transition-colors">Free SEO Audit</a>',
    '<a href="seo-copywriting.html" class="hover:text-white transition-colors">SEO კოპირაიტინგი</a>':
        '<a href="seo-copywriting.html" class="hover:text-white transition-colors">SEO Copywriting</a>',
    '<p class="font-heading text-white font-semibold text-sm uppercase tracking-wider mb-4">ინსტრუმენტები</p>':
        '<p class="font-heading text-white font-semibold text-sm uppercase tracking-wider mb-4">Tools</p>',
    '<a href="seo-tools.html" class="hover:text-white transition-colors">SEO ინსტრუმენტები</a>':
        '<a href="seo-tools.html" class="hover:text-white transition-colors">SEO Tools</a>',
    '<p class="font-heading text-white font-semibold text-sm uppercase tracking-wider mb-4">ისწავლე</p>':
        '<p class="font-heading text-white font-semibold text-sm uppercase tracking-wider mb-4">Learn</p>',
    '<a href="ra-aris-seo.html" class="hover:text-white transition-colors">რა არის SEO</a>':
        '<a href="ra-aris-seo.html" class="hover:text-white transition-colors">What is SEO</a>',
    '<a href="seo-leqsikoni.html" class="hover:text-white transition-colors">SEO ლექსიკონი</a>':
        '<a href="seo-leqsikoni.html" hreflang="ka" class="hover:text-white transition-colors">SEO Glossary (Georgian)</a>',
    '<a href="startup-leqsikoni.html" class="hover:text-white transition-colors">სტარტაპ ლექსიკონი</a>':
        '<a href="startup-leqsikoni.html" hreflang="ka" class="hover:text-white transition-colors">Startup Glossary (Georgian)</a>',
    '<a href="ai-leqsikoni.html" class="hover:text-white transition-colors">AI ლექსიკონი</a>':
        '<a href="ai-leqsikoni.html" hreflang="ka" class="hover:text-white transition-colors">AI Glossary (Georgian)</a>',
    '<a href="seo-course.html" class="hover:text-white transition-colors">SEO კურსი</a>':
        '<a href="seo-course.html" class="hover:text-white transition-colors">SEO Course</a>',
    '<a href="blog.html" class="hover:text-white transition-colors">ბლოგი</a>':
        '<a href="blog.html" hreflang="ka" class="hover:text-white transition-colors">Blog (Georgian)</a>',
    '<p class="font-heading text-white font-semibold text-sm uppercase tracking-wider mb-4">ინდუსტრიები</p>':
        '<p class="font-heading text-white font-semibold text-sm uppercase tracking-wider mb-4">Industries</p>',
    '<a href="industries/construction.html" class="hover:text-white transition-colors">სამშენებლო &amp; უძრავი ქონება</a>':
        '<a href="industries/construction.html" class="hover:text-white transition-colors">Construction &amp; Real Estate</a>',
    '<a href="industries/healthcare.html" class="hover:text-white transition-colors">ჯანდაცვა</a>':
        '<a href="industries/healthcare.html" class="hover:text-white transition-colors">Healthcare</a>',
    '<a href="industries/financial-services.html" class="hover:text-white transition-colors">ფინანსური სერვისები</a>':
        '<a href="industries/financial-services.html" class="hover:text-white transition-colors">Financial Services</a>',
    '<p class="font-heading text-white font-semibold text-sm uppercase tracking-wider mb-4">კომპანია</p>':
        '<p class="font-heading text-white font-semibold text-sm uppercase tracking-wider mb-4">Company</p>',
    '<a href="about-us.html" class="hover:text-white transition-colors">ჩვენს შესახებ</a>':
        '<a href="about-us.html" class="hover:text-white transition-colors">About Us</a>',
    '<a href="portfolio.html" class="hover:text-white transition-colors">პორტფოლიო</a>':
        '<a href="portfolio.html" class="hover:text-white transition-colors">Portfolio</a>',
    '<a href="vacancies.html" class="hover:text-white transition-colors">ვაკანსიები</a>':
        '<a href="vacancies.html" class="hover:text-white transition-colors">Careers</a>',
    '<a href="contact-us.html" class="hover:text-white transition-colors">კონტაქტი</a>':
        '<a href="contact-us.html" class="hover:text-white transition-colors">Contact</a>',
    '<p class="font-heading text-white font-semibold text-sm uppercase tracking-wider mb-4">კონტაქტი</p>':
        '<p class="font-heading text-white font-semibold text-sm uppercase tracking-wider mb-4">Contact</p>',
    'საქართველოს #1 SEO სააგენტო. &copy; 2026 ყველა უფლება დაცულია.':
        "Georgia's #1 SEO Agency. &copy; 2026 All rights reserved.",

    # Inner-text-after-svg edge cases (button + svg child + text)
    # Pattern: <button data-en="X">\nKA_TEXT\n<svg>...
    # The auto-swap regex skips these because there's an SVG between text and closing tag.
    'data-en="Services">\nსერვისები': 'data-en="Services">\nServices',
    'data-en="Copywriting">\nკოპირაიტინგი': 'data-en="Copywriting">\nCopywriting',
    'data-en="Industries">\nინდუსტრიები': 'data-en="Industries">\nIndustries',
    'data-en="Book Consultation">\nდაჯავშნეთ კონსულტაცია': 'data-en="Book Consultation">\nBook Consultation',
    'data-en="Call Us">\nდაგვირეკეთ': 'data-en="Call Us">\nCall Us',

    # Inner text where parent has <span> child + text (gradient title)
    'data-ka="მზად ხარ იყო პირველი?" data-en="Ready to be #1?">მზად ხარ იყო პირველი?':
        'data-ka="მზად ხარ იყო პირველი?" data-en="Ready to be #1?">Ready to be #1?',

    # Hero: choose your direction (h2 with span)
    '<h2 class="font-heading text-[24px] sm:text-[30px] lg:text-[36px] font-bold text-heading-dark leading-[1.3]">\nაირჩიეთ სასურველი მიმართულება':
        '<h2 class="font-heading text-[24px] sm:text-[30px] lg:text-[36px] font-bold text-heading-dark leading-[1.3]">\nChoose your direction',

    # Local SEO case study card (line 801)
    '+1500 ზარი': '+1500 calls',

    # Blog header (different phrasing)
    '>უახლესი პუბლიკაციები<': '>Latest Articles<',

    # Contact section "აირჩიეთ" by itself (different from "აირჩიეთ სასურველი მიმართულება")
    '>\nაირჩიეთ\n': '>\nChoose\n',

    # Blog (the actual headline text — different from BODY_TRANSLATIONS earlier)
    'Local SEO - როგორ მოვიზიდოთ კლიენტები Google Maps-დან':
        'Local SEO — How to attract customers from Google Maps',
    'Local SEO-ს სტრატეგიები, პრაქტიკული რჩევები და ინსტრუმენტები...':
        'Local SEO strategies, practical tips, and tools...',

    # JS month-name arrays (cosmetic — appear in counter widget)
    "const monthNamesKa = ['იანვარში', 'თებერვალში', 'მარტში', 'აპრილში', 'მაისში', 'ივნისში', 'ივლისში', 'აგვისტოში', 'სექტემბერში', 'ოქტომბერში', 'ნოემბერში', 'დეკემბერში'];":
        "const monthNamesKa = ['in January', 'in February', 'in March', 'in April', 'in May', 'in June', 'in July', 'in August', 'in September', 'in October', 'in November', 'in December'];",
    "const monthNames = ['იანვარში', 'თებერვალში', 'მარტში', 'აპრილში', 'მაისში', 'ივნისში', 'ივლისში', 'აგვისტოში', 'სექტემბერში', 'ოქტომბერში', 'ნოემბერში', 'დეკემბერში'];":
        "const monthNames = ['in January', 'in February', 'in March', 'in April', 'in May', 'in June', 'in July', 'in August', 'in September', 'in October', 'in November', 'in December'];",

    # "Recommended" badge inside service nav link (text + child span)
    'რეკომენდებული</span>': 'Recommended</span>',
    'YouTube არხი</a>': 'YouTube Channel</a>',
    # SEO მომსახურება + recommended badge — need to swap inner since auto-swap can't (nested span)
    'data-en="SEO Management">SEO მომსახურება <span': 'data-en="SEO Management">SEO Management <span',

    # Multi-line patterns: data-en + svg + KA text
    # "Call Us" button (hero or contact area) — text after svg
    "</svg>\nდაგვირეკეთ\n</a>": "</svg>\nCall Us\n</a>",
    # Book Consultation button — text after svg arrow
    "</svg>\n</a>\n<a href=\"tel:": "</svg>\n</a>\n<a href=\"tel:",  # no-op, just safety
    # Hero "Book Consultation" button is wrapped: text BEFORE svg arrow
    'data-en="Book Consultation">\nდაჯავშნეთ კონსულტაცია\n<svg':
        'data-en="Book Consultation">\nBook Consultation\n<svg',
    # CTA banner "Book Consultation" link without svg before — likely just text + tag
    '>დაჯავშნეთ კონსულტაცია\n<svg': '>Book Consultation\n<svg',

    # Fallback: any standalone "დაჯავშნეთ კონსულტაცია" line wrapped in tags
    "\nდაჯავშნეთ კონსულტაცია\n": "\nBook Consultation\n",

    # === LANGUAGE SWITCHER (EN active) ===
    '<button id="lang-toggle" class="hidden sm:flex items-center gap-1 px-2.5 py-1.5 text-xs font-semibold rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800/50 text-heading dark:text-heading-dark transition-colors">\n<span id="lang-ka" class="text-primary font-bold">KA</span>\n<span class="opacity-50">/</span>\n<span id="lang-en" class="opacity-50">EN</span>\n</button>':
        '<a href="../index.html" id="lang-toggle" class="hidden sm:flex items-center gap-1 px-2.5 py-1.5 text-xs font-semibold rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800/50 text-heading dark:text-heading-dark transition-colors" hreflang="ka" aria-label="Switch to Georgian">\n<span id="lang-ka" class="opacity-50">KA</span>\n<span class="opacity-50">/</span>\n<span id="lang-en" class="text-primary font-bold">EN</span>\n</a>',

}

# -------- 8. SKIPPED-PAGE LINK REWRITES (Phase 3 — applied AFTER body translations) --------
# Skipped pages (blog, dictionaries) have no /en/ counterpart, so links must
# escape the /en/ subtree. Each rewrite adds hreflang="ka" + "(Georgian)"
# label and prepends "../" to the href.
SKIPPED_LINK_REWRITES = {
    # Footer dictionary + blog links: href="<page>.html" → href="../<page>.html"
    'href="seo-leqsikoni.html"': 'href="../seo-leqsikoni.html" hreflang="ka"',
    'href="startup-leqsikoni.html"': 'href="../startup-leqsikoni.html" hreflang="ka"',
    'href="ai-leqsikoni.html"': 'href="../ai-leqsikoni.html" hreflang="ka"',
    'href="blog.html"': 'href="../blog.html" hreflang="ka"',
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true',
                        help='Print summary without writing the file')
    args = parser.parse_args()

    if not KA_FILE.exists():
        print(f"ERROR: source file not found: {KA_FILE}", file=sys.stderr)
        return 1

    html = KA_FILE.read_text(encoding='utf-8-sig')
    original_size = len(html)

    # Phase 1: structural replacements (lang, canonical, meta, schema)
    applied = 0
    not_found = []
    for i, (old, new) in enumerate(REPLACEMENTS, 1):
        if old in html:
            html = html.replace(old, new)
            applied += 1
        else:
            not_found.append((i, old[:80] + '...' if len(old) > 80 else old))

    # Phase 2a: auto-swap data-ka/data-en inner text
    html, swap_count = swap_data_en_inner_text(html)

    # Phase 2b: explicit body translations.
    # Apply LONGEST keys first so multi-word phrases match before
    # shorter words that could be substrings of those phrases.
    body_applied = 0
    body_missed = []
    sorted_translations = sorted(BODY_TRANSLATIONS.items(), key=lambda kv: -len(kv[0]))
    for i, (old, new) in enumerate(sorted_translations, 1):
        if old in html:
            html = html.replace(old, new)
            body_applied += 1
        else:
            body_missed.append((i, old[:80] + '...' if len(old) > 80 else old))

    # Phase 3: skipped-page link rewrites (applied after body translations
    # because they depend on the post-translation HTML state)
    skip_applied = 0
    for old, new in SKIPPED_LINK_REWRITES.items():
        # Only rewrite if hreflang isn't already present (idempotent)
        if old in html and 'hreflang="ka"' not in html.split(old, 1)[1][:50]:
            html = html.replace(old, new)
            skip_applied += 1
    print(f"Phase 3 (skipped link rewrites): {skip_applied}/{len(SKIPPED_LINK_REWRITES)} applied")

    new_size = len(html)
    print(f"Source:  {KA_FILE} ({original_size} bytes)")
    print(f"Target:  {EN_FILE} ({new_size} bytes; Δ {new_size - original_size:+d})")
    print(f"Phase 1 (structural): {applied}/{len(REPLACEMENTS)} replacements")
    print(f"Phase 2a (data-en auto-swap): {swap_count} elements swapped")
    print(f"Phase 2b (body explicit): {body_applied}/{len(BODY_TRANSLATIONS)} replacements")

    if not_found:
        print(f"\n⚠ Phase 1 — {len(not_found)} replacements did NOT match:")
        for idx, snippet in not_found:
            print(f"  #{idx}: {snippet}")

    if body_missed:
        print(f"\n⚠ Phase 2b — {len(body_missed)} body translations did NOT match:")
        for idx, snippet in body_missed:
            print(f"  #{idx}: {snippet}")

    # Sanity check: any Georgian Unicode left in the result?
    ka_re = re.compile(r'[Ⴀ-ჿ]')
    leftover_lines = []
    for lineno, line in enumerate(html.split('\n'), 1):
        if ka_re.search(line):
            # Skip lines that are JS month name arrays (intentional)
            if 'monthNames' in line and 'KA' in line:
                continue
            # Skip data-ka="..." attribute values (those should remain as-is for switcher)
            stripped = re.sub(r'data-ka="[^"]*"', '', line)
            if ka_re.search(stripped):
                leftover_lines.append((lineno, line[:200]))

    if leftover_lines:
        print(f"\n📋 {len(leftover_lines)} lines still contain Georgian text (Phase 2: visible-text translation):")
        for lineno, snippet in leftover_lines[:30]:
            print(f"  L{lineno}: {snippet}")
        if len(leftover_lines) > 30:
            print(f"  ... and {len(leftover_lines)-30} more")

    if args.dry_run:
        print("\nDRY-RUN — no file written.")
        return 0

    EN_FILE.parent.mkdir(parents=True, exist_ok=True)
    EN_FILE.write_text(html, encoding='utf-8')
    print(f"\n✓ Wrote {EN_FILE}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
