#!/usr/bin/env python3
"""
Launch prep fix #2 + bundled #6 finisher.

Removes <meta name="robots" content="noindex,..."> from all production
pages listed in sitemap.xml. Leaves 404.html and lead-form.html alone.

Also fixes seo-audit.html's canonical/og:url + schema url/item to use
.html form (matching filesystem) and updates the sitemap entry to match.
"""
import re
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# Files to KEEP noindex on (intentionally not indexed)
KEEP_NOINDEX = {
    '404.html',
    'en/404.html',
    'lead-form.html',
    'en/lead-form.html',
}

NOINDEX_PATTERNS = [
    re.compile(r'\s*<meta\s+name="robots"\s+content="noindex,\s*nofollow"\s*/?>\n?'),
    re.compile(r'\s*<meta\s+name="robots"\s+content="noindex,\s*follow"\s*/?>\n?'),
    re.compile(r'\s*<meta\s+name="robots"\s+content="noindex"\s*/?>\n?'),
]

# Build sitemap → local-path list
with open('sitemap.xml') as f:
    sitemap = f.read()
urls = re.findall(r'<loc>https://10xseo\.ge/([^<]*)</loc>', sitemap)

# Convert URL paths to local file paths
def url_to_path(url):
    if not url or url.endswith('/'):
        # /something/ → something.html (per filesystem convention) OR index.html for root
        if not url:
            return 'index.html'
        # Try dir/index.html first, then trimmed .html
        dir_path = url + 'index.html'
        html_path = url[:-1] + '.html'
        if os.path.exists(dir_path):
            return dir_path
        if os.path.exists(html_path):
            return html_path
        return None
    return url if os.path.exists(url) else None

# Process noindex removal
removed = []
skipped_keep = []
skipped_missing = []
skipped_no_noindex = []

for url in urls:
    path = url_to_path(url)
    if path is None:
        skipped_missing.append(url)
        continue
    if path in KEEP_NOINDEX:
        skipped_keep.append(path)
        continue
    with open(path) as f:
        content = f.read()
    original = content
    for pat in NOINDEX_PATTERNS:
        content = pat.sub('\n', content)
    # Collapse any triple newlines we may have created
    content = re.sub(r'\n{3,}', '\n\n', content)
    if content != original:
        with open(path, 'w') as f:
            f.write(content)
        removed.append(path)
    else:
        skipped_no_noindex.append(path)

print(f"=== noindex removal ===")
print(f"  Removed from: {len(removed)} files")
print(f"  Kept (intentional): {len(skipped_keep)} → {skipped_keep}")
print(f"  No noindex found: {len(skipped_no_noindex)}")
print(f"  Missing files: {len(skipped_missing)} → {skipped_missing}")

# === seo-audit URL form fix (matches about-us/portfolio approach) ===
print(f"\n=== seo-audit URL form fix ===")
seo_audit_path = 'seo-audit.html'
if os.path.exists(seo_audit_path):
    with open(seo_audit_path) as f:
        content = f.read()
    new_content = content.replace(
        'https://10xseo.ge/seo-audit/"',
        'https://10xseo.ge/seo-audit.html"'
    )
    if new_content != content:
        with open(seo_audit_path, 'w') as f:
            f.write(new_content)
        diff_count = content.count('https://10xseo.ge/seo-audit/"')
        print(f"  Fixed {diff_count} URL-context references in seo-audit.html")
    else:
        print(f"  seo-audit.html: no changes needed (already .html or already fixed)")

# === sitemap.xml: /seo-audit/ → /seo-audit.html ===
new_sitemap = sitemap.replace(
    'https://10xseo.ge/seo-audit/',
    'https://10xseo.ge/seo-audit.html'
)
if new_sitemap != sitemap:
    with open('sitemap.xml', 'w') as f:
        f.write(new_sitemap)
    diff = sitemap.count('https://10xseo.ge/seo-audit/')
    print(f"  Fixed {diff} entries in sitemap.xml")
else:
    print(f"  sitemap.xml: no /seo-audit/ entries found")
