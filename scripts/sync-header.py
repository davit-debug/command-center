#!/usr/bin/env python3
"""
Header sync — single source of truth = index.html
Replaces <header id="main-header"...></header> + mobile-menu block
on every production page with the canonical version from index.html.

Usage:
  python3 scripts/sync-header.py              # dry-run (default)
  python3 scripts/sync-header.py --apply      # writes changes
  python3 scripts/sync-header.py --target FILE  # operate on single file
  python3 scripts/sync-header.py --verify-only  # re-checks state

Boundary: from `<header id="main-header"` (inclusive) up to (but not
including) the next `<main` tag. This captures the sticky <header>
plus the #mobile-menu overlay that follows it.

Logo href is rewritten:
  - index.html source has <a href="#" ...> (logo on the homepage itself)
  - on inner pages it becomes <a href="index.html" ...> (root) or
    <a href="../index.html" ...>, <a href="../../index.html" ...> per depth.
The mobile-menu first item ("მთავარი") gets the same treatment.
"""
import argparse
import fnmatch
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_FILE = REPO_ROOT / 'index.html'  # KA source-of-truth
EN_SOURCE_FILE = REPO_ROOT / 'en' / 'index.html'  # EN source-of-truth

# Same exclude set as sync-footer.py — design variants / tests / backups
EXCLUDE_PATTERNS = [
    'index.html',
    '*-options.html', '*-options-*.html',
    'animation-options.html', 'before-after-options.html',
    'blog-layout-options.html', 'case-studies-options.html',
    'case-study-inner-options.html',
    'color-compare.html', 'color-options.html', 'cta-colors.html',
    'faq-service-*.html',
    'favicon-*.html', 'font-options.html',
    'footer-variants.html',
    'hex-animations.html', 'journey-preview.html',
    'logo-options*.html', 'logo-compare.html',
    'new-sections.html', 'team-variants.html', 'why-us-variants.html',
    'test*.html',
    '*-v[0-9].html', '*-v[0-9]-*.html', '*-backup.html', '*-old.html',
    'index-v*.html', 'v[0-9].html',
    'about-final-v2.html',
    'construction-clarity.html', 'construction-editorial.html',
    'construction-full-stack.html', 'construction-manifesto.html',
    'construction-mid-market-quiz.html',
    'construction-premium-multi-project.html',
    'construction-project-architecture.html', 'construction-pyramid-hero.html',
    'construction-realestate-*.html',
    'construction-roi-calculator.html',
    'construction-skyscraper-gallery.html',
    'construction-vsl-cold-traffic.html',
    'healthcare-v1.html',
    'real-estate-developers.html',
    'skyscraper-gallery.html',
    '_TEMPLATE.html',
]

EXCLUDE_DIRS = {'.git', '.claude', '.github', 'audit', 'node_modules', 'scripts', 'assets'}

SKIP_URL_PREFIXES = (
    'http://', 'https://', '//', 'mailto:', 'tel:',
    'data:', '#', 'javascript:',
)

HEADER_START_RE = re.compile(r'<header\s+id=["\']main-header["\']', re.IGNORECASE)
MAIN_START_RE = re.compile(r'<main\b', re.IGNORECASE)
MOBILE_MENU_START_RE = re.compile(r'<div\s+id=["\']mobile-menu["\']', re.IGNORECASE)
DIV_OPEN_RE = re.compile(r'<div\b', re.IGNORECASE)
DIV_CLOSE_RE = re.compile(r'</div\s*>', re.IGNORECASE)
HREF_SRC_RE = re.compile(r'\b(href|src)=(["\'])([^"\']+)\2')


def find_mobile_menu_end(html, search_from):
    """Find end-of-block (after closing </div>) for the #mobile-menu wrapper
    using balanced <div> counting. Returns absolute byte offset, or None."""
    m = MOBILE_MENU_START_RE.search(html, search_from)
    if not m:
        return None
    pos = m.end()
    depth = 1
    while depth > 0:
        no = DIV_OPEN_RE.search(html, pos)
        nc = DIV_CLOSE_RE.search(html, pos)
        if not nc:
            return None
        if no and no.start() < nc.start():
            depth += 1
            pos = no.end()
        else:
            depth -= 1
            pos = nc.end()
            if depth == 0:
                # absorb trailing whitespace + newlines so replacement doesn't
                # leave a stray blank line
                while pos < len(html) and html[pos] in ' \t\r\n':
                    pos += 1
                return pos
    return None

# Logo: <a href="#" class="flex items-center shrink-0"...>
LOGO_HREF_RE = re.compile(
    r'(<a\s+href=)(["\'])#\2(\s+class=["\']flex items-center shrink-0)',
    re.IGNORECASE,
)
# Mobile menu first item — "მთავარი"
MOBILE_HOME_RE = re.compile(
    r'(<a\s+href=)(["\'])#\2([^>]*data-ka=["\']მთავარი["\'])',
    re.IGNORECASE,
)


def relative_path(path):
    return path.relative_to(REPO_ROOT)


def is_en_path(path):
    """True if file lives under /en/ (English locale subtree)."""
    parts = relative_path(path).parts
    return bool(parts) and parts[0] == 'en'


def compute_depth(path):
    """Depth from the language root (KA root or /en/ root). /en/foo.html → 0."""
    parts = relative_path(path).parts
    if parts and parts[0] == 'en':
        return len(parts) - 2  # depth within /en/
    return len(parts) - 1  # depth from REPO_ROOT


def is_excluded(path):
    name = path.name
    rel = str(relative_path(path))
    for pattern in EXCLUDE_PATTERNS:
        if fnmatch.fnmatch(name, pattern):
            return True
        if fnmatch.fnmatch(rel, pattern):
            return True
    return False


def extract_header_block(html):
    """Find span from <header id="main-header" ... up to:
       (1) next <main tag if present, else
       (2) end of #mobile-menu wrapper (balanced div counting).
    Returns (start, end) or (None, None) if no usable end marker."""
    m_start = HEADER_START_RE.search(html)
    if not m_start:
        return None, None
    # Prefer <main\b
    main_m = MAIN_START_RE.search(html, m_start.end())
    if main_m:
        return m_start.start(), main_m.start()
    # Fallback: end of #mobile-menu div
    mm_end = find_mobile_menu_end(html, m_start.end())
    if mm_end is not None:
        return m_start.start(), mm_end
    return None, None


def adjust_paths(block_html, depth):
    """Prepend ../ to relative URLs based on depth (subdir nesting)."""
    if depth <= 0:
        return block_html
    prefix = '../' * depth

    def replace(match):
        attr = match.group(1)
        quote = match.group(2)
        url = match.group(3)
        if url.startswith(SKIP_URL_PREFIXES):
            return match.group(0)
        return f'{attr}={quote}{prefix}{url}{quote}'

    return HREF_SRC_RE.sub(replace, block_html)


def swap_home_logo_to_default(block_html):
    """Replace V4 home-only logo (logo-home.*) with the V2 default (logo.*).
    The home page (index.html) uses a yellow-only V4 mark; every other page
    uses the bicolor V2. Same width/height/class -> no layout shift on nav.
    Called when propagating index.html's header to other pages."""
    return (block_html
            .replace('images/logo-home.webp', 'images/logo.webp')
            .replace('images/logo-home.png', 'images/logo.png'))


def rewrite_logo_links(block_html, depth):
    """Convert href="#" → href="index.html" (or ../index.html etc.)
    on the logo anchor and the mobile-menu home item."""
    target = 'index.html'
    if depth > 0:
        target = '../' * depth + target

    def logo_repl(m):
        return f'{m.group(1)}{m.group(2)}{target}{m.group(2)}{m.group(3)}'

    def home_repl(m):
        return f'{m.group(1)}{m.group(2)}{target}{m.group(2)}{m.group(3)}'

    block_html = LOGO_HREF_RE.sub(logo_repl, block_html)
    block_html = MOBILE_HOME_RE.sub(home_repl, block_html)
    return block_html


def collect_targets():
    targets = []
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fn in filenames:
            if not fn.endswith('.html'):
                continue
            full = Path(dirpath) / fn
            if full == SOURCE_FILE or full == EN_SOURCE_FILE:
                continue
            if is_excluded(full):
                continue
            try:
                if full.stat().st_size > 5_000_000:
                    print(f"  SKIP (too large >5MB): {relative_path(full)}", file=sys.stderr)
                    continue
            except OSError:
                continue
            targets.append(full)
    return sorted(targets)


def categorize(html):
    """Returns OK / NO_HEADER / NO_END_MARKER."""
    h = HEADER_START_RE.search(html)
    if not h:
        return 'NO_HEADER'
    if MAIN_START_RE.search(html, h.end()):
        return 'OK'
    if find_mobile_menu_end(html, h.end()) is not None:
        return 'OK'
    return 'NO_END_MARKER'


def process_file(path, ka_source_block, en_source_block, dry_run=True):
    html = path.read_text(encoding='utf-8-sig')
    cat = categorize(html)
    if cat != 'OK':
        return 'aborted', cat

    s, e = extract_header_block(html)
    if s is None:
        return 'aborted', 'extraction_failed'

    if is_en_path(path):
        if en_source_block is None:
            return 'aborted', 'no_en_source'
        source_block = en_source_block
    else:
        source_block = ka_source_block

    depth = compute_depth(path)
    adjusted = adjust_paths(source_block, depth)
    adjusted = rewrite_logo_links(adjusted, depth)
    adjusted = swap_home_logo_to_default(adjusted)

    existing = html[s:e]
    if existing == adjusted:
        return 'unchanged', 'in_sync'

    new_html = html[:s] + adjusted + html[e:]
    if not dry_run:
        path.write_text(new_html, encoding='utf-8')
    return 'changed', 'replaced'


def verify_file(path):
    errors = []
    html = path.read_text(encoding='utf-8-sig')
    h_count = len(HEADER_START_RE.findall(html))
    m_count = len(MAIN_START_RE.findall(html))
    if h_count != 1:
        errors.append(f"<header id=main-header> count: {h_count} (expected 1)")
    if m_count < 1:
        errors.append(f"<main> count: {m_count} (expected ≥1)")
    if '</body>' not in html[-300:]:
        errors.append("</body> missing in tail")
    if '</html>' not in html[-300:]:
        errors.append("</html> missing in tail")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Write changes (default: dry-run)')
    parser.add_argument('--verify-only', action='store_true', help='Re-check state without writing')
    parser.add_argument('--target', type=str, help='Process single file (relative to repo root)')
    parser.add_argument('--verbose', action='store_true', help='Print every file action')
    args = parser.parse_args()

    if not SOURCE_FILE.exists():
        print(f"ERROR: source file not found: {SOURCE_FILE}", file=sys.stderr)
        return 1

    ka_source_html = SOURCE_FILE.read_text(encoding='utf-8-sig')
    s, e = extract_header_block(ka_source_html)
    if s is None:
        print(f"ERROR: cannot find <header id=main-header> + <main> in {SOURCE_FILE}", file=sys.stderr)
        return 1
    ka_source_block = ka_source_html[s:e]
    line_count = ka_source_block.count('\n') + 1
    print(f"✓ Extracted KA source header+menu from index.html ({len(ka_source_block)} bytes, {line_count} lines)")

    en_source_block = None
    if EN_SOURCE_FILE.exists():
        en_source_html = EN_SOURCE_FILE.read_text(encoding='utf-8-sig')
        en_s, en_e = extract_header_block(en_source_html)
        if en_s is not None:
            en_source_block = en_source_html[en_s:en_e]
            en_lines = en_source_block.count('\n') + 1
            print(f"✓ Extracted EN source header+menu from en/index.html ({len(en_source_block)} bytes, {en_lines} lines)")
        else:
            print(f"⚠ en/index.html exists but header block not found — /en/ targets will be skipped")
    else:
        print(f"  (en/index.html not found — only KA targets will be synced)")

    if args.target:
        targets = [REPO_ROOT / args.target]
        if not targets[0].exists():
            print(f"ERROR: target not found: {targets[0]}", file=sys.stderr)
            return 1
    else:
        targets = collect_targets()
    print(f"✓ Collected {len(targets)} target files")

    categories = {'OK': [], 'NO_HEADER': [], 'NO_END_MARKER': []}
    for path in targets:
        try:
            html = path.read_text(encoding='utf-8-sig')
            categories[categorize(html)].append(path)
        except Exception as ex:
            print(f"  ERROR reading {relative_path(path)}: {ex}", file=sys.stderr)

    print("\nPre-flight categorization:")
    for cat, files in categories.items():
        marker = ' ⚠' if cat != 'OK' else ''
        print(f"  {cat:12s}: {len(files):4d} files{marker}")

    if categories['NO_HEADER'] or categories['NO_END_MARKER']:
        print("\n⚠ Files needing manual review (no <header id=main-header> or no end marker):")
        for path in categories['NO_HEADER'] + categories['NO_END_MARKER']:
            print(f"    {relative_path(path)}")

    if args.verify_only:
        print("\n--verify-only: checking current state...")
        all_errors = {}
        for path in categories['OK']:
            errors = verify_file(path)
            if errors:
                all_errors[path] = errors
        if all_errors:
            print(f"\n⚠ {len(all_errors)} files have issues:")
            for path, errors in all_errors.items():
                print(f"  {relative_path(path)}:")
                for err in errors:
                    print(f"    - {err}")
            return 1
        print(f"✓ All {len(categories['OK'])} OK files verified")
        return 0

    print(f"\n{'APPLYING' if args.apply else 'DRY-RUN'}...")
    changed, unchanged, aborted = [], [], []
    for path in targets:
        cat = categorize(path.read_text(encoding='utf-8-sig'))
        if cat != 'OK':
            aborted.append((path, cat))
            continue
        try:
            action, msg = process_file(path, ka_source_block, en_source_block, dry_run=not args.apply)
            if action == 'changed':
                changed.append(path)
                if args.verbose:
                    print(f"  CHANGE  {relative_path(path)}")
            elif action == 'unchanged':
                unchanged.append(path)
            else:
                aborted.append((path, msg))
                print(f"  ABORT   {relative_path(path)}  ({msg})")
        except Exception as ex:
            aborted.append((path, str(ex)))
            print(f"  ERROR   {relative_path(path)}: {ex}", file=sys.stderr)

    by_dir = {}
    for path in changed:
        parts = relative_path(path).parts
        d = parts[0] if len(parts) > 1 else '(root)'
        by_dir[d] = by_dir.get(d, 0) + 1

    print(f"\nSummary:")
    print(f"  Changed:   {len(changed)} files")
    for d, n in sorted(by_dir.items()):
        print(f"    {d}/: {n}")
    print(f"  Unchanged: {len(unchanged)} files (already in sync)")
    print(f"  Aborted:   {len(aborted)} files")

    if args.apply and changed:
        print(f"\n✓ Verifying {len(changed)} modified files...")
        all_errors = {}
        for path in changed:
            errors = verify_file(path)
            if errors:
                all_errors[path] = errors
        if all_errors:
            print(f"\n⚠ POST-WRITE VERIFICATION FAILED for {len(all_errors)} files:")
            for path, errors in all_errors.items():
                print(f"  {relative_path(path)}:")
                for err in errors:
                    print(f"    - {err}")
            return 1
        print(f"  ✓ Tag balance + position checks passed")

    if args.apply:
        print(f"\nNext steps:")
        print(f"  git -C {REPO_ROOT} status")
        print(f"  git -C {REPO_ROOT} diff --stat | head -30")
    else:
        print(f"\nDry-run complete. Re-run with --apply to write changes.")

    return 0 if not aborted else 1


if __name__ == '__main__':
    sys.exit(main())
