#!/usr/bin/env python3
"""Inject missing canonical, hreflang, og:locale, og:url tags into /en/ pages.

Many KA source pages lack these tags, so the structural transforms in
translate-all.py never had targets to find/replace. This script adds
the tags directly to /en/<page>.html files (idempotent).

Usage:
  python3 scripts/inject-seo-meta.py --all
  python3 scripts/inject-seo-meta.py --page about-us.html
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://10xseo.ge"

KA_ONLY_PAGES = {'blog.html', 'seo-leqsikoni.html', 'ai-leqsikoni.html', 'startup-leqsikoni.html'}
KA_ONLY_PREFIXES = ('blog/',)


def page_urls(page_name: str):
    """Return (ka_url, en_url) for a page name (relative path)."""
    ka_url = f"{DOMAIN}/{page_name}" if page_name != "index.html" else f"{DOMAIN}/"
    en_url = f"{DOMAIN}/en/{page_name}" if page_name != "en/index.html" else f"{DOMAIN}/en/"
    return ka_url, en_url


def inject_meta(html: str, page_name: str) -> tuple[str, list[str]]:
    """Idempotently inject missing canonical, hreflang, og:locale, og:url.
    Returns (new_html, list of added tag descriptions).
    """
    # /en/ page name (without 'en/' prefix for EN URL building)
    if page_name.startswith("en/"):
        ka_path = page_name[3:]
    else:
        ka_path = page_name

    ka_url = f"{DOMAIN}/{ka_path}" if ka_path != "index.html" else f"{DOMAIN}/"
    en_url = f"{DOMAIN}/en/{ka_path}" if ka_path != "index.html" else f"{DOMAIN}/en/"

    head_section = html.split('</head>', 1)[0] if '</head>' in html else html

    additions = []
    added = []

    # Update existing canonical to /en/ URL
    # Handle both .html and clean URL (with trailing slash) variants
    canonical_en = f'<link rel="canonical" href="{en_url}">'
    # Possible KA canonical variants for this page
    ka_clean = ka_url.rstrip('.html')  # e.g. https://10xseo.ge/ai-seo (without .html)
    if ka_url.endswith('.html'):
        ka_clean_with_slash = ka_url[:-5] + '/'  # e.g. .../ai-seo/
    else:
        ka_clean_with_slash = ka_url

    canonical_variants = [
        f'<link rel="canonical" href="{ka_url}">',                # full path with .html
        f'<link rel="canonical" href="{ka_clean_with_slash}">',  # clean URL with /
    ]

    canonical_replaced = False
    for v in canonical_variants:
        if v in html and canonical_en not in html:
            html = html.replace(v, canonical_en)
            added.append("canonical (updated)")
            canonical_replaced = True
            break

    if not canonical_replaced and '<link rel="canonical"' not in head_section:
        additions.append(canonical_en)
        added.append("canonical")

    if 'hreflang="en"' not in head_section:
        additions.append(f'<link rel="alternate" hreflang="ka" href="{ka_url}">')
        additions.append(f'<link rel="alternate" hreflang="en" href="{en_url}">')
        additions.append(f'<link rel="alternate" hreflang="x-default" href="{ka_url}">')
        added.append("hreflang block")

    if 'og:locale" content="en_US"' not in head_section:
        if 'og:locale" content="ka_GE"' in head_section:
            html = html.replace(
                '<meta property="og:locale" content="ka_GE">',
                '<meta property="og:locale" content="en_US">\n<meta property="og:locale:alternate" content="ka_GE">'
            )
            added.append("og:locale (replaced)")
        else:
            additions.append('<meta property="og:locale" content="en_US">')
            added.append("og:locale")

    # Update existing og:url to /en/ if it points to KA
    og_url_ka = f'<meta property="og:url" content="{ka_url}">'
    og_url_en = f'<meta property="og:url" content="{en_url}">'
    if og_url_ka in html and og_url_en not in html:
        html = html.replace(og_url_ka, og_url_en)
        added.append("og:url (updated KA→EN)")
    elif 'og:url' not in head_section:
        additions.append(og_url_en)
        added.append("og:url")

    if additions:
        # Insert after <title> closing tag
        insertion_point = html.find('</title>')
        if insertion_point >= 0:
            insertion_point += len('</title>')
            injection = '\n' + '\n'.join(additions)
            html = html[:insertion_point] + injection + html[insertion_point:]
        else:
            print(f"  WARN: no </title> found, can't inject", file=sys.stderr)

    return html, added


def process_file(en_path: Path, dry_run: bool = False):
    """Process a single /en/<page>.html file."""
    rel = en_path.relative_to(ROOT / "en")
    print(f"=== en/{rel} ===")
    html = en_path.read_text(encoding="utf-8-sig")
    new_html, added = inject_meta(html, str(rel))

    if not added:
        print(f"  ✓ All meta already present")
        return

    print(f"  Added: {', '.join(added)}")
    if dry_run:
        print(f"  DRY-RUN — no file written")
        return
    en_path.write_text(new_html, encoding="utf-8")
    print(f"  ✓ Wrote")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--page", help="Page rel path under /en/")
    p.add_argument("--all", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    if args.all:
        en_root = ROOT / "en"
        for f in sorted(en_root.rglob("*.html")):
            process_file(f, dry_run=args.dry_run)
    elif args.page:
        process_file(ROOT / "en" / args.page, dry_run=args.dry_run)
    else:
        sys.exit("Specify --page or --all")


if __name__ == "__main__":
    sys.exit(main())
