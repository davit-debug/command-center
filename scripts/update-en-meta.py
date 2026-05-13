#!/usr/bin/env python3
"""Update EN HTML files to point to new local OG images instead of WP URLs / wrong paths."""
import re
from pathlib import Path

ROOT = Path("/Users/imac/SEO/command-center")

# Map: HTML path → new og:image filename (without 'images/og/' prefix)
UPDATES = {
    # Services with wrong path
    "en/seo-management.html":   "service-seo-mgmt-en.jpg",
    "en/seo-audit.html":        "seo-audit-en.jpg",
    "en/seo-copywriting.html":  "service-seo-copy-en.jpg",
    # Other pages with WP URLs
    "en/404.html":              "page-404-en.jpg",
    "en/about-us.html":         "page-about-us-en.jpg",
    "en/contact-us.html":       "page-contact-us-en.jpg",
    "en/lead-form.html":        "page-lead-form-en.jpg",
    "en/portfolio.html":        "page-portfolio-en.jpg",
    "en/seo-tools.html":        "service-seo-tools-en.jpg",
    "en/services.html":         "page-services-en.jpg",
    "en/vacancies.html":        "page-vacancies-en.jpg",
    "en/ra-aris-seo.html":      "service-ra-aris-seo-en.jpg",
}

# Alt text per file
ALTS = {
    "service-seo-mgmt-en.jpg":  "SEO Management — Monthly Service · 10×SEO",
    "seo-audit-en.jpg":         "Free SEO Audit — Loom Video Analysis · 10×SEO",
    "service-seo-copy-en.jpg":  "SEO Copywriting — Content That Converts · 10×SEO",
    "page-404-en.jpg":          "404 — Page Not Found · 10×SEO",
    "page-about-us-en.jpg":     "Meet 10×SEO — Georgia's #1 SEO Agency Team",
    "page-contact-us-en.jpg":   "Get In Touch — Book a 15-min Consultation · 10×SEO",
    "page-lead-form-en.jpg":    "Free SEO Consultation — 15-min Strategy Call · 10×SEO",
    "page-portfolio-en.jpg":    "Real Results · +247% Avg Growth · 10×SEO",
    "service-seo-tools-en.jpg": "Free SEO Tools — Pixel Width, OG Preview, Content Editor · 10×SEO",
    "page-services-en.jpg":     "SEO Services — Full Ecosystem for Growth · 10×SEO",
    "page-vacancies-en.jpg":    "Careers — Join Georgia's #1 SEO Agency Team · 10×SEO",
    "service-ra-aris-seo-en.jpg":"What Is SEO? · The Complete Beginner's Guide · 10×SEO",
}

updated = 0
errors = []
for rel_path, new_filename in UPDATES.items():
    f = ROOT / rel_path
    if not f.exists():
        errors.append(f"{rel_path}: file not found"); continue
    content = f.read_text(encoding="utf-8")
    new_url = f"https://10xseo.ge/images/og/{new_filename}"
    alt = ALTS.get(new_filename, "10×SEO")

    # Replace og:image
    new_content = re.sub(
        r'<meta\s+property="og:image"\s+content="[^"]+"',
        f'<meta property="og:image" content="{new_url}"',
        content
    )
    # Replace twitter:image
    new_content = re.sub(
        r'<meta\s+name="twitter:image"\s+content="[^"]+"',
        f'<meta name="twitter:image" content="{new_url}"',
        new_content
    )
    # Replace og:image:width/height/type to ensure correct
    new_content = re.sub(
        r'<meta\s+property="og:image:width"\s+content="[^"]+"',
        f'<meta property="og:image:width" content="1200"',
        new_content
    )
    new_content = re.sub(
        r'<meta\s+property="og:image:height"\s+content="[^"]+"',
        f'<meta property="og:image:height" content="630"',
        new_content
    )
    new_content = re.sub(
        r'<meta\s+property="og:image:type"\s+content="[^"]+"',
        f'<meta property="og:image:type" content="image/jpeg"',
        new_content
    )
    # Ensure alt exists; if not, add after og:image:type
    if 'property="og:image:alt"' not in new_content:
        new_content = new_content.replace(
            '<meta property="og:image:type" content="image/jpeg">',
            f'<meta property="og:image:type" content="image/jpeg">\n<meta property="og:image:alt" content="{alt}">',
            1
        )
    else:
        new_content = re.sub(
            r'<meta\s+property="og:image:alt"\s+content="[^"]+"',
            f'<meta property="og:image:alt" content="{alt}"',
            new_content
        )

    if new_content != content:
        f.write_text(new_content, encoding="utf-8")
        updated += 1
        print(f"  ✓ {rel_path} → {new_filename}")
    else:
        print(f"  - {rel_path} (no change)")

print(f"\nUpdated: {updated} files")
if errors:
    print("Errors:")
    for e in errors: print(f"  ✗ {e}")
