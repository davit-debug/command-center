#!/usr/bin/env python3
"""Normalize canonical href format across the site.

KA root pages use clean URLs (/page-slug/). My fix script added .html
canonicals on 4 root pages. Update them to match the site convention.

Also normalize:
  - og:url on en pages: should be /en/page.html, not KA /page/
  - hreflang ka href on en pages: should be /page/ (clean) to match site

Rules:
  - KA root page like 'about-us.html' → canonical 'https://10xseo.ge/about-us/'
  - EN page like 'en/about-us.html' → canonical 'https://10xseo.ge/en/about-us.html'
  - Subdir pages (blog/, case-studies/, tools/) → keep .html (no convention yet)
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://10xseo.ge"

# Root-level KA pages where I added canonical with .html (need to switch to /)
KA_ROOT_FIXES = [
    ("about-us.html", "https://10xseo.ge/about-us.html", "https://10xseo.ge/about-us/"),
    ("case-studies.html", "https://10xseo.ge/case-studies.html", "https://10xseo.ge/case-studies/"),
    ("portfolio.html", "https://10xseo.ge/portfolio.html", "https://10xseo.ge/portfolio/"),
    ("vacancies.html", "https://10xseo.ge/vacancies.html", "https://10xseo.ge/vacancies/"),
]


def fix_root_canonicals():
    """Update my new .html canonicals to /page/ format on 4 root pages."""
    for rel, old_url, new_url in KA_ROOT_FIXES:
        path = ROOT / rel
        if not path.exists():
            print(f"  ✗ {rel}: missing")
            continue
        html = path.read_text(encoding="utf-8")
        # Update both canonical and og:url, twitter:image etc. that reference the .html
        old_canon = f'<link rel="canonical" href="{old_url}">'
        new_canon = f'<link rel="canonical" href="{new_url}">'
        old_og = f'content="{old_url}"'
        new_og = f'content="{new_url}"'
        n_canon = html.count(old_canon)
        n_og = html.count(old_og)
        html = html.replace(old_canon, new_canon)
        html = html.replace(old_og, new_og)
        if n_canon or n_og:
            path.write_text(html, encoding="utf-8")
            print(f"  ✓ {rel}: canonical={n_canon}, og:url={n_og} → /page/ format")


def fix_en_og_url():
    """EN pages should have og:url pointing to /en/ URL, not KA URL.
    Many existing EN pages have og:url='/page/' (KA URL).
    """
    en_root = ROOT / "en"
    fixed = 0
    OG_URL_RE = re.compile(r'<meta\s+property="og:url"\s+content="([^"]+)"', re.IGNORECASE)
    for path in sorted(en_root.glob("*.html")):
        rel_path = path.name
        if rel_path == "404.html":
            continue  # skip 404
        html = path.read_text(encoding="utf-8")
        m = OG_URL_RE.search(html)
        if not m:
            continue
        current_og_url = m.group(1)
        # If og:url is KA root URL (no /en/ prefix), fix it to en/...
        if current_og_url.startswith(f"{DOMAIN}/") and "/en/" not in current_og_url:
            # Build expected en URL
            slug_match = re.match(rf"{re.escape(DOMAIN)}/([^/]+)/?", current_og_url)
            if slug_match:
                slug = slug_match.group(1)
                new_og_url = f"{DOMAIN}/en/{slug}.html"
                if rel_path == "index.html":
                    new_og_url = f"{DOMAIN}/en/"
                html = html.replace(
                    f'<meta property="og:url" content="{current_og_url}">',
                    f'<meta property="og:url" content="{new_og_url}">',
                    1,
                )
                path.write_text(html, encoding="utf-8")
                print(f"  ✓ en/{rel_path}: og:url {current_og_url} → {new_og_url}")
                fixed += 1
    # Also handle en/tools/*
    for subdir in ["tools", "case-studies", "industries", "blog"]:
        d = en_root / subdir
        if not d.exists():
            continue
        for path in sorted(d.glob("*.html")):
            html = path.read_text(encoding="utf-8")
            m = OG_URL_RE.search(html)
            if not m:
                continue
            current_og_url = m.group(1)
            if current_og_url.startswith(f"{DOMAIN}/") and "/en/" not in current_og_url:
                # Build new
                slug_match = re.match(rf"{re.escape(DOMAIN)}/{subdir}/([^/]+)/?", current_og_url)
                if slug_match:
                    slug = slug_match.group(1)
                    new_og_url = f"{DOMAIN}/en/{subdir}/{slug}.html"
                    html = html.replace(
                        f'<meta property="og:url" content="{current_og_url}">',
                        f'<meta property="og:url" content="{new_og_url}">',
                        1,
                    )
                    path.write_text(html, encoding="utf-8")
                    rel_disp = f"en/{subdir}/{path.name}"
                    print(f"  ✓ {rel_disp}: og:url {current_og_url} → {new_og_url}")
                    fixed += 1
    print(f"\nTotal og:url fixes: {fixed}")


if __name__ == "__main__":
    print("=== Fixing 4 root canonicals to /page/ format ===")
    fix_root_canonicals()
    print()
    print("=== Fixing EN og:url to /en/ URLs ===")
    fix_en_og_url()
