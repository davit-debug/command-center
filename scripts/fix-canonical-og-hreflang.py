#!/usr/bin/env python3
"""Inject missing canonical, hreflang, and OG meta tags on production pages.

Targets pages flagged by audit Stage 6, 7, 8. Idempotent.

Usage:
  python3 scripts/fix-canonical-og-hreflang.py --dry-run
  python3 scripts/fix-canonical-og-hreflang.py --apply
"""
import argparse
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIT = ROOT / "audit" / "prelaunch-2026-05-12"
DOMAIN = "https://10xseo.ge"

KA_ONLY_PAGES = {"blog.html", "seo-leqsikoni.html", "ai-leqsikoni.html", "startup-leqsikoni.html"}
KA_ONLY_PREFIXES = ("blog/",)
EN_ONLY = {"en/blog/what-is-aeo.html", "en/blog/aeo-optimization-agency-dubai.html"}


def is_ka_only(rel: str) -> bool:
    if rel in KA_ONLY_PAGES:
        return True
    return any(rel.startswith(p) for p in KA_ONLY_PREFIXES)


def page_urls(rel: str) -> tuple[str, str]:
    """Return (ka_url, en_url) for a relative page path."""
    if rel.startswith("en/"):
        ka_path = rel[3:]
    else:
        ka_path = rel
    if ka_path == "index.html":
        ka_url = f"{DOMAIN}/"
        en_url = f"{DOMAIN}/en/"
    else:
        ka_url = f"{DOMAIN}/{ka_path}"
        en_url = f"{DOMAIN}/en/{ka_path}"
    return ka_url, en_url


def inject_canonical_hreflang(html: str, rel: str) -> tuple[str, list[str]]:
    """Inject canonical + hreflang block if missing."""
    is_en = rel.startswith("en/")
    ka_url, en_url = page_urls(rel)
    self_url = en_url if is_en else ka_url

    head_section = html.split("</head>", 1)[0] if "</head>" in html else html
    additions: list[str] = []
    added: list[str] = []

    # Canonical
    if "<link rel=\"canonical\"" not in head_section and "<link rel='canonical'" not in head_section:
        additions.append(f'<link rel="canonical" href="{self_url}">')
        added.append("canonical")

    # hreflang block (if not already present, and page has bilingual counterpart)
    has_hreflang = 'rel="alternate"' in head_section and "hreflang=" in head_section
    if not has_hreflang:
        if is_en and rel in EN_ONLY:
            # en-only blog post — only self-ref
            additions.append(f'<link rel="alternate" hreflang="en" href="{en_url}">')
            additions.append(f'<link rel="alternate" hreflang="x-default" href="{en_url}">')
            added.append("hreflang (en-only)")
        elif not is_en and is_ka_only(rel):
            # ka-only page — only self-ref
            additions.append(f'<link rel="alternate" hreflang="ka" href="{ka_url}">')
            additions.append(f'<link rel="alternate" hreflang="x-default" href="{ka_url}">')
            added.append("hreflang (ka-only)")
        else:
            additions.append(f'<link rel="alternate" hreflang="ka" href="{ka_url}">')
            additions.append(f'<link rel="alternate" hreflang="en" href="{en_url}">')
            additions.append(f'<link rel="alternate" hreflang="x-default" href="{ka_url}">')
            added.append("hreflang (bilingual)")

    if additions:
        # Insert after </title>
        idx = html.find("</title>")
        if idx >= 0:
            idx += len("</title>")
            html = html[:idx] + "\n" + "\n".join(additions) + html[idx:]
        else:
            # Fallback: insert before </head>
            html = html.replace("</head>", "\n".join(additions) + "\n</head>", 1)
    return html, added


def get_title(html: str) -> str:
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    return m.group(1).strip() if m else ""


def get_meta_description(html: str) -> str:
    m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html, re.IGNORECASE)
    return m.group(1) if m else ""


def detect_og_image(html: str, rel: str) -> str:
    """Return existing og:image URL or build a sensible default."""
    m = re.search(r'<meta\s+property="og:image"\s+content="([^"]*)"', html, re.IGNORECASE)
    if m:
        return m.group(1)
    # default fallback
    if rel.startswith("en/"):
        return f"{DOMAIN}/images/og-default-en.jpg"
    return f"{DOMAIN}/images/og-default.jpg"


def inject_og(html: str, rel: str) -> tuple[str, list[str]]:
    """Inject missing OG fields."""
    is_en = rel.startswith("en/")
    ka_url, en_url = page_urls(rel)
    self_url = en_url if is_en else ka_url

    head_section = html.split("</head>", 1)[0] if "</head>" in html else html
    additions: list[str] = []
    added: list[str] = []

    title = get_title(html).replace('"', "&quot;")
    desc = get_meta_description(html).replace('"', "&quot;")

    # Determine which fields are missing
    required = {
        "og:title": ("title", f'<meta property="og:title" content="{title}">'),
        "og:description": ("description", f'<meta property="og:description" content="{desc}">'),
        "og:url": ("url", f'<meta property="og:url" content="{self_url}">'),
        "og:type": ("type", '<meta property="og:type" content="website">'),
        "og:locale": ("locale", f'<meta property="og:locale" content="{"en_US" if is_en else "ka_GE"}">'),
        "og:site_name": ("site_name", '<meta property="og:site_name" content="10xSEO">'),
    }
    for prop, (label, tag) in required.items():
        if f'property="{prop}"' not in head_section:
            additions.append(tag)
            added.append(f"og:{label}")

    # og:image — only inject if absent (don't override user-set image)
    if 'property="og:image"' not in head_section:
        img = detect_og_image(html, rel)
        additions.append(f'<meta property="og:image" content="{img}">')
        added.append("og:image (fallback)")

    # og:locale:alternate
    if "og:locale:alternate" not in head_section and not (is_en and rel in EN_ONLY) and not (not is_en and is_ka_only(rel)):
        alt_locale = "ka_GE" if is_en else "en_US"
        additions.append(f'<meta property="og:locale:alternate" content="{alt_locale}">')
        added.append("og:locale:alternate")

    # Twitter Cards (if missing)
    if "twitter:card" not in head_section:
        additions.append('<meta name="twitter:card" content="summary_large_image">')
        added.append("twitter:card")
    if "twitter:title" not in head_section:
        additions.append(f'<meta name="twitter:title" content="{title}">')
        added.append("twitter:title")
    if "twitter:description" not in head_section and desc:
        additions.append(f'<meta name="twitter:description" content="{desc}">')
        added.append("twitter:description")
    if "twitter:image" not in head_section:
        img = detect_og_image(html, rel)
        additions.append(f'<meta name="twitter:image" content="{img}">')
        added.append("twitter:image")

    if additions:
        idx = html.find("</title>")
        if idx >= 0:
            idx += len("</title>")
            html = html[:idx] + "\n" + "\n".join(additions) + html[idx:]
        else:
            html = html.replace("</head>", "\n".join(additions) + "\n</head>", 1)

    return html, added


def load_targets() -> list[str]:
    """Load production pages flagged for canonical or OG fixes."""
    targets: set[str] = set()
    with (AUDIT / "06_canonical.csv").open() as f:
        for r in csv.DictReader(f):
            if r["has_canonical"] == "no":
                targets.add(r["path"])
    with (AUDIT / "07_og_twitter.csv").open() as f:
        for r in csv.DictReader(f):
            if r["og_complete"] == "no" or r["tw_complete"] == "no":
                targets.add(r["path"])
    with (AUDIT / "08_hreflang.csv").open() as f:
        for r in csv.DictReader(f):
            if r["hl_ka"] == "no":
                targets.add(r["path"])

    # exclude test/variant files
    skip_prefixes = ("og-", "cta-picker", "menu-rename")
    targets = {t for t in targets if not Path(t).name.startswith(skip_prefixes)}
    return sorted(targets)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--apply", action="store_true")
    p.add_argument("--only-canonical", action="store_true", help="Skip OG injection")
    args = p.parse_args()
    if not (args.dry_run or args.apply):
        sys.exit("Specify --dry-run or --apply")

    targets = load_targets()
    print(f"Found {len(targets)} pages with missing canonical/OG/hreflang")
    print()

    total_added = 0
    pages_modified = 0
    for rel in targets:
        path = ROOT / rel
        if not path.exists():
            print(f"  ✗ MISSING: {rel}")
            continue
        html = path.read_text(encoding="utf-8")
        original = html
        html, added1 = inject_canonical_hreflang(html, rel)
        if args.only_canonical:
            added2 = []
        else:
            html, added2 = inject_og(html, rel)
        added = added1 + added2
        if added:
            print(f"  ✓ {rel}: {', '.join(added)}")
            total_added += len(added)
            pages_modified += 1
            if args.apply:
                path.write_text(html, encoding="utf-8")
        else:
            print(f"  - {rel}: nothing to add")

    print()
    print(f"Pages modified: {pages_modified} / {len(targets)}")
    print(f"Total tags added: {total_added}")
    if args.dry_run:
        print("(DRY RUN — no files written)")


if __name__ == "__main__":
    main()
