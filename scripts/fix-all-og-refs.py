#!/usr/bin/env python3
"""Fix all remaining broken OG references in HTML files."""
import re
from pathlib import Path

ROOT = Path("/Users/imac/SEO/command-center")

# Map: old filename → (KA new, EN new) — used in regex to replace within HTML
# (key is the file portion only, no path)
KA_EN_MAP = {
    "home-og.png":                                  ("page-home.jpg", "page-home-en.jpg"),
    "about-og.png":                                 ("page-about-us.jpg", "page-about-us-en.jpg"),
    "seo-audit-og.png":                             ("service-seo-audit.jpg", "seo-audit-en.jpg"),
    "seo-management-og.png":                        ("service-seo-mgmt.jpg", "service-seo-mgmt-en.jpg"),
    "case-250-percent-increase-og.png":             ("case-250-percent.jpg", "case-250-percent.jpg"),
    "case-270-percent-increase-og.png":             ("case-270-percent.jpg", "case-270-percent.jpg"),
    "case-3x-in-28-days-og.png":                    ("case-3x-28days.jpg", "case-3x-28days.jpg"),
    "case-4200-yoveltviuri-vizitori-4-tveshi-og.png":("case-4200-visitors.jpg","case-4200-visitors.jpg"),
    "case-local-seo-result-og.png":                 ("case-local-seo.jpg", "case-local-seo.jpg"),
    "case-seo-crisis-management-og.png":            ("case-crisis-mgmt.jpg", "case-crisis-mgmt.jpg"),
    "case-seo-krizisidan-top-3mde-og.png":          ("case-crisis-top3.jpg", "case-crisis-top3.jpg"),
    "case-stomatologiuri-klinikis-seo-og.png":      ("case-dental.jpg", "case-dental.jpg"),
    "case-trafikis-gaormageba-3-tveshi-og.png":     ("case-2x-traffic.jpg", "case-2x-traffic.jpg"),
}

# EN pages still on WP URLs — map old WP URL pattern → target local file
WP_REPLACEMENTS = {
    # EN Case Studies — use existing KA case JPGs (language-neutral)
    "en/case-studies/250-percent-increase.html":             "case-250-percent.jpg",
    "en/case-studies/270-percent-increase.html":             "case-270-percent.jpg",
    "en/case-studies/3x-in-28-days.html":                    "case-3x-28days.jpg",
    "en/case-studies/4200-yoveltviuri-vizitori-4-tveshi.html":"case-4200-visitors.jpg",
    "en/case-studies/local-seo-result.html":                 "case-local-seo.jpg",
    "en/case-studies/seo-crisis-management.html":            "case-crisis-mgmt.jpg",
    "en/case-studies/seo-krizisidan-top-3mde.html":          "case-crisis-top3.jpg",
    "en/case-studies/stomatologiuri-klinikis-seo.html":      "case-dental.jpg",
    "en/case-studies/trafikis-gaormageba-3-tveshi.html":     "case-2x-traffic.jpg",
    "en/case-studies.html":                                  "page-case-studies.jpg",

    # EN Tools — use KA tool JPGs (tool OG images are language-neutral)
    "en/tools/content-brief-builder.html": "tool-content-brief.jpg",
    "en/tools/keyword-density.html":       "tool-keyword-density.jpg",
    "en/tools/numbers-to-words.html":      "tool-numbers-words.jpg",
    "en/tools/og-preview.html":            "tool-og-preview.jpg",
    "en/tools/pixel-width-checker.html":   "tool-pixel-width.jpg",
    "en/tools/readability-score.html":     "tool-readability.jpg",
    "en/tools/seo-content-editor.html":    "tool-content-editor.jpg",
}

changes = {"refs_fixed": 0, "wp_fixed": 0}

# === Step 1: Replace broken *-og.png refs in all HTML files ===
for f in ROOT.rglob("*.html"):
    s = str(f.relative_to(ROOT))
    if any(x in s for x in [".venv","_archive","og-per-","case-studies-v","og-fb-all","og-en-temp"]): continue
    try: content = f.read_text(encoding="utf-8")
    except: continue
    is_en = s.startswith("en/")
    new_content = content
    for old_file, (ka_new, en_new) in KA_EN_MAP.items():
        new_file = en_new if is_en else ka_new
        # Replace any 10xseo.ge URL containing old file → new file
        pattern = re.escape(old_file)
        # Specifically: in any href or content attribute with images/og/{old}
        new_content = re.sub(
            rf'images/og/{pattern}',
            f'images/og/{new_file}',
            new_content
        )
        # Also handle without images/og prefix (some refs might be different)
        # Don't be too aggressive
    if new_content != content:
        f.write_text(new_content, encoding="utf-8")
        changes["refs_fixed"] += 1

# === Step 2: Replace WP URLs in EN case-studies and tools ===
for rel_path, target_jpg in WP_REPLACEMENTS.items():
    f = ROOT / rel_path
    if not f.exists(): continue
    content = f.read_text(encoding="utf-8")
    new_url = f"https://10xseo.ge/images/og/{target_jpg}"

    # Replace WP URLs
    new_content = re.sub(
        r'https://10xseo\.ge/wp-content/uploads/[^"]+\.(png|jpg|webp)',
        new_url,
        content
    )
    # Also ensure dimensions are correct
    new_content = re.sub(r'<meta\s+property="og:image:width"\s+content="[^"]+"',
                        '<meta property="og:image:width" content="1200"', new_content)
    new_content = re.sub(r'<meta\s+property="og:image:height"\s+content="[^"]+"',
                        '<meta property="og:image:height" content="630"', new_content)
    new_content = re.sub(r'<meta\s+property="og:image:type"\s+content="[^"]+"',
                        '<meta property="og:image:type" content="image/jpeg"', new_content)
    if new_content != content:
        f.write_text(new_content, encoding="utf-8")
        changes["wp_fixed"] += 1
        print(f"  ✓ {rel_path}")

print(f"\n{changes['refs_fixed']} files: *-og.png refs replaced")
print(f"{changes['wp_fixed']} files: WP URLs → local JPG")
