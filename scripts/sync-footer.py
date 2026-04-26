#!/usr/bin/env python3
"""
Footer sync — single source of truth = index.html
Usage:
  python3 scripts/sync-footer.py              # dry-run (default)
  python3 scripts/sync-footer.py --apply      # writes changes
  python3 scripts/sync-footer.py --verify-only # re-checks state
  python3 scripts/sync-footer.py --target FILE # operate on single file

Re-run anytime after editing the <footer> in index.html to propagate
the change to all production HTML pages. Idempotent.
"""

import argparse
import fnmatch
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_FILE = REPO_ROOT / 'index.html'

EXCLUDE_PATTERNS = [
    'index.html',
    # Design exploration / variant pages
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
    # Test/debug
    'test*.html',
    # Versioned backups
    '*-v[0-9].html', '*-v[0-9]-*.html', '*-backup.html', '*-old.html',
    'index-v*.html', 'v[0-9].html',
    'about-final-v2.html',
    # Industry design exploration variants (keep only canonical 4)
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
    # Blog template (not a real page)
    '_TEMPLATE.html',
]

EXCLUDE_DIRS = {'.git', '.claude', '.github', 'audit', 'node_modules', 'scripts'}

SKIP_URL_PREFIXES = (
    'http://', 'https://', '//', 'mailto:', 'tel:',
    'data:', '#', 'javascript:',
)

OPEN_TAG_RE = re.compile(r'<footer\b[^>]*>', re.IGNORECASE)
CLOSE_TAG_RE = re.compile(r'</footer\s*>', re.IGNORECASE)
HREF_SRC_RE = re.compile(r'\b(href|src)=(["\'])([^"\']+)\2')


def extract_footer_span(html, start_pos=0):
    """Find first balanced <footer>...</footer> span. Returns (start, end) or (None, None)."""
    m = OPEN_TAG_RE.search(html, start_pos)
    if not m:
        return None, None
    span_start = m.start()
    pos = m.end()
    depth = 1
    while depth > 0:
        next_open = OPEN_TAG_RE.search(html, pos)
        next_close = CLOSE_TAG_RE.search(html, pos)
        if not next_close:
            return None, None
        if next_open and next_open.start() < next_close.start():
            depth += 1
            pos = next_open.end()
        else:
            depth -= 1
            pos = next_close.end()
            if depth == 0:
                return span_start, pos
    return None, None


def count_footer_tags(html):
    """Returns (open_count, close_count)."""
    return len(OPEN_TAG_RE.findall(html)), len(CLOSE_TAG_RE.findall(html))


def adjust_paths(footer_html, depth):
    """Prepend '../'*depth to relative href/src URLs. Skips absolute/special URLs."""
    if depth <= 0:
        return footer_html
    prefix = '../' * depth

    def replace(match):
        attr = match.group(1)
        quote = match.group(2)
        url = match.group(3)
        if url.startswith(SKIP_URL_PREFIXES):
            return match.group(0)
        return f'{attr}={quote}{prefix}{url}{quote}'

    return HREF_SRC_RE.sub(replace, footer_html)


def find_insertion_point(html):
    """Return byte offset where new footer should be inserted in a footer-less file."""
    # 1. After </main>
    m = re.search(r'</main\s*>\s*\n?', html, re.IGNORECASE)
    if m:
        return m.end()
    # 2. Before sticky CTA comment
    m = re.search(r'<!--\s*=+\s*STICKY BOTTOM CTA', html, re.IGNORECASE)
    if m:
        return m.start()
    # 3. Before first <script> in last 5000 chars (likely page-end scripts)
    last_chunk_start = max(0, len(html) - 5000)
    m = re.search(r'<script\b', html[last_chunk_start:], re.IGNORECASE)
    if m:
        return last_chunk_start + m.start()
    # 4. Before </body>
    m = re.search(r'</body\s*>', html, re.IGNORECASE)
    if m:
        return m.start()
    raise ValueError("Cannot find insertion point — file has no </main>, no sticky-cta, no <script>, no </body>")


def relative_path(path):
    """Path relative to repo root."""
    return path.relative_to(REPO_ROOT)


def compute_depth(path):
    """Number of subdirectories above the file (root files = 0)."""
    return len(relative_path(path).parts) - 1


def is_excluded(path):
    """Check if file matches any exclude pattern (filename only)."""
    name = path.name
    rel = str(relative_path(path))
    for pattern in EXCLUDE_PATTERNS:
        if fnmatch.fnmatch(name, pattern):
            return True
        if fnmatch.fnmatch(rel, pattern):
            return True
    return False


def collect_targets():
    """Walk repo for .html files, applying exclusions."""
    targets = []
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        # prune excluded dirs
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fn in filenames:
            if not fn.endswith('.html'):
                continue
            full = Path(dirpath) / fn
            if full == SOURCE_FILE:
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
    """Return one of: OK_HAS_FOOTER, ORPHAN_CLOSE, MISSING_BOTH, MULTIPLE, MISMATCH."""
    opens, closes = count_footer_tags(html)
    if opens == 1 and closes == 1:
        return 'OK_HAS_FOOTER'
    if opens == 0 and closes == 1:
        return 'ORPHAN_CLOSE'
    if opens == 0 and closes == 0:
        return 'MISSING_BOTH'
    if opens > 1 or closes > 1:
        return 'MULTIPLE'
    return 'MISMATCH'


def process_file(path, source_footer, dry_run=True):
    """Process one target file. Returns (action, message).

    action: 'changed', 'unchanged', 'aborted'
    """
    html = path.read_text(encoding='utf-8-sig')
    cat = categorize(html)
    depth = compute_depth(path)
    adjusted = adjust_paths(source_footer, depth)

    if cat in ('MULTIPLE', 'MISMATCH'):
        opens, closes = count_footer_tags(html)
        return 'aborted', f"{cat} (open={opens}, close={closes})"

    if cat == 'OK_HAS_FOOTER':
        s, e = extract_footer_span(html)
        if s is None:
            return 'aborted', "tag count says OK but span extraction failed"
        existing = html[s:e]
        if existing == adjusted:
            return 'unchanged', "footer already in sync"
        new_html = html[:s] + adjusted + html[e:]

    elif cat == 'ORPHAN_CLOSE':
        # Find and remove the orphan </footer>
        orphan = CLOSE_TAG_RE.search(html)
        if not orphan:
            return 'aborted', "ORPHAN_CLOSE category but no </footer> found"
        cleaned = html[:orphan.start()] + html[orphan.end():]
        # Insert new footer after </main>
        try:
            ins = find_insertion_point(cleaned)
        except ValueError as e:
            return 'aborted', str(e)
        # Use leading newline + 2-space indent for readability
        new_html = cleaned[:ins] + '  ' + adjusted + '\n\n' + cleaned[ins:]

    elif cat == 'MISSING_BOTH':
        try:
            ins = find_insertion_point(html)
        except ValueError as e:
            return 'aborted', str(e)
        new_html = html[:ins] + '  ' + adjusted + '\n\n' + html[ins:]

    else:
        return 'aborted', f"unknown category {cat}"

    if not dry_run:
        # Preserve trailing newline
        path.write_text(new_html, encoding='utf-8')

    return 'changed', cat


def verify_file(path):
    """Post-write verification. Returns list of error strings (empty = OK)."""
    errors = []
    html = path.read_text(encoding='utf-8-sig')
    opens, closes = count_footer_tags(html)
    if opens != 1 or closes != 1:
        errors.append(f"tag count: open={opens}, close={closes} (expected 1/1)")
        return errors

    s, e = extract_footer_span(html)
    if s is None:
        errors.append("footer span extraction failed")
        return errors

    # Check </main> position vs footer
    main_close = re.search(r'</main\s*>', html, re.IGNORECASE)
    if main_close and main_close.start() > s:
        errors.append(f"footer at byte {s} comes BEFORE </main> at byte {main_close.start()}")

    # Check footer is before </body>
    body_close = re.search(r'</body\s*>', html, re.IGNORECASE)
    if body_close and e > body_close.start():
        errors.append(f"footer ends after </body>")

    # Check end-of-file integrity (last 200 chars contain </body> and </html>)
    tail = html[-200:]
    if '</body>' not in tail:
        errors.append("</body> not in last 200 chars")
    if '</html>' not in tail:
        errors.append("</html> not in last 200 chars")

    return errors


def verify_links_sample(modified_files, sample_size=5):
    """Verify sample of modified files have no broken footer links."""
    import random
    sample = random.sample(modified_files, min(sample_size, len(modified_files)))
    broken = []
    for path in sample:
        html = path.read_text(encoding='utf-8-sig')
        s, e = extract_footer_span(html)
        if s is None:
            continue
        footer = html[s:e]
        for m in HREF_SRC_RE.finditer(footer):
            url = m.group(3)
            if url.startswith(SKIP_URL_PREFIXES):
                continue
            target = (path.parent / url).resolve()
            if not target.exists():
                broken.append(f"{relative_path(path)}: {url} → {target} (404)")
    return broken


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

    # Step 1: extract source footer
    source_html = SOURCE_FILE.read_text(encoding='utf-8-sig')
    s, e = extract_footer_span(source_html)
    if s is None:
        print(f"ERROR: could not extract <footer> from {SOURCE_FILE}", file=sys.stderr)
        return 1
    source_footer = source_html[s:e]
    print(f"✓ Extracted source footer from index.html ({len(source_footer)} bytes, {source_footer.count(chr(10))+1} lines)")

    # Step 2: collect targets
    if args.target:
        targets = [REPO_ROOT / args.target]
        if not targets[0].exists():
            print(f"ERROR: target not found: {targets[0]}", file=sys.stderr)
            return 1
    else:
        targets = collect_targets()
    print(f"✓ Collected {len(targets)} target files")

    # Step 3: pre-flight categorization
    categories = {'OK_HAS_FOOTER': [], 'ORPHAN_CLOSE': [], 'MISSING_BOTH': [],
                  'MULTIPLE': [], 'MISMATCH': []}
    for path in targets:
        try:
            html = path.read_text(encoding='utf-8-sig')
            cat = categorize(html)
            categories[cat].append(path)
        except Exception as ex:
            print(f"  ERROR reading {relative_path(path)}: {ex}", file=sys.stderr)

    print("\nPre-flight categorization:")
    for cat, files in categories.items():
        marker = ' ⚠' if cat in ('MULTIPLE', 'MISMATCH') else ''
        print(f"  {cat:20s}: {len(files):4d} files{marker}")

    if categories['MULTIPLE'] or categories['MISMATCH']:
        print("\n⚠ Files needing manual review:")
        for path in categories['MULTIPLE'] + categories['MISMATCH']:
            opens, closes = count_footer_tags(path.read_text(encoding='utf-8-sig'))
            print(f"    {relative_path(path)}  (open={opens}, close={closes})")

    if args.verify_only:
        print("\n--verify-only: checking current footer state...")
        all_errors = {}
        for path in categories['OK_HAS_FOOTER']:
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
        print(f"✓ All {len(categories['OK_HAS_FOOTER'])} files with footers verified OK")
        return 0

    # Step 4: process files
    print(f"\n{'APPLYING' if args.apply else 'DRY-RUN'}...")
    changed = []
    unchanged = []
    aborted = []
    for path in targets:
        cat = next((c for c, f in categories.items() if path in f), None)
        if cat in ('MULTIPLE', 'MISMATCH'):
            aborted.append((path, cat))
            continue
        try:
            action, msg = process_file(path, source_footer, dry_run=not args.apply)
            if action == 'changed':
                changed.append(path)
                if args.verbose:
                    print(f"  CHANGE  {relative_path(path)}  ({msg})")
            elif action == 'unchanged':
                unchanged.append(path)
            else:
                aborted.append((path, msg))
                print(f"  ABORT   {relative_path(path)}  ({msg})")
        except Exception as ex:
            aborted.append((path, str(ex)))
            print(f"  ERROR   {relative_path(path)}: {ex}", file=sys.stderr)

    # Group changes by directory for summary
    by_dir = {}
    for path in changed:
        d = relative_path(path).parts[0] if len(relative_path(path).parts) > 1 else '(root)'
        by_dir.setdefault(d, 0)
        by_dir[d] += 1

    print(f"\nSummary:")
    print(f"  Changed:   {len(changed)} files")
    for d, n in sorted(by_dir.items()):
        print(f"    {d}/: {n}")
    print(f"  Unchanged: {len(unchanged)} files (already in sync)")
    print(f"  Aborted:   {len(aborted)} files")

    # Step 5: post-write verification
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

        broken = verify_links_sample(changed, sample_size=5)
        if broken:
            print(f"\n⚠ Broken links in sampled files:")
            for b in broken:
                print(f"    {b}")
            return 1
        print(f"  ✓ Sample link resolution passed (5 files)")

    if args.apply:
        print(f"\nNext steps:")
        print(f"  git -C {REPO_ROOT} status")
        print(f"  git -C {REPO_ROOT} diff --stat | head -30")
        print(f"  git -C {REPO_ROOT} add -A && git -C {REPO_ROOT} commit -m 'Sync footer from index.html'")
        print(f"  git -C {REPO_ROOT} push origin main")
    else:
        print(f"\nDry-run complete. Re-run with --apply to write changes.")

    return 0 if not aborted else 1


if __name__ == '__main__':
    sys.exit(main())
