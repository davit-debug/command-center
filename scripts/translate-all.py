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

    # Skipped-page link inner text (works regardless of href depth)
    '>SEO ლექსიკონი</a>': '>SEO Glossary (Georgian)</a>',
    '>სტარტაპ ლექსიკონი</a>': '>Startup Glossary (Georgian)</a>',
    '>AI ლექსიკონი</a>': '>AI Glossary (Georgian)</a>',

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
            'SEO მომსახურებიდან AI ოპტიმიზაციამდე — აირჩიეთ სერვისი თქვენი ბიზნესის საჭიროებების მიხედვით.':
                'From full SEO management to AI search optimization — pick the service that matches your business stage. We serve Tbilisi-based and international brands.',
            '<span class="text-xs text-body dark:text-body-dark">წლის<br>გამოცდილება</span>':
                '<span class="text-xs text-body dark:text-body-dark">years of<br>experience</span>',
            '<span class="text-xs text-body dark:text-body-dark">კმაყოფილი<br>კლიენტი</span>':
                '<span class="text-xs text-body dark:text-body-dark">happy<br>clients</span>',
            '<span class="text-xs text-body dark:text-body-dark">ინდუსტრია<br>დაფარული</span>':
                '<span class="text-xs text-body dark:text-body-dark">industries<br>covered</span>',

            # Breadcrumbs
            '<a href="index.html" class="text-body/60 dark:text-body-dark/60 hover:text-primary transition-colors">მთავარი</a>':
                '<a href="index.html" class="text-body/60 dark:text-body-dark/60 hover:text-primary transition-colors">Home</a>',
            '<span class="text-heading dark:text-heading-dark font-medium">სერვისები</span>':
                '<span class="text-heading dark:text-heading-dark font-medium">Services</span>',

            # Quick nav pills
            '>ძირითადი სერვისები</a>': '>Core Services</a>',
            '>სპეციალიზებული</a>': '>Specialized</a>',
            '>ინსტრუმენტები</a>': '>Tools</a>',
            '>უფასო აუდიტი</a>': '>Free Audit</a>',

            # Tier 1 section headers
            '<p class="text-sm font-semibold text-primary-light uppercase tracking-wider mb-3">ძირითადი სერვისები</p>':
                '<p class="text-sm font-semibold text-primary-light uppercase tracking-wider mb-3">Core Services</p>',
            '<h2 class="font-heading text-2xl sm:text-3xl lg:text-4xl font-extrabold text-heading dark:text-heading-dark">სრული SEO მართვა თქვენი ბიზნესისთვის</h2>':
                '<h2 class="font-heading text-2xl sm:text-3xl lg:text-4xl font-extrabold text-heading dark:text-heading-dark">Complete SEO Management for Your Business</h2>',

            # "Recommended" badge
            'რეკომენდებული</span>': 'Recommended</span>',

            # Tier 1 service cards
            '<h3 class="font-heading text-2xl lg:text-3xl font-bold text-heading dark:text-heading-dark mb-3">SEO მომსახურება <span class="text-lg text-body-dark/60 font-normal">(Done-For-You)</span></h3>':
                '<h3 class="font-heading text-2xl lg:text-3xl font-bold text-heading dark:text-heading-dark mb-3">SEO Management <span class="text-lg text-body-dark/60 font-normal">(Done-For-You)</span></h3>',
            '<p class="text-body dark:text-body-dark leading-relaxed mb-5">სრული SEO მართვა — Keyword Research, ტექნიკური ოპტიმიზაცია, კონტენტი, Link Building, AEO/GEO. Live Dashboard რეპორტინგი და 10-წუთიანი SLA.</p>':
                '<p class="text-body dark:text-body-dark leading-relaxed mb-5">Full-stack SEO management — keyword research, technical optimization, content, link building, AEO/GEO. Live dashboard reporting and 10-minute SLA.</p>',
            '<span class="text-sm text-body-dark/60">/თვე-დან</span>': '<span class="text-sm text-body-dark/60">/mo, starting at</span>',

            # Service feature lists
            '>ტექნიკური ოპტიმიზაცია</li>': '>Technical optimization</li>',
            '>კონტენტი & Link Building</li>': '>Content & link building</li>',
            '>AEO/GEO ოპტიმიზაცია</li>': '>AEO/GEO optimization</li>',

            # CTA buttons
            'გაიგეთ მეტი': 'Learn more',

            # Stats labels
            '<span class="text-sm text-body-dark">წლის გამოცდილება<br>SEO ინდუსტრიაში</span>':
                '<span class="text-sm text-body-dark">years experience<br>in the SEO industry</span>',
            '<span class="text-sm text-body-dark">საშუალო ტრაფიკის<br>ზრდა პარტნიორებში</span>':
                '<span class="text-sm text-body-dark">average traffic<br>growth across clients</span>',
            '<span class="font-inter text-3xl font-extrabold text-accent">10 წთ</span>':
                '<span class="font-inter text-3xl font-extrabold text-accent">10 min</span>',
            '<span class="text-sm text-body-dark">SLA პასუხის<br>დრო სამუშაო საათებში</span>':
                '<span class="text-sm text-body-dark">SLA response<br>time during business hours</span>',

            # SEO Consultation card
            '<h3 class="font-heading text-xl font-bold text-heading dark:text-heading-dark mb-2">SEO კონსულტაცია</h3>':
                '<h3 class="font-heading text-xl font-bold text-heading dark:text-heading-dark mb-2">SEO Consultation</h3>',
            '<p class="text-sm text-body dark:text-body-dark leading-relaxed mb-4">1-საათიანი ექსპერტ კონსულტაცია 12 წლის გამოცდილებით. რთული პრობლემები, გუნდის აწყობა, არსებული სტრატეგიის აუდიტი.</p>':
                '<p class="text-sm text-body dark:text-body-dark leading-relaxed mb-4">1-hour expert consultation with 12+ years experience. Complex problems, team building, and audits of your existing strategy.</p>',
            '<span class="text-xs text-body-dark/60">/სთ + დღგ</span>':
                '<span class="text-xs text-body-dark/60">/hour + VAT</span>',

            # SEO Strategy card
            '<h3 class="font-heading text-xl font-bold text-heading dark:text-heading-dark mb-2">SEO სტრატეგია</h3>':
                '<h3 class="font-heading text-xl font-bold text-heading dark:text-heading-dark mb-2">SEO Strategy</h3>',
            '<p class="text-sm text-body dark:text-body-dark leading-relaxed mb-4">პროფესიონალური SEO Roadmap — სრული ანალიზი, სამოქმედო გეგმა, კონკურენტების კვლევა და ტრაფიკის პროგნოზი.</p>':
                '<p class="text-sm text-body dark:text-body-dark leading-relaxed mb-4">A professional SEO roadmap — complete analysis, action plan, competitor research, and traffic forecast.</p>',
            '<span class="text-xs text-body-dark/60">-დან</span>': '<span class="text-xs text-body-dark/60">starting at</span>',
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

    # ===== SERVICE PAGES =====
    'seo-management.html': {
        'title_ka': 'ყოველთვიური SEO მომსახურება',
        'title_en': 'Monthly SEO Management Services | 10xSEO Tbilisi, Georgia',
        'meta_ka': 'SEO მომსახურება მოიცავს სრული პასუხისმგებლობის აღებას პროცესებზე. ჩვენთან შენ მიიღებ საუკეთესო SEO სერვისს საქართველოში !',
        'meta_en': 'Done-for-you monthly SEO management. 10xSEO takes full ownership: technical SEO, content, link building, AI search optimization. Top SEO agency in Georgia.',
        'body': {},
    },
    'seo-consultation.html': {
        'title_ka': 'SEO კონსულტაცია 1:1 - პროფესიონალური მხარდაჭერა | 10XSEO',
        'title_en': 'SEO Consultation 1:1 — Expert Strategy Sessions | 10xSEO',
        'meta_ka': 'SEO კონსულტაცია 13-წლიანი გამოცდილების მქონე ექსპერტთან. მოაგვარეთ ტექნიკური გამოწვევები და მიიღეთ კონკრეტული პასუხები. დაჯავშნეთ 1:1 სესია.',
        'meta_en': 'Get 1:1 SEO consultation from a 14-year veteran. Solve technical SEO challenges, get clear answers, and a custom action plan. Book a session with 10xSEO.',
        'body': {},
    },
    'seo-strategy.html': {
        'title_ka': 'SEO სტრატეგია - შედეგზე ორიენტირებული სამოქმედო გეგმა | 10XSEO',
        'title_en': 'SEO Strategy — Results-Driven Action Plan | 10xSEO Tbilisi',
        'meta_ka': 'მიიღეთ სრული SEO სტრატეგია თქვენი პროექტისთვის: კომპლექსური ანალიზი, ბაზრის კვლევა და ოპტიმიზაციის ეტაპობრივი გეგმა.',
        'meta_en': 'Get a complete SEO strategy for your project: in-depth analysis, competitor research, market study, and step-by-step optimization roadmap from 10xSEO.',
        'body': {},
    },
    'seo-audit.html': {
        'title_ka': 'SEO აუდიტი - უფასო Loom ვიდეოანალიზი 72 საათში | 10xSEO',
        'title_en': 'Free SEO Audit — Loom Video Analysis in 72 Hours | 10xSEO',
        'meta_ka': 'უფასო SEO აუდიტი: 10-წუთიანი Loom ვიდეო, სადაც ექსპერტი პირადად განიხილავს საიტზე არსებულ ხარვეზებს, აანალიზებს კონკურენტებს და ზრდის რეალურ პოტენციალს. მიიღეთ სეო აუდიტი 72 საათში.',
        'meta_en': 'Free SEO audit: 10-minute Loom video where our expert reviews your site\'s issues, analyzes competitors, and shows real growth potential. Delivered in 72 hours.',
        'body': {},
    },
    'seo-copywriting.html': {
        'title_ka': 'SEO ქოფირაითინგი - ტექსტები, რომლებიც გაყიდვებს ზრდის | 10xSEO',
        'title_en': 'SEO Copywriting — Content That Ranks & Sells | 10xSEO',
        'meta_ka': 'SEO ქოფირაითინგი ბიზნესისთვის: მთავარი გვერდი, ბლოგები, სტატიები, პრესრელიზები. ჩვენი ტექსტების დახმარებით თქვენი ვებგვერდი Google-ის პირველ გვერდზე მოხვდება.',
        'meta_en': 'SEO copywriting for business: homepages, blogs, articles, press releases. We write content that ranks on Google\'s first page and converts visitors into customers.',
        'body': {},
    },
    'copywriting.html': {
        'title_ka': 'UI/UX ქოფირაითინგი - როცა ტექსტი მომხმარებლის ქცევას მართავს | 10xSEO',
        'title_en': 'UI/UX Copywriting — Words That Drive User Behavior | 10xSEO',
        'meta_ka': 'ნუ დაკარგავთ კლიენტებს ბუნდოვანი ინტერფეისის გამო. UI/UX ქოფირაითინგი: ვებგვერდის ტექსტები, რომლებიც ვიზიტორს მყიდველად აქცევს',
        'meta_en': 'Stop losing customers to unclear UI. 10xSEO\'s UI/UX copywriting turns visitors into buyers with words that guide every click and reduce friction.',
        'body': {},
    },
    'cro.html': {
        'title_ka': 'კონვერსიის ოპტიმიზაცია (CRO) - მეტი შედეგი არსებული რესურსით | 10XSEO',
        'title_en': 'Conversion Rate Optimization (CRO) — More Results, Same Traffic | 10xSEO',
        'meta_ka': 'CRO სერვისი: გააუმჯობესეთ კონვერსიის მაჩვენებელი მონაცემთა ანალიზითა და A/B ტესტირებით. აქციეთ ნახვები რეალურ გაყიდვებად სარეკლამო ბიუჯეტის გაზრდის გარეშე.',
        'meta_en': 'CRO services from 10xSEO: improve conversion rates with data analysis & A/B testing. Turn visits into real sales without increasing your ad spend.',
        'body': {},
    },
    'google-ads.html': {
        'title_ka': 'Google Ads მენეჯმენტი - მიზნობრივი კამპანიები რეალური შედეგისთვის | 10xSEO',
        'title_en': 'Google Ads Management — Targeted Campaigns That Convert | 10xSEO',
        'meta_ka': 'Google Ads სერვისი: გაზარდეთ გაყიდვები Google-ის მეშვეობით და მიიღეთ მაქსიმალური სარგებელი რეკლამიდან.',
        'meta_en': 'Google Ads management for Tbilisi & international brands. Maximize ROI from search ads, display, and shopping campaigns with 10xSEO\'s precision targeting.',
        'body': {},
    },
    'ra-aris-seo.html': {
        'title_ka': 'რა არის SEO ოპტიმიზაცია?',
        'title_en': 'What Is SEO? Complete Guide to Search Engine Optimization | 10xSEO',
        'meta_ka': 'SEO ოპტიმიზაცია - ანუ როგორ ვაჩვენოთ საძიებო სისტემებს რომ პირველ პოზიციაზე სწორედ ჩვენ უნდა ვიყოთ?',
        'meta_en': 'What is SEO? A complete guide to search engine optimization — how it works, why it matters, and how 10xSEO ranks Tbilisi & international brands #1 on Google.',
        'body': {},
    },
    'seo-course.html': {
        'title_ka': 'SEO ოპტიმიზაციის კურსი - 12 პრაქტიკული სესია| 10XSEO',
        'title_en': 'SEO Course — 12 Hands-On Sessions With Davit Tsilosani | 10xSEO',
        'meta_ka': 'დავით წილოსანის SEO ოპტიმიზაციის კურსი მათთვის, ვისაც პრაქტიკული ცოდნა სჭირდება. 12 ინტენსიური სესია, რეალური მაგალითები და სტაჟირების შანსი 10XSEO-ში',
        'meta_en': 'SEO course by Davit Tsilosani. 12 hands-on sessions, real-world examples, and an internship opportunity at 10xSEO. Learn SEO from Georgia\'s leading practitioner.',
        'body': {},
    },
    'roi-calculator.html': {
        'title_ka': 'SEO ROI კალკულატორი — გამოთვალე SEO ინვესტიციის ანაზღაურება | 10XSEO',
        'title_en': 'SEO ROI Calculator — Estimate Your SEO Investment Return | 10xSEO',
        'meta_ka': 'გამოთვალეთ SEO ინვესტიციის ანაზღაურება მყისიერად. უფასო ინტერაქტიული კალკულატორი — შემოსავლის პროგნოზი, break-even ვადა და უმოქმედობის ფასი.',
        'meta_en': 'Calculate your SEO ROI instantly. Free interactive calculator — revenue projection, break-even timeline, and cost-of-inaction estimate. Plan your SEO budget.',
        'body': {},
    },
    'seo-tools.html': {
        'title_ka': 'უფასო SEO ინსტრუმენტები — Pixel Width, OG Preview, Content Editor, Brief Builder | 10XSEO',
        'title_en': 'Free SEO Tools — Pixel Width, OG Preview, Content Editor & More | 10xSEO',
        'meta_ka': '6 უფასო SEO ინსტრუმენტი: Pixel Width Checker, Keyword Density, OG Preview, Readability Score, Content Editor, Brief Builder — ქართული ტექსტისთვის ოპტიმიზებული.',
        'meta_en': '7 free SEO tools by 10xSEO: Pixel Width Checker, Keyword Density, OG Preview, Readability Score, Content Editor, Brief Builder, Number-to-Words.',
        'body': {},
    },
    'portfolio.html': {
        'title_ka': 'პორტფოლიო — 10XSEO',
        'title_en': 'Portfolio — Real SEO Results from 10xSEO Clients',
        'meta_ka': '10XSEO-ს პარტნიორები და მათი რეალური შედეგები',
        'meta_en': '10xSEO\'s clients and their real SEO results — 50+ partners, 247% average traffic growth, 8x ROI. Tbilisi-based agency serving Georgian and international brands.',
        'body': {},
    },
    'vacancies.html': {
        'title_ka': 'ვაკანსიები - შემოუერთდით 10xSEO-ს გუნდს | 10XSEO',
        'title_en': 'Careers at 10xSEO — Join Georgia\'s #1 SEO Agency Team',
        'meta_ka': 'გახდი 10xSEO-ს გუნდის წევრი! იხილეთ მიმდინარე ვაკანსიები და გამოგვიგზავნეთ თქვენი CV.',
        'meta_en': 'Join 10xSEO — Georgia\'s leading SEO agency. See current openings and send us your CV. Tbilisi-based, hybrid work, growth opportunities.',
        'body': {},
    },
    'lead-form.html': {
        'title_ka': 'უფასო SEO კონსულტაცია — 10XSEO',
        'title_en': 'Free SEO Consultation — 10xSEO',
        'meta_ka': 'მოითხოვეთ უფასო SEO კონსულტაცია 10XSEO-სგან. შეავსეთ ფორმა და ჩვენი გუნდი 24 საათში დაგიკავშირდებათ.',
        'meta_en': 'Request a free SEO consultation from 10xSEO. Fill out the form and our team will contact you within 24 hours.',
        'body': {},
    },
    'case-studies.html': {
        'title_ka': 'შესრულებული პროექტები და შედეგები | 10xSEO',
        'title_en': 'Case Studies — Real SEO Results from 10xSEO Clients',
        'meta_ka': 'ნახეთ, როგორ ვაღწევთ შედეგებს: ვიზიტორთა რაოდენობის გასამმაგება, +270% ორგანული ზრდა და პირველი ადგილი ძიებაში. გაიგეთ მეტი ჩვენი გამოცდილების შესახებ.',
        'meta_en': 'See how 10xSEO delivers results: 3x traffic growth, +270% organic, #1 Google rankings. Real case studies from Tbilisi & international brands.',
        'body': {},
    },
    '404.html': {
        'title_ka': '404 — გვერდი ვერ მოიძებნა | 10xSEO',
        'title_en': '404 — Page Not Found | 10xSEO',
        'meta_ka': 'გვერდი, რომელსაც ეძებთ, არ არსებობს. დაბრუნდით მთავარ გვერდზე ან გაეცანით ჩვენს SEO სერვისებს.',
        'meta_en': 'The page you\'re looking for doesn\'t exist. Return to the homepage or browse our SEO services.',
        'body': {},
    },

    # ===== INDUSTRY PAGES =====
    'industries/construction.html': {
        'title_ka': 'გაყიდვების ახალი მასშტაბი: SEO სამშენებლო სექტორისთვის',
        'title_en': 'Construction & Real Estate SEO — Scale Your Sales | 10xSEO',
        'meta_ka': 'SEO, AI და რეკლამა დეველოპერებისთვის: ერთიანი მოდელი, რომელიც პირდაპირ თქვენი პროექტის გაყიდვების ზრდაზეა ორიენტირებული.',
        'meta_en': 'SEO, AI search & ads for property developers: a unified model focused on direct project sales growth. Specialized SEO for construction in Georgia.',
        'body': {},
    },
    'industries/healthcare.html': {
        'title_ka': 'SEO სერვისი კლინიკებისთვის | 10xSEO',
        'title_en': 'Healthcare SEO — SEO Services for Clinics & Medical Brands | 10xSEO',
        'meta_ka': 'SEO და AEO სტრატეგიები კლინიკებისთვის. გააძლიერეთ თქვენი პოზიციები Google-ის საძიებო სისტემაში | 10xSEO',
        'meta_en': 'SEO & AEO strategies for clinics. Strengthen your Google rankings, attract patients, and rank in AI search answers. Healthcare SEO experts at 10xSEO.',
        'body': {},
    },
    'industries/financial-services.html': {
        'title_ka': 'ფინანსური სექტორის SEO: ბანკები, დაზღვევა, ბუღალტერია | 10xSEO',
        'title_en': 'Financial Services SEO — Banks, Insurance, Accounting | 10xSEO',
        'meta_ka': 'როგორ მოვიზიდოთ კლიენტები ფინანსურ სექტორში? SEO ფინანსური ინსტიტუტებისთვის. მაღალი ხარისხის კონტენტი და ტექნიკური ოპტიმიზაცია',
        'meta_en': 'How do you attract clients in the financial sector? SEO for financial institutions: high-quality content + technical optimization that builds trust and rankings.',
        'body': {},
    },
    'industries/ecommerce.html': {
        'title_ka': 'E-commerce SEO სერვისები: გაზარდეთ გაყიდვები ონლაინ | 10xSEO',
        'title_en': 'E-commerce SEO Services — Grow Online Sales | 10xSEO',
        'meta_ka': 'E-commerce SEO: გაიტანეთ თქვენი პროდუქცია საერთაშორისო ბაზარზე საძიებო სისტემების დახმარებით. ონლაინმაღაზიების სრული ტექნიკური მხარდაჭერა და ორგანული ზრდის სტრატეგია',
        'meta_en': 'E-commerce SEO: take your products to international markets via search engines. Full technical support for online stores and organic growth strategy.',
        'body': {},
    },

    # ===== TOOLS PAGES =====
    'tools/seo-content-editor.html': {
        'title_ka': 'SEO Content Editor — კონტენტის ოპტიმიზაცია რეალურ დროში | 10XSEO',
        'title_en': 'SEO Content Editor — Real-Time Content Optimization | 10xSEO',
        'meta_ka': 'წერეთ SEO-ოპტიმიზებული კონტენტი რეალური დროის მეტრიკებით. Keyword density, წაკითხვადობა, სათაურები — ყველაფერი ერთ ადგილას.',
        'meta_en': 'Write SEO-optimized content with real-time metrics. Keyword density, readability, headings — everything in one place. Free tool by 10xSEO.',
        'body': {},
    },
    'tools/keyword-density.html': {
        'title_ka': 'Keyword Density Checker — საკვანძო სიტყვების სიხშირე | 10XSEO',
        'title_en': 'Keyword Density Checker — Free SEO Tool | 10xSEO',
        'meta_ka': 'გაანალიზეთ ტექსტში საკვანძო სიტყვების სიხშირე. თავიდან აიცილეთ keyword stuffing და იპოვეთ ოპტიმალური ბალანსი.',
        'meta_en': 'Analyze keyword density in your text. Avoid keyword stuffing and find the optimal balance. Free SEO tool by 10xSEO.',
        'body': {},
    },
    'tools/pixel-width-checker.html': {
        'title_ka': 'Meta Title & Description Pixel Width Checker — უფასო SEO ინსტრუმენტი | 10XSEO',
        'title_en': 'Meta Title & Description Pixel Width Checker — Free SEO Tool | 10xSEO',
        'meta_ka': 'შეამოწმეთ Meta Title და Description ზუსტი პიქსელის სიგანე — ქართული ტექსტისთვის. Google სათაურს პიქსელებით ჭრის, არა სიმბოლოებით.',
        'meta_en': 'Check the exact pixel width of your Meta Title & Description. Google truncates by pixels, not characters. Free tool — supports Latin and Georgian text.',
        'body': {},
    },
    'tools/og-preview.html': {
        'title_ka': 'Open Graph Preview — სოციალური ქსელების პრევიუ | 10XSEO',
        'title_en': 'Open Graph Preview — Social Media Preview Tool | 10xSEO',
        'meta_ka': 'ნახეთ როგორ გამოჩნდება თქვენი ბმული Facebook-ზე, Twitter-ზე და LinkedIn-ზე. დააკოპირეთ მზა OG ტეგები.',
        'meta_en': 'See how your link will appear on Facebook, Twitter, and LinkedIn. Copy ready-to-use OG tags. Free tool by 10xSEO.',
        'body': {},
    },
    'tools/readability-score.html': {
        'title_ka': 'Readability Score — ტექსტის წაკითხვადობის შემოწმება | 10XSEO',
        'title_en': 'Readability Score — Text Readability Checker | 10xSEO',
        'meta_ka': 'შეაფასეთ ტექსტის წაკითხვადობა Flesch Reading Ease სკორით. რთული წინადადებები ამცირებენ engagement-ს — გაამარტივეთ SEO კონტენტი.',
        'meta_en': 'Score your text readability with the Flesch Reading Ease metric. Hard sentences reduce engagement — simplify your SEO content. Free tool by 10xSEO.',
        'body': {},
    },
    'tools/content-brief-builder.html': {
        'title_ka': 'Content Brief Builder — კონტენტ-ბრიფის გენერატორი | 10XSEO',
        'title_en': 'Content Brief Builder — SEO Content Brief Generator | 10xSEO',
        'meta_ka': 'შექმენით სტრუქტურირებული კონტენტ-ბრიფი წამებში. სათაურის ვარიანტები, H2/H3 outline, SEO checklist — კოპირაიტერისთვის მზა დავალება.',
        'meta_en': 'Create a structured content brief in seconds. Title options, H2/H3 outline, SEO checklist — a ready-made assignment for your copywriter. Free tool.',
        'body': {},
    },
    'tools/numbers-to-words.html': {
        'title_ka': 'რიცხვები სიტყვებში — ქართული რიცხვის წერითი ფორმა | 10XSEO',
        'title_en': 'Numbers to Words — Georgian Number-to-Words Converter | 10xSEO',
        'meta_ka': 'გადაიყვანეთ რიცხვი ქართულ წერით ფორმაში. იდეალურია ხელშეკრულებების, ინვოისების და ლეგალური დოკუმენტებისთვის. ერთი ლარი, ხუთასი თეთრი — უფასოდ.',
        'meta_en': 'Convert numbers into Georgian written form. Ideal for contracts, invoices, and legal documents. One Georgian Lari, five hundred Tetri — free tool.',
        'body': {},
    },

    # ===== CASE STUDIES =====
    'case-studies/250-percent-increase.html': {
        'title_ka': 'ტრაფიკის 250%-იანი ზრდა 3 თვეში | 10XSEO',
        'title_en': '250% Traffic Growth in 3 Months — Case Study | 10xSEO',
        'meta_ka': 'ორგანული ტრაფიკი 2.5-ჯერ გაიზარდა მოკლე პერიოდში. Keyword Mapping, On-page ოპტიმიზაცია და ლინკ ბილდინგი.',
        'meta_en': 'Organic traffic grew 2.5x in a short period. Keyword mapping, on-page optimization, and link building. Real 10xSEO case study.',
        'body': {},
    },
    'case-studies/270-percent-increase.html': {
        'title_ka': 'როგორ გავზარდეთ ტრეფიკი 270%-ით, გაყიდვები 45%-ით? | 10XSEO',
        'title_en': 'How We Grew Traffic 270% & Sales 45% — Case Study | 10xSEO',
        'meta_ka': 'ამერიკულ ბაზარზე მოქმედი ტექნოლოგიური სტარტაპი Shopify-ზე. ტრაფიკი 270%-ით გაიზარდა, გაყიდვები 45%-ით.',
        'meta_en': 'A US-market tech startup on Shopify. Traffic grew 270%, sales 45%. Real 10xSEO case study with strategy breakdown.',
        'body': {},
    },
    'case-studies/3x-in-28-days.html': {
        'title_ka': 'როგორ გავზარდეთ ტრაფიკი 28 დღეში 3-ჯერ? | 10XSEO',
        'title_en': 'How We Tripled Traffic in 28 Days — Case Study | 10xSEO',
        'meta_ka': 'სრულიად ახალი პროექტი, 0-დან დაწყება. 28 დღეში ტრაფიკი 3-ჯერ გაიზარდა, 1500+ კლიკი თვეში, #1 პოზიცია.',
        'meta_en': 'Brand new project, started from zero. Traffic tripled in 28 days, 1500+ clicks per month, #1 position. Real 10xSEO case study.',
        'body': {},
    },
    'case-studies/4200-yoveltviuri-vizitori-4-tveshi.html': {
        'title_ka': '4200+ ყოველთვიური ვიზიტორი 4 თვეში | 10XSEO',
        'title_en': '4,200+ Monthly Visitors in 4 Months — Healthcare Case Study | 10xSEO',
        'meta_ka': 'სამედიცინო პროექტი, სადაც SEO საიტის გაშვებამდე დაიწყო. 4 თვეში 4200+ ყოველთვიური ვიზიტორი, +20-25% ზრდა ბოლო 28 დღეში.',
        'meta_en': 'Healthcare project where SEO started before site launch. 4,200+ monthly visitors in 4 months, +20-25% growth in the last 28 days. 10xSEO case study.',
        'body': {},
    },
    'case-studies/local-seo-result.html': {
        'title_ka': 'ზარების რაოდენობა +60% — ლოკალური SEO 2 თვეში | 10XSEO',
        'title_en': '+60% Phone Calls — Local SEO Case Study in 2 Months | 10xSEO',
        'meta_ka': 'ცნობილი ქართული ბრენდის ზარები 60%-ით გაიზარდა 2 თვეში. GMB ოპტიმიზაცია, 1500+ ზარი, +20,000 იმფრეშენი.',
        'meta_en': 'A well-known Georgian brand grew phone calls 60% in 2 months. GMB optimization, 1500+ calls, +20,000 impressions. Real 10xSEO local SEO case study.',
        'body': {},
    },
    'case-studies/seo-crisis-management.html': {
        'title_ka': 'SEO კრიზისიდან Google-ის ტოპ 3 პოზიციამდე | 10XSEO',
        'title_en': 'From SEO Crisis to Google Top 3 — Recovery Case Study | 10xSEO',
        'meta_ka': 'B2B კომპანია Google-ის პენალტიდან Top 3 პოზიციამდე 2 თვეში. URL სტრუქტურის შეცვლა, 301 Redirect, შიდა ლინკბილდინგი.',
        'meta_en': 'B2B company recovered from Google penalty to Top 3 in 2 months. URL restructure, 301 redirects, internal link building. 10xSEO crisis recovery case study.',
        'body': {},
    },
    'case-studies/seo-krizisidan-top-3mde.html': {
        'title_ka': 'SEO კრიზისიდან Google-ის ტოპ 3 პოზიციამდე — 2 თვეში | 10XSEO',
        'title_en': 'SEO Crisis to Google Top 3 — 2-Month Recovery Case Study | 10xSEO',
        'meta_ka': 'როგორ აღვადგინეთ Google-ის ჯარიმის მქონე გვერდი და მივაღწიეთ ტოპ 3 პოზიციას მხოლოდ 2 თვეში. B2B სექტორში SEO კრიზისის მართვის რეალური ქეის სტადი.',
        'meta_en': 'How we recovered a Google-penalized page and reached Top 3 in just 2 months. Real B2B SEO crisis management case study by 10xSEO.',
        'body': {},
    },
    'case-studies/stomatologiuri-klinikis-seo.html': {
        'title_ka': '#1 პოზიცია Google-ში: 1.6K ვიზიტორი და 600%-იანი ზრდა 6 თვეში — ქეის სტადი | 10XSEO',
        'title_en': '#1 on Google: 1.6K Visitors & 600% Growth in 6 Months — Dental Clinic Case Study | 10xSEO',
        'meta_ka': '#1 პოზიცია Google-ში: 1,620 ყოველთვიური ვიზიტორი (0-დან), 600%-იანი ზრდა, 63,000 იმპრესია 3 თვეში, 52% CTR იმპლანტის ფასი ქივორდზე.',
        'meta_en': '#1 on Google: 1,620 monthly visitors (from zero), 600% growth, 63,000 impressions in 3 months, 52% CTR on "implant price" keyword. Dental SEO case study.',
        'body': {},
    },
    'case-studies/trafikis-gaormageba-3-tveshi.html': {
        'title_ka': 'როგორ გავაორმაგეთ ტრაფიკი 3 თვეში? | 10XSEO',
        'title_en': 'How We Doubled Traffic in 3 Months — Construction Case Study | 10xSEO',
        'meta_ka': 'სამშენებლო სფეროში მომუშავე კომპანიის ტრაფიკი 100%-ით გაიზარდა 3 თვეში. ქივორდ მეპინგი, On-Page SEO და ბექლინკების სტრატეგია.',
        'meta_en': 'A construction company\'s traffic grew 100% in 3 months. Keyword mapping, on-page SEO, and backlink strategy. Real 10xSEO case study.',
        'body': {},
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
    # hreflang="ka" added separately by COMMON_BODY translations to avoid duplicates
    'href="seo-leqsikoni.html"': 'href="../seo-leqsikoni.html"',
    'href="startup-leqsikoni.html"': 'href="../startup-leqsikoni.html"',
    'href="ai-leqsikoni.html"': 'href="../ai-leqsikoni.html"',
    'href="blog.html"': 'href="../blog.html"',
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

    # Phase 6: Skipped-page link rewrites — depth-aware
    # KA root has href="<page>.html"; KA nested has href="../<page>.html" (sync-adjusted)
    # EN root needs href="../<page>.html" (escape /en/)
    # EN nested needs href="../../<page>.html" or more (escape /en/ + climb directories)
    page_depth = page_name.count('/')
    sl_applied = 0
    skipped_pages = ['seo-leqsikoni.html', 'startup-leqsikoni.html', 'ai-leqsikoni.html', 'blog.html']
    for skipped in skipped_pages:
        # Target prefix for EN: one ../ to escape /en/, plus page_depth more ../ for nested
        target_prefix = '../' * (page_depth + 1)
        target_href = f'href="{target_prefix}{skipped}"'
        # Match existing forms in source
        candidates = [
            f'href="{skipped}"',                    # KA root form
            f'href="../{skipped}"',                 # KA depth-1 form (already has 1 ../)
            f'href="../../{skipped}"',              # KA depth-2 form (rare)
        ]
        for old in candidates:
            if old in html and old != target_href:
                html = html.replace(old, target_href)
                sl_applied += 1
                break  # only one form should be in source

    # Phase 7: Lang switcher
    ls_applied = 0
    for old, new in LANG_SWITCHER_REPLACEMENTS.items():
        if old in html:
            html = html.replace(old, new)
            ls_applied += 1

    # Phase 8: Add hreflang="ka" to <a> tags pointing to skipped pages (any depth)
    skip_pattern = re.compile(
        r'(<a\s+href="(?:\.\./)+(?:seo-leqsikoni|startup-leqsikoni|ai-leqsikoni|blog)\.html")(?![^>]*hreflang=)',
        re.IGNORECASE
    )
    html = skip_pattern.sub(r'\1 hreflang="ka"', html)

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
