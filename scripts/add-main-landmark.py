#!/usr/bin/env python3
"""Add <main id="main-content"> landmark to pages flagged by audit Stage 19.

Insertion rule:
  - Open: right after the mobile-menu closing `</div>` (or `</header>` if no mobile-menu)
  - Close: right before `<footer` tag

Idempotent — skips pages that already have <main>.
"""
import argparse
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIT = ROOT / "audit" / "prelaunch-2026-05-12"

MAIN_OPEN = '<main id="main-content">'
MAIN_CLOSE = '</main>'

# Pattern: mobile-menu div + everything inside + closing </div>
# We match the entire mobile-menu block as one unit.
MOBILE_MENU_RE = re.compile(
    r'<div\s+id="mobile-menu"[^>]*>.*?</nav>\s*</div>',
    re.IGNORECASE | re.DOTALL
)
HEADER_CLOSE_RE = re.compile(r'</header>', re.IGNORECASE)
FOOTER_OPEN_RE = re.compile(r'<footer\b', re.IGNORECASE)


def load_missing_main_pages() -> list[str]:
    pages = []
    with (AUDIT / "19_a11y_summary.csv").open() as f:
        for r in csv.DictReader(f):
            if r["has_main"] == "no":
                p = r["path"]
                name = Path(p).name
                # Skip ONLY variant/test pages at root level (tools/og-preview is real)
                if "/" not in p and name.startswith(("og-", "cta-picker", "menu-rename")):
                    continue
                pages.append(p)
    return pages


def add_main(html: str) -> tuple[str, bool]:
    """Returns (new_html, modified)."""
    if "<main" in html.lower():
        return html, False  # Already has main

    # Find insertion point after mobile-menu (preferred) or </header>
    mobile_match = MOBILE_MENU_RE.search(html)
    if mobile_match:
        insert_at = mobile_match.end()
    else:
        header_match = HEADER_CLOSE_RE.search(html)
        if header_match:
            insert_at = header_match.end()
        else:
            return html, False  # Can't find anchor

    # Find closing point before <footer>
    footer_match = FOOTER_OPEN_RE.search(html, insert_at)
    if not footer_match:
        return html, False  # No footer found

    close_at = footer_match.start()

    # Insert MAIN_OPEN and MAIN_CLOSE
    new_html = (
        html[:insert_at]
        + "\n" + MAIN_OPEN + "\n"
        + html[insert_at:close_at]
        + MAIN_CLOSE + "\n"
        + html[close_at:]
    )
    return new_html, True


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()
    if not (args.dry_run or args.apply):
        import sys
        sys.exit("Specify --dry-run or --apply")

    pages = load_missing_main_pages()
    print(f"Found {len(pages)} pages missing <main> landmark (excl. variants)")
    print()

    modified = 0
    for rel in pages:
        path = ROOT / rel
        if not path.exists():
            print(f"  ✗ {rel}: file not found")
            continue
        html = path.read_text(encoding="utf-8")
        new_html, changed = add_main(html)
        if not changed:
            print(f"  - {rel}: already has main OR no anchor found")
            continue
        print(f"  ✓ {rel}")
        modified += 1
        if args.apply:
            path.write_text(new_html, encoding="utf-8")
    print()
    print(f"Modified: {modified} / {len(pages)} {'(DRY-RUN)' if args.dry_run else ''}")


if __name__ == "__main__":
    main()
