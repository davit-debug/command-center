#!/usr/bin/env python3
"""Translate any KA page to EN. Common transforms shared across all pages,
per-page text translations defined below.

Usage:
  python3 scripts/translate-all.py --page services.html
  python3 scripts/translate-all.py --all
  python3 scripts/translate-all.py --page services.html --dry-run

Layered transforms (in order):
  1. STRUCTURAL: lang, canonical, hreflang, og:*, twitter:*, Calendly URL
  2. SCHEMA: JSON-LD inLanguage, breadcrumb, page-specific @id/url/name
  3. AUTO-SWAP: data-ka/data-en inner text replacement (header/footer chrome)
  4. COMMON_BODY: shared body translations (footer columns, etc.)
  5. PAGE_BODY: page-specific body translations
  6. SKIPPED_LINKS: rewrite /blog, /seo-leqsikoni, etc. → ../path with hreflang="ka"
  7. LANG_SWITCHER: EN-active toggle linking back to KA root
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://10xseo.ge"

# Translated pages (have /en/ counterpart)
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
KA_ONLY_PAGES = {'blog.html', 'seo-leqsikoni.html', 'ai-leqsikoni.html', 'startup-leqsikoni.html'}
KA_ONLY_PREFIXES = ('blog/',)


# ============================================================
# COMMON TRANSFORMS — shared across ALL pages
# ============================================================

def common_structural_replacements(ka_path: str, en_path: str):
    """Generate (old, new) pairs for structural meta tags.
    ka_path = e.g. "services.html" or "case-studies/foo.html" (relative)
    en_path = e.g. "en/services.html" (relative)
    """
    ka_url = f"{DOMAIN}/{ka_path}" if ka_path != "index.html" else f"{DOMAIN}/"
    en_url = f"{DOMAIN}/{en_path}" if en_path != "en/index.html" else f"{DOMAIN}/en/"

    return [
        # Lang
        ('<html lang="ka"', '<html lang="en"'),
        # Skip-nav
        ('გადახტომა მთავარ შინაარსზე', 'Skip to main content'),
        # og:locale
        ('<meta property="og:locale" content="ka_GE">',
         '<meta property="og:locale" content="en_US">\n<meta property="og:locale:alternate" content="ka_GE">'),
        # Canonical (with hreflang block injection)
        (f'<link rel="canonical" href="{ka_url}">',
         f'<link rel="canonical" href="{en_url}">\n'
         f'<link rel="alternate" hreflang="ka" href="{ka_url}">\n'
         f'<link rel="alternate" hreflang="en" href="{en_url}">\n'
         f'<link rel="alternate" hreflang="x-default" href="{ka_url}">'),
        # og:url
        (f'<meta property="og:url" content="{ka_url}">',
         f'<meta property="og:url" content="{en_url}">'),
        # Calendly URL (separate English event per user decision 2026-05-10)
        ('calendly.com/10xseo-sales/30-seo-clone',
         'calendly.com/10xseo-sales/quick-seo-consultation-15-minutes'),
        # JSON-LD inLanguage
        ('"inLanguage":"ka-GE"', '"inLanguage":"en-US"'),
        ('"inLanguage": "ka-GE"', '"inLanguage": "en-US"'),
        # JSON-LD address (transliterated)
        ('"streetAddress": "ბახტრიონის ქუჩა 8"', '"streetAddress": "8 Bakhtrioni Street"'),
        ('"addressLocality": "თბილისი"', '"addressLocality": "Tbilisi"'),
        # Common knowsAbout in Person schema
        ('"knowsAbout":["SEO","ტექნიკური SEO","On-Page SEO","Link Building","Content Marketing","Keyword Research","AEO","GEO","Local SEO"]',
         '"knowsAbout":["SEO","Technical SEO","On-Page SEO","Link Building","Content Marketing","Keyword Research","AEO","GEO","Local SEO"]'),
    ]


# ============================================================
# COMMON BODY TRANSLATIONS — header chrome, footer, etc.
# ============================================================

COMMON_BODY = {
    # ARIA labels
    'aria-label="მთავარი ნავიგაცია"': 'aria-label="Main navigation"',
    'aria-label="მობილური ნავიგაცია"': 'aria-label="Mobile navigation"',
    'aria-label="მენიუს გახსნა"': 'aria-label="Open menu"',

    # Header nav text-after-svg edge cases (button + svg child + text)
    'data-en="Services">\nსერვისები': 'data-en="Services">\nServices',
    'data-en="Copywriting">\nკოპირაიტინგი': 'data-en="Copywriting">\nCopywriting',
    'data-en="Industries">\nინდუსტრიები': 'data-en="Industries">\nIndustries',
    'data-en="Book Consultation">\nდაჯავშნეთ კონსულტაცია': 'data-en="Book Consultation">\nBook Consultation',
    'data-en="Call Us">\nდაგვირეკეთ': 'data-en="Call Us">\nCall Us',
    "</svg>\nდაგვირეკეთ\n</a>": "</svg>\nCall Us\n</a>",

    # Industry submenu items (no data-en)
    '>სამშენებლო &amp; უძრავი ქონება<': '>Construction &amp; Real Estate<',
    '>კლინიკები &amp; ჯანდაცვა<': '>Healthcare &amp; Clinics<',
    '>ფინანსური სერვისები<': '>Financial Services<',
    '>კოპირაიტინგი<': '>Copywriting<',
    '>ინდუსტრიები<': '>Industries<',
    '>კონტაქტი<': '>Contact<',

    # Mobile nav category labels
    'transition-delay:0.25s">კოპირაიტინგი</p>': 'transition-delay:0.25s">Copywriting</p>',
    'transition-delay:0.43s">ინდუსტრიები</p>': 'transition-delay:0.43s">Industries</p>',

    # Footer column titles
    '<p class="font-heading text-white font-semibold text-sm uppercase tracking-wider mb-4">სერვისები</p>':
        '<p class="font-heading text-white font-semibold text-sm uppercase tracking-wider mb-4">Services</p>',
    '<p class="font-heading text-white font-semibold text-sm uppercase tracking-wider mb-4">ინსტრუმენტები</p>':
        '<p class="font-heading text-white font-semibold text-sm uppercase tracking-wider mb-4">Tools</p>',
    '<p class="font-heading text-white font-semibold text-sm uppercase tracking-wider mb-4">ისწავლე</p>':
        '<p class="font-heading text-white font-semibold text-sm uppercase tracking-wider mb-4">Learn</p>',
    '<p class="font-heading text-white font-semibold text-sm uppercase tracking-wider mb-4">ინდუსტრიები</p>':
        '<p class="font-heading text-white font-semibold text-sm uppercase tracking-wider mb-4">Industries</p>',
    '<p class="font-heading text-white font-semibold text-sm uppercase tracking-wider mb-4">კომპანია</p>':
        '<p class="font-heading text-white font-semibold text-sm uppercase tracking-wider mb-4">Company</p>',
    '<p class="font-heading text-white font-semibold text-sm uppercase tracking-wider mb-4">კონტაქტი</p>':
        '<p class="font-heading text-white font-semibold text-sm uppercase tracking-wider mb-4">Contact</p>',

    # Footer service links
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
    '<a href="seo-tools.html" class="hover:text-white transition-colors">SEO ინსტრუმენტები</a>':
        '<a href="seo-tools.html" class="hover:text-white transition-colors">SEO Tools</a>',
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
    '<a href="industries/construction.html" class="hover:text-white transition-colors">სამშენებლო &amp; უძრავი ქონება</a>':
        '<a href="industries/construction.html" class="hover:text-white transition-colors">Construction &amp; Real Estate</a>',
    '<a href="industries/healthcare.html" class="hover:text-white transition-colors">ჯანდაცვა</a>':
        '<a href="industries/healthcare.html" class="hover:text-white transition-colors">Healthcare</a>',
    '<a href="industries/financial-services.html" class="hover:text-white transition-colors">ფინანსური სერვისები</a>':
        '<a href="industries/financial-services.html" class="hover:text-white transition-colors">Financial Services</a>',
    '<a href="about-us.html" class="hover:text-white transition-colors">ჩვენს შესახებ</a>':
        '<a href="about-us.html" class="hover:text-white transition-colors">About Us</a>',
    '<a href="portfolio.html" class="hover:text-white transition-colors">პორტფოლიო</a>':
        '<a href="portfolio.html" class="hover:text-white transition-colors">Portfolio</a>',
    '<a href="vacancies.html" class="hover:text-white transition-colors">ვაკანსიები</a>':
        '<a href="vacancies.html" class="hover:text-white transition-colors">Careers</a>',
    '<a href="contact-us.html" class="hover:text-white transition-colors">კონტაქტი</a>':
        '<a href="contact-us.html" class="hover:text-white transition-colors">Contact</a>',

    # Address
    'ბახტრიონის ქუჩა 8, თბილისი 0194': '8 Bakhtrioni Street, Tbilisi 0194, Georgia',

    # Copyright
    'საქართველოს #1 SEO სააგენტო. &copy; 2026 ყველა უფლება დაცულია.':
        "Georgia's #1 SEO Agency. &copy; 2026 All rights reserved.",
}


# ============================================================
# PER-PAGE DATA
# ============================================================

PAGES = {
    'services.html': {
        'title_ka': 'SEO სერვისები — სრული ეკოსისტემა თქვენი ბიზნესისთვის | 10XSEO',
        'title_en': '#1 SEO Services in Georgia | Tbilisi SEO Agency — 10xSEO',
        'meta_ka': '10XSEO სერვისები: SEO მომსახურება, AI SEO/GEO, კონვერსიის ოპტიმიზაცია, Google Ads, კოპირაიტინგი, SEO კურსი და უფასო ინსტრუმენტები. საქართველოს #1 SEO სააგენტო.',
        'meta_en': 'Top SEO services in Tbilisi & Georgia. Get SEO management, AI SEO, CRO, Google Ads & copywriting from 10xSEO. Book a free 15-min consult today.',
        'body': {
            # Hero
            '<span class="text-sm font-semibold text-primary-light">12 სერვისი ერთი სააგენტოდან</span>':
                '<span class="text-sm font-semibold text-primary-light">12 services under one agency</span>',
            'SEO სერვისები — სრული ეკოსისტემა <span class="gradient-text">თქვენი ბიზნესის ზრდისთვის</span>':
                'AI-Powered SEO Services <span class="gradient-text">for Ambitious Brands</span>',
            'SEO მომსახურებადან AI ოპტიმიზაციამდე — აირჩიეთ სერვისი თქვენი ბიზნესის საჭიროებების მიხედვით.':
                'From full SEO management to AI search optimization — pick the service that matches your business stage. We serve Tbilisi-based and international brands.',
            '<span class="text-xs text-body dark:text-body-dark">წლის<br>გამოცდილება</span>':
                '<span class="text-xs text-body dark:text-body-dark">years of<br>experience</span>',
            '<span class="text-xs text-body dark:text-body-dark">კმაყოფილი<br>კლიენტი</span>':
                '<span class="text-xs text-body dark:text-body-dark">happy<br>clients</span>',
        },
    },
    'ai-seo.html': {
        'title_ka': 'AI SEO -  იყავით იქ, სადაც პასუხებს ეძებენ | 10xSEO',
        'title_en': 'AI SEO (GEO/AEO) | Rank in ChatGPT, Gemini & Perplexity — 10xSEO',
        'meta_ka': 'მოხვდით ChatGPT-ის, Gemini-სა და Claude-ის პასუხებში. AI SEO სერვისი: GEO და AEO ოპტიმიზაცია თქვენი ბრენდის მაქსიმალური ხილვადობისთვის.',
        'meta_en': 'Get cited in ChatGPT, Gemini, Perplexity & Claude. 10xSEO\'s AI SEO service: GEO + AEO optimization for maximum brand visibility in AI search.',
        'body': {
            'AI SEO (GEO/AEO) —<br>': 'AI SEO (GEO/AEO) —<br>',
            '<span class="ai-gradient-text">ხილვადობა ChatGPT-ში, Gemini-ში და Perplexity-ში</span>':
                '<span class="ai-gradient-text">Visibility in ChatGPT, Gemini & Perplexity</span>',
            'GEO & AEO — გახადეთ თქვენი ბრენდი ხილული <strong class="text-heading dark:text-heading-dark">ChatGPT-ში</strong>, <strong class="text-heading dark:text-heading-dark">Gemini-ში</strong>, <strong class="text-heading dark:text-heading-dark">Perplexity-ში</strong> და <strong class="text-heading dark:text-heading-dark">Claude-ში</strong>.':
                'GEO & AEO — make your brand visible in <strong class="text-heading dark:text-heading-dark">ChatGPT</strong>, <strong class="text-heading dark:text-heading-dark">Gemini</strong>, <strong class="text-heading dark:text-heading-dark">Perplexity</strong> and <strong class="text-heading dark:text-heading-dark">Claude</strong>.',
        },
    },
    'contact-us.html': {
        'title_ka': 'კონტაქტი — დაგვიკავშირდით | 10XSEO',
        'title_en': 'Contact 10xSEO | SEO Agency in Tbilisi, Georgia',
        'meta_ka': 'SEO კონსულტაციისთვის დაგვიკავშირდით. ტელეფონი: 510 10 15 17, ელ.ფოსტა: sales@10xseo.ge. ბახტრიონის ქუჩა 8, თბილისი 0194.',
        'meta_en': 'Contact 10xSEO for an SEO consultation. Phone: +995 510 10 15 17, Email: sales@10xseo.ge. 8 Bakhtrioni Street, Tbilisi 0194, Georgia.',
        'body': {
            '<span class="gradient-text">დაგვიკავშირდით</span>':
                '<span class="gradient-text">Get in Touch</span>',
        },
    },
    'about-us.html': {
        'title_ka': 'ჩვენ შესახებ - 10xSEO',
        'title_en': 'About 10xSEO | The Team Behind Georgia\'s #1 SEO Agency',
        'meta_ka': '10xSEO — SEO სააგენტო, რომელიც ბრენდებს Google-სა და AI პლატფორმებზე #1 პოზიციაზე აყენებს. გაიცანი ჩვენი გუნდი, ხედვა და მიდგომა.',
        'meta_en': 'Meet 10xSEO — Tbilisi\'s top SEO agency. 14 years experience, 50+ clients, white-hat methodology, AI-powered approach for Georgian and global brands.',
        'body': {
            '10xSEO — SEO სააგენტო <span class="accent">#1 საქართველოში</span>':
                '10xSEO — Georgia\'s <span class="accent">#1 SEO Agency</span>',
            '<p class="hero-subtitle reveal">იყავი პირველი იქ, სადაც კლიენტები გეძებენ</p>':
                '<p class="hero-subtitle reveal">Be first where customers search for you</p>',
        },
    },
}


# ============================================================
# AUTO-SWAP — data-ka/data-en inner text replacement
# ============================================================

def swap_data_en_inner_text(html):
    """Swap inner text with data-en value where it matches data-ka value."""
    pattern = re.compile(
        r'(data-ka="([^"]+)"\s+data-en="([^"]+)"[^>]*>)(\s*)([^<]*?)(\s*)(</[a-zA-Z]+>)',
        re.DOTALL
    )
    swaps = [0]

    def replacer(m):
        opening, ka_text, en_text = m.group(1), m.group(2), m.group(3)
        leading_ws, inner, trailing_ws, closing = m.group(4), m.group(5), m.group(6), m.group(7)
        ka_decoded = ka_text.replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
        inner_decoded = inner.replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
        if inner_decoded.strip() == ka_decoded.strip():
            swaps[0] += 1
            return f'{opening}{leading_ws}{en_text}{trailing_ws}{closing}'
        return m.group(0)

    return pattern.sub(replacer, html), swaps[0]


# ============================================================
# SKIPPED-PAGE LINK REWRITES (depth 0 — root pages only)
# ============================================================

SKIPPED_LINK_REWRITES = {
    'href="seo-leqsikoni.html"': 'href="../seo-leqsikoni.html" hreflang="ka"',
    'href="startup-leqsikoni.html"': 'href="../startup-leqsikoni.html" hreflang="ka"',
    'href="ai-leqsikoni.html"': 'href="../ai-leqsikoni.html" hreflang="ka"',
    'href="blog.html"': 'href="../blog.html" hreflang="ka"',
}


# ============================================================
# LANG SWITCHER — EN-active toggle linking back to KA
# ============================================================

LANG_SWITCHER_REPLACEMENTS = {
    # New <a> form (KA index has been updated)
    '<a href="en/index.html" id="lang-toggle" class="hidden sm:flex items-center gap-1 px-2.5 py-1.5 text-xs font-semibold rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800/50 text-heading dark:text-heading-dark transition-colors" hreflang="en" aria-label="Switch to English">\n<span id="lang-ka" class="text-primary font-bold">KA</span>\n<span class="opacity-50">/</span>\n<span id="lang-en" class="opacity-50">EN</span>\n</a>':
        '<a href="../index.html" id="lang-toggle" class="hidden sm:flex items-center gap-1 px-2.5 py-1.5 text-xs font-semibold rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800/50 text-heading dark:text-heading-dark transition-colors" hreflang="ka" aria-label="Switch to Georgian">\n<span id="lang-ka" class="opacity-50">KA</span>\n<span class="opacity-50">/</span>\n<span id="lang-en" class="text-primary font-bold">EN</span>\n</a>',
    # Old <button> form (other pages might still have it before sync runs)
    '<button id="lang-toggle" class="hidden sm:flex items-center gap-1 px-2.5 py-1.5 text-xs font-semibold rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800/50 text-heading dark:text-heading-dark transition-colors">\n<span id="lang-ka" class="text-primary font-bold">KA</span>\n<span class="opacity-50">/</span>\n<span id="lang-en" class="opacity-50">EN</span>\n</button>':
        '<a href="../index.html" id="lang-toggle" class="hidden sm:flex items-center gap-1 px-2.5 py-1.5 text-xs font-semibold rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800/50 text-heading dark:text-heading-dark transition-colors" hreflang="ka" aria-label="Switch to Georgian">\n<span id="lang-ka" class="opacity-50">KA</span>\n<span class="opacity-50">/</span>\n<span id="lang-en" class="text-primary font-bold">EN</span>\n</a>',
}


# ============================================================
# MAIN
# ============================================================

def translate_page(page_name: str, dry_run: bool = False):
    """Translate a single page (relative path like 'services.html')."""
    if page_name not in PAGES:
        print(f"ERROR: page '{page_name}' not in PAGES dict — add metadata first", file=sys.stderr)
        return False

    page_data = PAGES[page_name]
    ka_path = ROOT / page_name
    en_path = ROOT / 'en' / page_name

    if not ka_path.exists():
        print(f"ERROR: source file not found: {ka_path}", file=sys.stderr)
        return False

    html = ka_path.read_text(encoding='utf-8-sig')
    original_size = len(html)

    # Phase 1: Title + meta
    html = html.replace(f'<title>{page_data["title_ka"]}</title>', f'<title>{page_data["title_en"]}</title>')
    html = html.replace(f'content="{page_data["meta_ka"]}"', f'content="{page_data["meta_en"]}"')

    # Phase 2: Common structural transforms
    en_rel_path = f"en/{page_name}"
    structural = common_structural_replacements(page_name, en_rel_path)
    s_applied = 0
    for old, new in structural:
        if old in html:
            html = html.replace(old, new)
            s_applied += 1

    # Phase 3: Auto-swap data-ka/data-en
    html, swap_count = swap_data_en_inner_text(html)

    # Phase 4: Common body translations
    cb_applied = 0
    for old, new in COMMON_BODY.items():
        if old in html:
            html = html.replace(old, new)
            cb_applied += 1

    # Phase 5: Page-specific body translations (sorted longest first)
    pb_applied = 0
    for old, new in sorted(page_data.get('body', {}).items(), key=lambda kv: -len(kv[0])):
        if old in html:
            html = html.replace(old, new)
            pb_applied += 1

    # Phase 6: Skipped-page link rewrites (only for depth-0 pages)
    page_depth = page_name.count('/')
    sl_applied = 0
    if page_depth == 0:  # root page → ../path needed
        for old, new in SKIPPED_LINK_REWRITES.items():
            if old in html and 'hreflang="ka"' not in html.split(old, 1)[1][:50]:
                html = html.replace(old, new)
                sl_applied += 1

    # Phase 7: Lang switcher
    ls_applied = 0
    for old, new in LANG_SWITCHER_REPLACEMENTS.items():
        if old in html:
            html = html.replace(old, new)
            ls_applied += 1

    new_size = len(html)
    print(f"\n=== {page_name} ===")
    print(f"  Source:  {original_size} bytes")
    print(f"  Target:  {new_size} bytes (Δ {new_size - original_size:+d})")
    print(f"  Phase 1 (title+meta): applied")
    print(f"  Phase 2 (structural): {s_applied}/{len(structural)}")
    print(f"  Phase 3 (data-en auto-swap): {swap_count} elements")
    print(f"  Phase 4 (common body): {cb_applied}/{len(COMMON_BODY)}")
    print(f"  Phase 5 (page body): {pb_applied}/{len(page_data.get('body', {}))}")
    print(f"  Phase 6 (skipped links): {sl_applied}/{len(SKIPPED_LINK_REWRITES)}")
    print(f"  Phase 7 (lang switcher): {ls_applied}/{len(LANG_SWITCHER_REPLACEMENTS)}")

    # Sanity check: leftover Georgian
    ka_re = re.compile(r'[Ⴀ-ჿ]')
    leftover_count = 0
    for line in html.split('\n'):
        stripped = re.sub(r'data-ka="[^"]*"', '', line)
        if ka_re.search(stripped):
            leftover_count += 1
    print(f"  Leftover Georgian lines (excluding data-ka attrs): {leftover_count}")

    if dry_run:
        print(f"  DRY-RUN — no file written")
        return True

    en_path.parent.mkdir(parents=True, exist_ok=True)
    en_path.write_text(html, encoding='utf-8')
    print(f"  ✓ Wrote {en_path}")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--page', type=str, help='Page to translate (e.g. services.html)')
    parser.add_argument('--all', action='store_true', help='Translate all pages in PAGES dict')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    if args.all:
        for page in PAGES:
            translate_page(page, dry_run=args.dry_run)
    elif args.page:
        translate_page(args.page, dry_run=args.dry_run)
    else:
        print("Available pages:")
        for p in PAGES:
            print(f"  --page {p}")
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
