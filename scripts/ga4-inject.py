#!/usr/bin/env python3
"""GA4 injection script. Idempotent — skips pages that already have gtag.

Usage:
    python3 ga4-inject.py G-XXXXXXXXXX           # dry-run, prints what would change
    python3 ga4-inject.py G-XXXXXXXXXX --apply   # write changes

Insertion point: immediately after the first <meta charset="..."> tag in <head>.
Loads gtag.js async via standard Google snippet.
"""
import sys
import re
import glob
import os
from pathlib import Path

BASE = Path("/Users/imac/SEO/command-center")
EXCLUDE_DIRS = ("_archive", "audit", "fonts", "scripts", "assets", "og-per", "og-previews")
EXCLUDE_FILE_PATTERNS = ("__", "variants", "picker")

def ga_snippet(measurement_id: str) -> str:
    return f'''
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={measurement_id}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{measurement_id}');
  </script>'''

def should_skip(rel: str) -> bool:
    parts = rel.split(os.sep)
    if any(p.startswith(EXCLUDE_FILE_PATTERNS) for p in parts): return True
    if any(d in rel for d in EXCLUDE_DIRS): return True
    return False

def inject(measurement_id: str, apply: bool):
    pages = []
    for p in sorted(BASE.rglob("*.html")):
        rel = str(p.relative_to(BASE))
        if should_skip(rel): continue
        pages.append(p)

    snippet = ga_snippet(measurement_id)
    charset_re = re.compile(r'(<meta\s+charset=["\'][^"\']+["\']\s*/?>)', re.IGNORECASE)

    changed = 0
    skipped_existing = 0
    skipped_no_charset = 0
    for p in pages:
        try:
            html = p.read_text(encoding="utf-8")
        except Exception as e:
            print(f"READ ERROR: {p}: {e}"); continue

        # Only skip if the install snippet is present, not just event calls like gtag('event', ...)
        if "googletagmanager.com/gtag/js" in html:
            skipped_existing += 1
            continue

        m = charset_re.search(html)
        if not m:
            print(f"NO CHARSET: {p.relative_to(BASE)}")
            skipped_no_charset += 1
            continue

        new_html = html[:m.end()] + snippet + html[m.end():]

        if apply:
            p.write_text(new_html, encoding="utf-8")
            changed += 1
        else:
            changed += 1

    action = "Modified" if apply else "Would modify"
    print(f"\n{action}: {changed} files")
    print(f"Skipped (already has gtag): {skipped_existing}")
    print(f"Skipped (no <meta charset>): {skipped_no_charset}")
    print(f"Total scanned: {len(pages)}")
    if not apply:
        print("\nDry run — re-run with --apply to write changes.")

if __name__ == "__main__":
    if len(sys.argv) < 2 or not sys.argv[1].startswith("G-"):
        print("Usage: python3 ga4-inject.py G-XXXXXXXXXX [--apply]")
        print("       (Tracking ID must start with 'G-')")
        sys.exit(1)
    measurement_id = sys.argv[1]
    apply = "--apply" in sys.argv
    inject(measurement_id, apply)
