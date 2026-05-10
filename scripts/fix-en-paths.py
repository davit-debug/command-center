#!/usr/bin/env python3
"""Fix relative resource paths in /en/ pages to escape the /en/ subtree.

For each /en/<page>.html at depth d (within /en/), relative paths to
shared resources (blog/, images/, fonts/, videos/, assets/) and to
KA-only pages (blog post html files) need (d+1) ../ prefixes total.

Also adds hreflang="ka" to blog post links (skipped pages).
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Resource directory prefixes that should escape /en/ to root
SHARED_DIRS = ('blog/', 'images/', 'fonts/', 'videos/', 'assets/')

# href to skipped pages → add hreflang="ka"
SKIPPED_PAGE_PATTERNS = [
    r'(?:\.\./)*blog/[\w-]+\.html',  # blog post URLs
]


def fix_file(en_path: Path, dry_run: bool = False):
    rel = en_path.relative_to(ROOT / "en")
    rel_parts = rel.parts
    depth = len(rel_parts) - 1  # depth within /en/ (0 for /en/index.html)

    print(f"=== en/{rel} (depth {depth}) ===")

    html = en_path.read_text(encoding="utf-8-sig")
    fixes = 0

    # Required prefix to escape /en/ + climb out of subdirs
    needed_prefix = '../' * (depth + 1)

    for shared in SHARED_DIRS:
        # Pattern: href="<existing-prefix>blog/foo" or src="<existing-prefix>blog/foo"
        for attr in ('href', 'src'):
            pattern = re.compile(
                rf'\b{attr}="((?:\.\./)*){re.escape(shared)}([^"]+)"'
            )
            def replacer(m):
                nonlocal fixes
                current_prefix = m.group(1)
                rest = m.group(2)
                if current_prefix == needed_prefix:
                    return m.group(0)
                fixes += 1
                return f'{attr}="{needed_prefix}{shared}{rest}"'
            html = pattern.sub(replacer, html)

    # Favicon files at root (favicon.svg, favicon.ico, favicon-*.png, apple-touch-icon.png)
    favicon_files = ['favicon.svg', 'favicon.ico', 'favicon-32x32.png', 'apple-touch-icon.png']
    for fav in favicon_files:
        for attr in ('href', 'src'):
            pattern = re.compile(
                rf'\b{attr}="((?:\.\./)*){re.escape(fav)}"'
            )
            def fav_replacer(m):
                nonlocal fixes
                current_prefix = m.group(1)
                if current_prefix == needed_prefix:
                    return m.group(0)
                fixes += 1
                return f'{attr}="{needed_prefix}{fav}"'
            html = pattern.sub(fav_replacer, html)

    # Add hreflang="ka" to blog post links
    blog_link_re = re.compile(
        rf'<a([^>]*\bhref="(?:\.\./)+blog/[\w-]+\.html")(?![^>]*hreflang=)([^>]*)>'
    )
    def add_hreflang(m):
        nonlocal fixes
        fixes += 1
        return f'<a{m.group(1)} hreflang="ka"{m.group(2)}>'
    html = blog_link_re.sub(add_hreflang, html)

    print(f"  Fixed {fixes} paths")

    if dry_run or fixes == 0:
        return

    en_path.write_text(html, encoding="utf-8")
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
            fix_file(f, dry_run=args.dry_run)
    elif args.page:
        fix_file(ROOT / "en" / args.page, dry_run=args.dry_run)
    else:
        sys.exit("Specify --page or --all")


if __name__ == "__main__":
    sys.exit(main())
