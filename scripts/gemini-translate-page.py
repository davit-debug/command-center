#!/usr/bin/env python3
"""Gemini-based bulk translator for /en/ pages.

Extracts unique Georgian phrases from a /en/<page>.html file (after
structural translation by translate-all.py), batch-translates them
via Gemini API, and applies the translations as str.replace operations
on the HTML.

Usage:
  python3 scripts/gemini-translate-page.py --page services.html
  python3 scripts/gemini-translate-page.py --page services.html --dry-run
  python3 scripts/gemini-translate-page.py --all
"""
import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEY_PATH = "/Users/imac/SEO/.gemini-key"
MODEL = "gemini-2.5-pro"
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"

KA_RE = re.compile(r'[Ⴀ-ჿ]')


def load_key():
    if not os.path.exists(KEY_PATH):
        sys.exit(f"ERROR: Gemini key not found at {KEY_PATH}")
    with open(KEY_PATH) as f:
        return f.read().strip()


def extract_unique_ka_phrases(html_path):
    """Extract unique lines containing Georgian text from HTML.
    Strips data-ka attribute values (we keep those as-is)."""
    with open(html_path, encoding="utf-8") as f:
        content = f.read()

    seen = set()
    phrases = []
    for line in content.split("\n"):
        # Strip data-ka attribute values to avoid translating attribute KA references
        stripped = re.sub(r'data-ka="[^"]*"', "", line)
        if not KA_RE.search(stripped):
            continue
        # Skip lines that are just JSON-LD service URLs or breadcrumb URLs
        # We'll handle schema separately. Focus on visible-text lines.
        line_norm = line.strip()
        if line_norm in seen:
            continue
        seen.add(line_norm)
        # Don't skip long lines — Gemini can handle JSON-LD and FAQ Q&A blocks
        if len(line) > 6000:  # only skip extreme cases (whole-file minified CSS)
            continue
        phrases.append(line.rstrip())
    return phrases


def build_prompt(phrases):
    """Build Gemini prompt for batch translation."""
    numbered = "\n".join(f"{i+1}. {p}" for i, p in enumerate(phrases))
    return f"""You are translating SEO copy for a Georgian SEO agency's English website (10xseo.ge/en/). The agency targets Tbilisi-based businesses AND international clients.

Translate the following Georgian text snippets to English, preserving:
- All HTML tags, classes, IDs, and attributes EXACTLY as-is
- JSON-LD structure if present
- HTML entities (&amp;, &copy;, etc.)
- Numbers, brand names (Google, ChatGPT, 10xSEO), and English words already present
- The hreflang="ka" attribute on links to Georgian-only pages
- All visible Georgian text translated to natural, professional English

For each numbered line below, output the English translation maintaining the EXACT same HTML structure. Use professional SEO industry English with clear, conversion-focused tone. Target audience: business owners and marketing managers.

Output JSON: {{"translations": [{{"id": 1, "ka": "<original>", "en": "<english>"}}, ...]}}

INPUT (numbered lines):
---
{numbered}
---

Output JSON only, no commentary, no markdown fence:"""


def call_gemini(prompt, key):
    url = ENDPOINT.format(model=MODEL, key=key)
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 65536,
            "responseMimeType": "application/json",
        },
    }).encode("utf-8")

    req = urllib.request.Request(
        url, data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        sys.exit(f"ERROR: Gemini HTTP {e.code}: {err[:500]}")
    except urllib.error.URLError as e:
        sys.exit(f"ERROR: Gemini network: {e.reason}")

    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        sys.exit(f"ERROR: Bad response: {json.dumps(data)[:500]}")

    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.MULTILINE)
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        # Save raw for debugging
        debug_path = f"/tmp/gemini_raw_{os.getpid()}.txt"
        with open(debug_path, "w") as f:
            f.write(text)
        sys.exit(f"ERROR: JSON parse failed ({e}). Raw saved to {debug_path}")


def apply_translations(html_path, translations, dry_run=False):
    """Apply ka→en str.replace operations on the HTML file."""
    with open(html_path, encoding="utf-8") as f:
        html = f.read()

    applied = 0
    not_found = 0
    for entry in translations:
        ka = entry.get("ka", "").rstrip()
        en = entry.get("en", "").rstrip()
        if not ka or not en or ka == en:
            continue
        if ka in html:
            html = html.replace(ka, en)
            applied += 1
        else:
            not_found += 1

    print(f"  Applied: {applied}/{len(translations)} translations")
    print(f"  Not found in HTML: {not_found}")

    # Sanity check: Georgian text remaining
    remaining = sum(1 for line in html.split("\n")
                    if KA_RE.search(re.sub(r'data-ka="[^"]*"', "", line)))
    print(f"  Leftover Georgian lines: {remaining}")

    if dry_run:
        print(f"  DRY-RUN — no file written")
        return

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✓ Wrote {html_path}")


def translate_page(page_rel_path, dry_run=False, batch_size=50):
    """Process a single /en/ page."""
    html_path = ROOT / "en" / page_rel_path
    if not html_path.exists():
        print(f"SKIP: {html_path} not found")
        return False

    print(f"\n=== {page_rel_path} ===")
    phrases = extract_unique_ka_phrases(html_path)
    if not phrases:
        print(f"  No Georgian phrases found — skipping")
        return True
    print(f"  Extracted {len(phrases)} unique Georgian phrases")

    key = load_key()
    all_translations = []

    # Batch into groups to stay within token limits
    for batch_start in range(0, len(phrases), batch_size):
        batch = phrases[batch_start:batch_start + batch_size]
        print(f"  Batch {batch_start//batch_size + 1}: {len(batch)} phrases")
        prompt = build_prompt(batch)
        result = call_gemini(prompt, key)
        if isinstance(result, dict) and "translations" in result:
            all_translations.extend(result["translations"])
        else:
            print(f"  WARNING: unexpected result shape for batch")
            print(f"  Result preview: {json.dumps(result)[:200]}")

    print(f"  Got {len(all_translations)} translations from Gemini")

    if all_translations:
        apply_translations(html_path, all_translations, dry_run=dry_run)
    return True


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--page", help="Page relative path (e.g. services.html)")
    p.add_argument("--all", action="store_true", help="Translate all /en/ pages with Georgian leftover")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--batch-size", type=int, default=50, help="Phrases per Gemini call")
    args = p.parse_args()

    if args.all:
        # Walk /en/ tree
        en_root = ROOT / "en"
        pages = sorted([p.relative_to(en_root) for p in en_root.rglob("*.html")])
        for page in pages:
            try:
                translate_page(str(page), dry_run=args.dry_run, batch_size=args.batch_size)
            except SystemExit as e:
                print(f"  ERROR on {page}: {e}")
                continue
    elif args.page:
        translate_page(args.page, dry_run=args.dry_run, batch_size=args.batch_size)
    else:
        sys.exit("Specify --page <path> or --all")

    return 0


if __name__ == "__main__":
    sys.exit(main())
