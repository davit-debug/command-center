#!/usr/bin/env python3
"""Inject hreflang tags into KA pages pointing to their EN counterparts.

For each KA page with an /en/<page>.html counterpart, ensure the head has:
- <link rel="alternate" hreflang="ka" href="<self_ka_url>">
- <link rel="alternate" hreflang="en" href="<en_url>">
- <link rel="alternate" hreflang="x-default" href="<self_ka_url>">

Also adds og:locale:alternate "en_US" if og:locale ka_GE is present.

Skipped pages (blog, dictionaries) get only self-referencing hreflang
(no en alternate, since no EN translation exists).

Usage:
  python3 scripts/inject-hreflang-ka.py --all
  python3 scripts/inject-hreflang-ka.py --page about-us.html
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://10xseo.ge"

KA_ONLY_PAGES = {'blog.html', 'seo-leqsikoni.html', 'ai-leqsikoni.html', 'startup-leqsikoni.html'}
KA_ONLY_PREFIXES = ('blog/',)

EXCLUDE_FILES = {
    'index.html',  # already has hreflang manually added
}

EXCLUDE_DIRS = {'.git', '.claude', '.github', 'audit', 'node_modules', 'scripts', 'assets', 'en', 'fonts', 'images', 'videos'}


def is_ka_only(rel_path: str) -> bool:
    if rel_path in KA_ONLY_PAGES:
        return True
    return any(rel_path.startswith(p) for p in KA_ONLY_PREFIXES)


def inject_hreflang(html: str, ka_path: str) -> tuple[str, list[str]]:
    """Inject hreflang block + og:locale:alternate into KA page head."""
    ka_url = f"{DOMAIN}/{ka_path}" if ka_path != "index.html" else f"{DOMAIN}/"
    en_url = f"{DOMAIN}/en/{ka_path}" if ka_path != "index.html" else f"{DOMAIN}/en/"

    head = html.split('</head>', 1)[0] if '</head>' in html else html
    added = []
    additions = []

    # Determine if EN counterpart exists
    has_en_counterpart = not is_ka_only(ka_path)
    en_full_path = ROOT / "en" / ka_path
    if not en_full_path.exists():
        has_en_counterpart = False

    if 'hreflang="ka"' not in head:
        if has_en_counterpart:
            additions.append(f'<link rel="alternate" hreflang="ka" href="{ka_url}">')
            additions.append(f'<link rel="alternate" hreflang="en" href="{en_url}">')
            additions.append(f'<link rel="alternate" hreflang="x-default" href="{ka_url}">')
            added.append("hreflang block (ka+en+x-default)")
        else:
            additions.append(f'<link rel="alternate" hreflang="ka" href="{ka_url}">')
            additions.append(f'<link rel="alternate" hreflang="x-default" href="{ka_url}">')
            added.append("hreflang block (ka self-only — no EN counterpart)")

    # og:locale:alternate
    if has_en_counterpart and 'og:locale:alternate' not in head:
        if 'og:locale" content="ka_GE"' in head:
            html = html.replace(
                '<meta property="og:locale" content="ka_GE">',
                '<meta property="og:locale" content="ka_GE">\n<meta property="og:locale:alternate" content="en_US">'
            )
            added.append("og:locale:alternate en_US")

    if additions:
        # Insert after </title> if present
        insertion_point = html.find('</title>')
        if insertion_point >= 0:
            insertion_point += len('</title>')
        else:
            # Fallback: after canonical or charset
            for marker in ['<link rel="canonical"', '<meta charset="UTF-8">']:
                idx = html.find(marker)
                if idx >= 0:
                    line_end = html.find('>', idx) + 1
                    insertion_point = line_end
                    break
            else:
                return html, []

        injection = '\n' + '\n'.join(additions)
        html = html[:insertion_point] + injection + html[insertion_point:]

    return html, added


def find_ka_pages():
    """Walk repo for KA HTML files."""
    pages = []
    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT)
        parts = rel.parts
        if any(p in EXCLUDE_DIRS for p in parts):
            continue
        if rel.name in EXCLUDE_FILES:
            continue
        # Skip design variant filenames (same as sync scripts)
        if '-options' in rel.name or '-v2' in rel.name or '-v1' in rel.name:
            continue
        if rel.name in ('about-final.html', 'about-final-v2.html', 'about-variants.html',
                        'about-new.html', 'about-preview.html', 'why-10xseo.html'):
            continue
        pages.append(rel)
    return sorted(pages)


def process_file(rel_path: Path, dry_run: bool = False):
    full = ROOT / rel_path
    print(f"=== {rel_path} ===")
    html = full.read_text(encoding="utf-8-sig")
    new_html, added = inject_hreflang(html, str(rel_path))

    if not added:
        print(f"  ✓ Already has hreflang")
        return

    print(f"  Added: {', '.join(added)}")
    if dry_run:
        print(f"  DRY-RUN")
        return
    full.write_text(new_html, encoding="utf-8")
    print(f"  ✓ Wrote")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--page", help="KA page rel path")
    p.add_argument("--all", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    if args.all:
        pages = find_ka_pages()
        print(f"Processing {len(pages)} KA pages...")
        for page in pages:
            process_file(page, dry_run=args.dry_run)
    elif args.page:
        process_file(Path(args.page), dry_run=args.dry_run)
    else:
        sys.exit("Specify --page or --all")


if __name__ == "__main__":
    sys.exit(main())
