#!/usr/bin/env python3
"""Polish Georgian legal pages — second-pass Gemini rewrite for naturalness.

Goals:
1. Simplify company naming — use only "შპს 10იქსსიო.ჯი"; drop "LLC 10ixsio.ge",
   parenthetical "(„10xSEO", „ჩვენ")", "(LLC 10ixsio.ge)". Use "ჩვენ" naturally
   as a pronoun without upfront definition.
2. Improve Georgian flow — fix calques, awkward word order, run-on sentences.
3. Cut redundant phrases ("ჩვენი ვებსაიტზე არსებული", "შემდეგ" overuse).
4. Preserve all HTML structure (tags, classes, attributes, IDs, hrefs).
5. Keep brand names verbatim: Google, GA4, Calendly, Hotjar, Microsoft Clarity,
   GDPR, DIFC, DFSA, RERA, DHA, ADGM, 10xSEO (when used standalone, e.g., in
   email subject or postal address).

Run:
    python3 /Users/imac/SEO/command-center/scripts/polish-legal-ka.py
"""
import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path('/Users/imac/SEO/command-center')
KEY_PATH = '/Users/imac/SEO/.gemini-key'
MODEL = 'gemini-2.5-pro'
ENDPOINT = 'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}'

PAGES = ['privacy-policy', 'terms-of-service', 'cookies-policy']


def load_key():
    if not os.path.exists(KEY_PATH):
        sys.exit(f'ERROR: Gemini key not found at {KEY_PATH}')
    with open(KEY_PATH) as f:
        return f.read().strip()


def call_gemini(prompt, key, max_tokens=65536, model=None, max_retries=4):
    import time
    chosen_model = model or MODEL
    url = ENDPOINT.format(model=chosen_model, key=key)
    body = json.dumps({
        'contents': [{'parts': [{'text': prompt}]}],
        'generationConfig': {
            'temperature': 0.3,
            'maxOutputTokens': max_tokens,
            'responseMimeType': 'application/json',
        },
    }).encode('utf-8')

    last_err = None
    for attempt in range(max_retries):
        req = urllib.request.Request(
            url, data=body,
            headers={'Content-Type': 'application/json'},
            method='POST',
        )
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                data = json.loads(resp.read())
            break
        except urllib.error.HTTPError as e:
            err = e.read().decode('utf-8', errors='replace')
            last_err = f'HTTP {e.code}: {err[:300]}'
            if e.code in (429, 500, 502, 503, 504):
                wait = 5 * (2 ** attempt)
                print(f'  retry {attempt+1}/{max_retries} after {wait}s ({e.code})')
                time.sleep(wait)
                continue
            sys.exit(f'ERROR: Gemini HTTP {e.code}: {err[:800]}')
        except urllib.error.URLError as e:
            last_err = f'network: {e.reason}'
            time.sleep(5 * (2 ** attempt))
            continue
    else:
        # all retries failed — try fallback model if not already
        if chosen_model != 'gemini-2.5-flash':
            print(f'  Falling back to gemini-2.5-flash after retries')
            return call_gemini(prompt, key, max_tokens, model='gemini-2.5-flash', max_retries=2)
        sys.exit(f'ERROR: Gemini retries exhausted. Last error: {last_err}')

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
        debug_path = f'/tmp/gemini_polish_raw_{os.getpid()}.txt'
        with open(debug_path, 'w') as f:
            f.write(text)
        sys.exit(f'ERROR: JSON parse failed ({e}). Raw saved to {debug_path}')


POLISH_RULES = """
POLISH RULES (must follow exactly):

A. Company naming — STRICT:
   - Use ONLY "შპს 10იქსსიო.ჯი" as the legal company name.
   - REMOVE all instances of: "LLC 10ixsio.ge", "(LLC 10ixsio.ge)", "(LLC \\"10ixsio.ge\\")",
     "სავაჭრო სახელი „10xSEO\"", "(იურიდიული პირი საქართველოში: ...)".
   - REMOVE parenthetical introductions of pronouns like "(შემდგომში „10xSEO\", „ჩვენ\")"
     or "(„ჩვენ\", „ჩვენი\")".
   - Use "ჩვენ" as a natural pronoun without defining it upfront — that's standard Georgian.
   - "10xSEO" as a brand name can appear in: (a) the company-name strong tag standalone,
     (b) postal addresses, (c) email subject suggestions. NOT in pronoun definitions.

B. Georgian naturalness:
   - Subject-verb-object order: prefer subject right next to verb (avoid "თუ როგორ X-ი Y" → "თუ როგორ Y-ს აკეთებს X").
   - Cut filler: "ჩვენი ვებსაიტზე არსებული" → "ჩვენი ვებსაიტის"; "შემდეგ ავტომატურად" → "ავტომატურად".
   - Fix calques: "ერთობლივი მუშაობის ანალიზი" (joint work analysis) → "აგრეგირებული ანალიზი" or "ჯამური მონაცემების ანალიზი" for "aggregate analysis".
   - "user agent" → keep verbatim or use "მომხმარებლის აგენტი (user agent)".
   - "გადახედვა" (in security context) → "შემოწმება" or "შეფასება".
   - Avoid "შემდეგ" repetition; use "სრულდება" / "უქმდება" / "იშლება" where appropriate.
   - "ხელთ არსებულ" → "ჩვენთან არსებულ" or "ჩვენთან დაცულ".

C. HTML — STRICT, MUST PRESERVE:
   - All HTML tags exactly: <p>, <h2>, <ul>, <ol>, <li>, <strong>, <a>, <table>, <thead>, <tbody>, <tr>, <th>, <td>, <em>, <nav>, <div>, <article>, <section>, <br>, <span>.
   - All class attributes exactly (e.g., class="text-base text-body...").
   - All id attributes exactly (e.g., id="controller").
   - All href values exactly.
   - HTML entities exactly (&amp;, &copy;).
   - Brand-name strings inside HTML: 10xSEO, Google, GA4, Calendly, Hotjar, Microsoft Clarity, GDPR, DIFC, DFSA, RERA, DHA, ADGM, EEA, UK, USA, SCCs, PDPL, TLS 1.3.
   - GDPR Article cites in Latin letters: (a), (b), (c), (f), Art. 15-22, Art. 46, Art. 77.
   - Cookie names verbatim: _ga, _ga_<ID>, _hjid, _hjSession*, MUID, _clck, _clsk, __cf_bm.

D. Formality: formal თქვენ register throughout (no შენ).

E. UAE references — use "UAE" as a parenthetical reference after "არაბთა გაერთიანებული საამიროები" on FIRST mention only; thereafter just "UAE" is fine for brevity.
"""


def polish_main(slug, en_main_html, ka_main_html, key):
    """Send KA main content to Gemini for naturalness rewrite."""
    prompt = f"""You are polishing the Georgian translation of a legal page (10xSEO website, slug: {slug}). The translation is already accurate but reads awkwardly in places — too many company-name designations, calques from English, and filler.

{POLISH_RULES}

EN ORIGINAL (for reference — do NOT translate from this; you're polishing the KA below):
---
{en_main_html}
---

KA TO POLISH (rewrite for naturalness):
---
{ka_main_html}
---

Output JSON: {{"ka_polished": "<entire polished KA HTML, structurally identical>"}}

JSON only, no markdown fence, no commentary:"""

    result = call_gemini(prompt, key)
    if not isinstance(result, dict) or 'ka_polished' not in result:
        sys.exit(f'ERROR: Unexpected polish result: {json.dumps(result)[:400]}')
    return result['ka_polished']


def extract_main(html):
    m = re.search(r'<main id="main-content">\n(.*?)\n  </main>', html, flags=re.DOTALL)
    if not m:
        sys.exit('ERROR: Could not find <main> in HTML')
    return m.group(1)


def replace_main(html, new_main):
    new_block = f'<main id="main-content">\n{new_main}\n  </main>'
    return re.sub(
        r'<main id="main-content">.*?</main>',
        lambda m: new_block,
        html, count=1, flags=re.DOTALL,
    )


def main():
    key = load_key()

    for slug in PAGES:
        en_path = ROOT / 'en' / f'{slug}.html'
        ka_path = ROOT / f'{slug}.html'

        if not en_path.exists() or not ka_path.exists():
            print(f'SKIP {slug}: missing file')
            continue

        en_html = en_path.read_text(encoding='utf-8')
        ka_html = ka_path.read_text(encoding='utf-8')

        en_main = extract_main(en_html)
        ka_main = extract_main(ka_html)

        print(f'\n=== {slug} ===')
        print(f'  KA main: {len(ka_main):,} chars')

        polished = polish_main(slug, en_main, ka_main, key)
        print(f'  Polished: {len(polished):,} chars')

        # Sanity check: must contain key markers
        assert '<main' not in polished, f'Polished content should not contain <main> wrapper'
        # 10xSEO can still appear (in postal address, email subject)
        # But "LLC 10ixsio.ge" and "(„10xSEO", „ჩვენ")" should NOT
        if 'LLC 10ixsio.ge' in polished:
            print(f'  WARN: "LLC 10ixsio.ge" still present in polished {slug}')

        new_html = replace_main(ka_html, polished)
        ka_path.write_text(new_html, encoding='utf-8')
        print(f'  ✓ Wrote {ka_path} ({len(new_html):,} bytes)')

    print('\nDone.')


if __name__ == '__main__':
    main()
