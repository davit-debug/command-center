#!/usr/bin/env python3
"""Add skip-nav link to pages flagged by audit Stage 19.

Skip-nav: <a href="#main-content" class="sr-only focus:not-sr-only ...">გადახტომა მთავარ შინაარსზე</a>
Insertion: right after <body ...> opening tag.
"""
import argparse
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIT = ROOT / "audit" / "prelaunch-2026-05-12"

SKIP_NAV_KA = '<a href="#main-content" class="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-[9999] focus:bg-primary focus:text-white focus:px-4 focus:py-2 focus:rounded-lg">გადახტომა მთავარ შინაარსზე</a>'
SKIP_NAV_EN = '<a href="#main-content" class="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-[9999] focus:bg-primary focus:text-white focus:px-4 focus:py-2 focus:rounded-lg">Skip to main content</a>'

BODY_OPEN_RE = re.compile(r'(<body\b[^>]*>)', re.IGNORECASE)
SKIP_NAV_RE = re.compile(r'<a[^>]*href="#main(-content)?"[^>]*>', re.IGNORECASE)


def load_missing_skip_pages() -> list[str]:
    pages = []
    with (AUDIT / "19_a11y_summary.csv").open() as f:
        for r in csv.DictReader(f):
            if r["has_skip_nav"] == "no":
                p = r["path"]
                name = Path(p).name
                # Skip og-variant root pages
                if "/" not in p and name.startswith(("og-", "cta-picker", "menu-rename")):
                    continue
                pages.append(p)
    return pages


def add_skip_nav(html: str, is_en: bool) -> tuple[str, bool]:
    if SKIP_NAV_RE.search(html):
        return html, False  # already present
    body_match = BODY_OPEN_RE.search(html)
    if not body_match:
        return html, False
    snippet = SKIP_NAV_EN if is_en else SKIP_NAV_KA
    insert_at = body_match.end()
    new_html = html[:insert_at] + "\n" + snippet + html[insert_at:]
    return new_html, True


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()
    if not (args.dry_run or args.apply):
        import sys; sys.exit("Specify --dry-run or --apply")

    pages = load_missing_skip_pages()
    print(f"Found {len(pages)} pages missing skip-nav (excl. variants)")
    modified = 0
    for rel in pages:
        path = ROOT / rel
        if not path.exists():
            print(f"  ✗ {rel}: file not found")
            continue
        html = path.read_text(encoding="utf-8")
        is_en = rel.startswith("en/")
        new_html, changed = add_skip_nav(html, is_en)
        if not changed:
            print(f"  - {rel}: already has skip-nav OR no <body>")
            continue
        if args.apply:
            path.write_text(new_html, encoding="utf-8")
        modified += 1
    print(f"\nModified: {modified} / {len(pages)} {'(DRY-RUN)' if args.dry_run else ''}")


if __name__ == "__main__":
    main()
