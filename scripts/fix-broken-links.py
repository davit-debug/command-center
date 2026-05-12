#!/usr/bin/env python3
"""Fix the 10 broken internal links found by Stage 17 audit."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (file_path, old_href, new_href, description)
FIXES = [
    ("blog/seo-copywriting.html", 'href="../cifruli-marketingi.html"', 'href="cifruli-marketingi.html"',
     "rel path: parent → sibling in /blog/"),
    ("blog/seo-copywriting.html", 'href="../seo-auditi.html"', 'href="../seo-audit.html"',
     "typo: seo-auditi → seo-audit"),
    ("blog/seo-2025.html", 'href="../seo-auditi.html"', 'href="../seo-audit.html"',
     "typo: seo-auditi → seo-audit"),
    ("blog/seo-2025.html", 'href="../seo-optimizacia.html"', 'href="../ra-aris-seo.html"',
     "missing page: redirect to ra-aris-seo (closest topic)"),
    ("blog/cifruli-marketingi.html", 'href="../seo-optimizacia.html"', 'href="../ra-aris-seo.html"',
     "missing page: redirect to ra-aris-seo"),
    ("blog/ra-dro-schireba-seos-shedegebis-misagebad.html", 'href="../miige-shemotavazeba.html"',
     'href="../contact-us.html"', "missing page: redirect to contact-us"),
    ("en/industries/healthcare.html", 'href="../en/industries.html"', 'href="../services.html"',
     "missing page: → services"),
    ("en/industries/ecommerce.html", 'href="../en/industries.html"', 'href="../services.html"',
     "missing page: → services"),
]

# Variations that also need fixing (different href formats)
EXTRA_FIXES = [
    ("en/industries/healthcare.html", 'href="en/industries.html"', 'href="../services.html"', ""),
    ("en/industries/ecommerce.html", 'href="en/industries.html"', 'href="../services.html"', ""),
    ("en/industries/healthcare.html", 'href="../industries.html"', 'href="../services.html"', ""),
    ("en/industries/ecommerce.html", 'href="../industries.html"', 'href="../services.html"', ""),
    # KA equivalents (missed in first pass)
    ("industries/healthcare.html", 'href="../industries.html"', 'href="../services.html"', "missing page: → services"),
    ("industries/ecommerce.html", 'href="../industries.html"', 'href="../services.html"', "missing page: → services"),
    ("industries/construction.html", 'href="../industries.html"', 'href="../services.html"', ""),
    ("industries/financial-services.html", 'href="../industries.html"', 'href="../services.html"', ""),
]


def main():
    total = 0
    for file_rel, old, new, desc in FIXES + EXTRA_FIXES:
        path = ROOT / file_rel
        if not path.exists():
            print(f"  ✗ {file_rel}: file not found")
            continue
        html = path.read_text(encoding="utf-8")
        count = html.count(old)
        if count == 0:
            print(f"  - {file_rel}: '{old}' not found, skip")
            continue
        new_html = html.replace(old, new)
        path.write_text(new_html, encoding="utf-8")
        print(f"  ✓ {file_rel}: {old} → {new} ({count}x) {desc}")
        total += count
    print(f"\nTotal replacements: {total}")


if __name__ == "__main__":
    main()
