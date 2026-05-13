#!/usr/bin/env python3
"""Generate 3 Georgian legal pages by translating EN content via Gemini 2.5 Pro.

Strategy: Uses root contact-us.html (KA shell) as the structural template
(KA header, KA footer, KA mobile menu, etc.) and translates only:
  1. Head meta strings (title, description, OG, twitter, breadcrumb)
  2. JSON-LD schema name/description
  3. Main content (extracted from en/<slug>.html)

Gemini does the heavy translation; we apply post-processing for structural
metadata (lang, canonical, hreflang, og:locale, og:image filename).

Run:
    python3 /Users/imac/SEO/command-center/scripts/gen-legal-ka.py
"""
import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path('/Users/imac/SEO/command-center')
TEMPLATE = (ROOT / 'contact-us.html').read_text(encoding='utf-8')
KEY_PATH = '/Users/imac/SEO/.gemini-key'
MODEL = 'gemini-2.5-pro'
ENDPOINT = 'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}'

LAST_UPDATED_KA = 'ბოლო განახლება: 13 მაისი, 2026 · ძალაში შესვლა: 13 მაისი, 2026'
LAST_UPDATED_DATE_KA = '13 მაისი, 2026'

PAGES = ['privacy-policy', 'terms-of-service', 'cookies-policy']

# ============================================================
# GEMINI HELPERS
# ============================================================
def load_key():
    if not os.path.exists(KEY_PATH):
        sys.exit(f'ERROR: Gemini key not found at {KEY_PATH}')
    with open(KEY_PATH) as f:
        return f.read().strip()


def call_gemini(prompt, key, max_tokens=65536):
    url = ENDPOINT.format(model=MODEL, key=key)
    body = json.dumps({
        'contents': [{'parts': [{'text': prompt}]}],
        'generationConfig': {
            'temperature': 0.2,
            'maxOutputTokens': max_tokens,
            'responseMimeType': 'application/json',
        },
    }).encode('utf-8')

    req = urllib.request.Request(
        url, data=body,
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err = e.read().decode('utf-8', errors='replace')
        sys.exit(f'ERROR: Gemini HTTP {e.code}: {err[:600]}')
    except urllib.error.URLError as e:
        sys.exit(f'ERROR: Gemini network: {e.reason}')

    try:
        text = data['candidates'][0]['content']['parts'][0]['text']
    except (KeyError, IndexError):
        sys.exit(f'ERROR: Bad response: {json.dumps(data)[:600]}')

    text = text.strip()
    if text.startswith('```'):
        text = re.sub(r'^```(?:json)?\s*|\s*```$', '', text, flags=re.MULTILINE)
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        debug_path = f'/tmp/gemini_raw_{os.getpid()}.txt'
        with open(debug_path, 'w') as f:
            f.write(text)
        sys.exit(f'ERROR: JSON parse failed ({e}). Raw saved to {debug_path}')


# ============================================================
# TRANSLATION
# ============================================================
TRANSLATION_RULES = """
TRANSLATION RULES (must follow exactly):
1. Translate visible English text to professional, formal Georgian.
2. Preserve ALL HTML tags, attributes, classes, IDs, and inline styles exactly.
3. Preserve all URLs, email addresses, phone numbers, and JSON-LD structure URLs.
4. Preserve brand names: 10xSEO, Google, GA4, Calendly, Hotjar, Microsoft Clarity, GDPR, DIFC, DFSA, RERA, DHA, ADGM. Keep "10xSEO" not "10xსეო".
5. Keep "შპს 10იქსსიო.ჯი" as-is (legal entity name in Georgian).
6. SEO term: use "ქოფირაითინგი" NOT "კოპირაიტინგი" for copywriting.
7. Cookie term: use "ქუქი-ფაილი" / "ქუქი".
8. Use formal Georgian (თქვენ form), not informal (შენ).
9. Translate established legal terms accurately:
   - "Privacy Policy" → "კონფიდენციალურობის პოლიტიკა"
   - "Terms of Service" → "მომსახურების პირობები"
   - "Cookies Policy" → "ქუქი-ფაილების პოლიტიკა"
   - "Data Controller" → "მონაცემთა დამმუშავებელი"
   - "Data Processor" → "მონაცემთა მუშავი"
   - "Personal Data" → "პერსონალური მონაცემები"
   - "Consent" → "თანხმობა"
   - "Legitimate interest" → "ლეგიტიმური ინტერესი"
   - "GDPR" → "GDPR" (keep abbreviation, optionally add "(EU მონაცემთა დაცვის ზოგადი რეგულაცია)")
   - "Personal Data Protection Service of Georgia" → "საქართველოს პერსონალურ მონაცემთა დაცვის სამსახური"
   - "Last updated" → "ბოლო განახლება"
   - "Effective" → "ძალაში შესვლა"
10. Do NOT translate technical cookie names like _ga, _hjid, MUID — keep verbatim.
11. Preserve HTML entities (&amp;, &copy;) exactly.
12. For UI strings like "On this page", translate to "ამ გვერდზე".
"""


def translate_main_content(en_main, key):
    """Translate the EN <main> content to KA via Gemini."""
    prompt = f"""You are translating a legal page (privacy policy / terms / cookies) from English to Georgian for a Georgian SEO agency website (10xseo.ge).

{TRANSLATION_RULES}

INPUT (English HTML):
---
{en_main}
---

Output JSON: {{"ka_html": "<the entire translated HTML, structurally identical to input>"}}

JSON output only, no markdown fence, no commentary:"""

    result = call_gemini(prompt, key)
    if not isinstance(result, dict) or 'ka_html' not in result:
        sys.exit(f'ERROR: Unexpected translation result: {json.dumps(result)[:300]}')
    return result['ka_html']


def translate_meta(meta_strings, key):
    """Translate dict of meta strings EN→KA via single Gemini call."""
    items = '\n'.join(f'{k}: {v}' for k, v in meta_strings.items())
    prompt = f"""Translate the following short English strings to Georgian. They are meta tags (title, description, breadcrumb name, image alt) for legal pages of a Georgian SEO agency (10xseo.ge).

{TRANSLATION_RULES}

For titles, keep "| 10xSEO" suffix.
For descriptions, keep ~155 character limit, natural Georgian.

INPUT (key: english_value):
---
{items}
---

Output JSON: {{"key1": "ka_translation_1", "key2": "ka_translation_2", ...}}

JSON output only, no markdown fence:"""

    result = call_gemini(prompt, key, max_tokens=8192)
    if not isinstance(result, dict):
        sys.exit(f'ERROR: Unexpected meta translation result: {json.dumps(result)[:300]}')
    return result


# ============================================================
# HTML PROCESSING
# ============================================================
def extract_main_content(html):
    """Extract the content between <main id="main-content"> and </main>."""
    match = re.search(r'<main id="main-content">\n(.*?)\n  </main>', html, flags=re.DOTALL)
    if not match:
        sys.exit('ERROR: Could not find <main> content')
    return match.group(1)


def build_webpage_schema_ka(slug, title_ka, desc_ka):
    return f'''  <!-- Schema: WebPage -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "{title_ka.replace(' | 10xSEO', '')} — 10xSEO",
    "description": "{desc_ka}",
    "url": "https://10xseo.ge/{slug}.html",
    "inLanguage": "ka-GE",
    "isPartOf": {{
      "@type": "WebSite",
      "name": "10xSEO",
      "url": "https://10xseo.ge"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "10xSEO",
      "legalName": "შპს 10იქსსიო.ჯი",
      "url": "https://10xseo.ge",
      "email": "sales@10xseo.ge",
      "telephone": "+995510101517",
      "address": {{
        "@type": "PostalAddress",
        "streetAddress": "ბახტრიონის ქუჩა 8",
        "addressLocality": "თბილისი",
        "postalCode": "0194",
        "addressCountry": "GE"
      }}
    }}
  }}
  </script>

'''


def build_breadcrumb_schema_ka(slug, breadcrumb_ka):
    return f'''  <!-- Schema: BreadcrumbList -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type": "ListItem", "position": 1, "name": "მთავარი", "item": "https://10xseo.ge/"}},
      {{"@type": "ListItem", "position": 2, "name": "{breadcrumb_ka}", "item": "https://10xseo.ge/{slug}.html"}}
    ]
  }}
  </script>
'''


def build_ka_page(slug, title_ka, desc_ka, og_image_alt_ka, breadcrumb_ka, main_ka):
    """Compose the full KA HTML using contact-us.html (root) as shell."""
    html = TEMPLATE

    # 1. Remove ContactPage schema
    html = re.sub(
        r'  <!-- Schema: ContactPage -->\n  <script type="application/ld\+json">\n.*?\n  </script>\n\n',
        '',
        html, count=1, flags=re.DOTALL,
    )

    # 2. Remove FAQPage schema
    html = re.sub(
        r'  <!-- Schema: FAQPage -->\n  <script type="application/ld\+json">\n.*?\n  </script>\n\n',
        '',
        html, count=1, flags=re.DOTALL,
    )

    # 3. Replace BreadcrumbList with new BreadcrumbList + insert WebPage schema
    new_schemas = build_webpage_schema_ka(slug, title_ka, desc_ka) + build_breadcrumb_schema_ka(slug, breadcrumb_ka)
    html = re.sub(
        r'  <!-- Schema: BreadcrumbList -->\n  <script type="application/ld\+json">\n.*?\n  </script>',
        new_schemas.rstrip(),
        html, count=1, flags=re.DOTALL,
    )

    # 4. Head meta swaps
    page_url = f'https://10xseo.ge/{slug}.html'
    en_url = f'https://10xseo.ge/en/{slug}.html'
    og_image = f'https://10xseo.ge/images/og/page-{slug}.jpg'

    replacements = [
        (r'<title>[^<]*</title>', f'<title>{title_ka}</title>'),
        (r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc_ka}">'),
        (r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title_ka}">'),
        (r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc_ka}">'),
        (r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{page_url}">'),
        (r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{og_image}">'),
        (r'<meta property="og:image:alt" content="[^"]*">', f'<meta property="og:image:alt" content="{og_image_alt_ka}">'),
        (r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{title_ka}">'),
        (r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{desc_ka}">'),
        (r'<meta name="twitter:image" content="[^"]*">', f'<meta name="twitter:image" content="{og_image}">'),
        (r'<meta name="twitter:image:alt" content="[^"]*">', f'<meta name="twitter:image:alt" content="{og_image_alt_ka}">'),
        (r'<link rel="alternate" hreflang="ka" href="[^"]*">', f'<link rel="alternate" hreflang="ka" href="{page_url}">'),
        (r'<link rel="alternate" hreflang="en" href="[^"]*">', f'<link rel="alternate" hreflang="en" href="{en_url}">'),
        (r'<link rel="alternate" hreflang="x-default" href="[^"]*">', f'<link rel="alternate" hreflang="x-default" href="{page_url}">'),
        (r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{page_url}">'),
    ]
    for pattern, replacement in replacements:
        html = re.sub(pattern, replacement, html, count=1)

    # 5. Replace main content
    new_main = f'<main id="main-content">\n{main_ka}\n  </main>'
    html = re.sub(
        r'<main id="main-content">.*?</main>',
        lambda m: new_main,
        html, count=1, flags=re.DOTALL,
    )

    # 6. Strip the contact-form scripts block (broken JS in template)
    html = re.sub(
        r'  <!-- ========== SCRIPTS ========== -->\n  <script>\n    // Theme toggle.*?\n  </script>\n\n  <script>\n    // Mobile menu with animation',
        '  <!-- ========== SCRIPTS ========== -->\n  <script>\n    // Mobile menu with animation',
        html, count=1, flags=re.DOTALL,
    )

    return html


# ============================================================
# MAIN
# ============================================================
def main():
    key = load_key()

    # Collect meta strings from EN files for batch translation
    meta_to_translate = {}
    en_main_per_page = {}
    en_meta_per_page = {}

    for slug in PAGES:
        en_path = ROOT / 'en' / f'{slug}.html'
        if not en_path.exists():
            sys.exit(f'ERROR: {en_path} not found — run gen-legal-en.py first')

        en_html = en_path.read_text(encoding='utf-8')

        # Extract title
        m_title = re.search(r'<title>([^<]+)</title>', en_html)
        # Extract description
        m_desc = re.search(r'<meta name="description" content="([^"]+)">', en_html)
        # Extract og:image:alt
        m_alt = re.search(r'<meta property="og:image:alt" content="([^"]+)">', en_html)
        # Extract breadcrumb name (position 2)
        m_bc = re.search(r'"position": 2, "name": "([^"]+)"', en_html)

        title_en = m_title.group(1) if m_title else ''
        desc_en = m_desc.group(1) if m_desc else ''
        alt_en = m_alt.group(1) if m_alt else ''
        bc_en = m_bc.group(1) if m_bc else ''

        meta_to_translate[f'{slug}__title'] = title_en
        meta_to_translate[f'{slug}__description'] = desc_en
        meta_to_translate[f'{slug}__og_image_alt'] = alt_en
        meta_to_translate[f'{slug}__breadcrumb'] = bc_en

        en_meta_per_page[slug] = {
            'title': title_en,
            'description': desc_en,
            'og_image_alt': alt_en,
            'breadcrumb': bc_en,
        }
        en_main_per_page[slug] = extract_main_content(en_html)

    # Translate all meta strings in one Gemini call
    print(f'\n--- Translating {len(meta_to_translate)} meta strings ---')
    ka_meta = translate_meta(meta_to_translate, key)
    print(f'  Got {len(ka_meta)} translations')

    # Translate main content per page (one Gemini call each)
    for slug in PAGES:
        print(f'\n--- {slug} ---')
        print('  Translating main content...')
        en_main = en_main_per_page[slug]
        ka_main = translate_main_content(en_main, key)
        # Apply local placeholder substitutions
        ka_main = ka_main.replace('__LAST_UPDATED__', LAST_UPDATED_KA)
        ka_main = ka_main.replace('__LAST_UPDATED_DATE__', LAST_UPDATED_DATE_KA)

        # Compose KA page
        ka_html = build_ka_page(
            slug,
            title_ka=ka_meta.get(f'{slug}__title', en_meta_per_page[slug]['title']),
            desc_ka=ka_meta.get(f'{slug}__description', en_meta_per_page[slug]['description']),
            og_image_alt_ka=ka_meta.get(f'{slug}__og_image_alt', en_meta_per_page[slug]['og_image_alt']),
            breadcrumb_ka=ka_meta.get(f'{slug}__breadcrumb', en_meta_per_page[slug]['breadcrumb']),
            main_ka=ka_main,
        )

        # Sanity checks
        assert f'https://10xseo.ge/{slug}.html' in ka_html, f'canonical missing in {slug}'
        assert 'sales@10xseo.ge' in ka_html, f'NAP email missing in {slug}'
        assert 'შპს 10იქსსიო.ჯი' in ka_html, f'legal entity missing in {slug}'

        out = ROOT / f'{slug}.html'
        out.write_text(ka_html, encoding='utf-8')
        print(f'  ✓ Wrote {out} ({len(ka_html):,} bytes)')

    print('\nDone.')


if __name__ == '__main__':
    main()
