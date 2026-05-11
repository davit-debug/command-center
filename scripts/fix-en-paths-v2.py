#!/usr/bin/env python3
"""Extended path fixer: srcset, CSS url(), script/link refs to shared dirs."""
import re
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_DIR = ROOT / "en"

SHARED_DIRS = ('images/', 'fonts/', 'videos/', 'assets/', 'blog/', 'js/', 'css/')


def adjust_path(path: str, needed_prefix: str) -> str | None:
    """If path is relative and starts with a shared dir, return adjusted path. Else None."""
    if path.startswith(('http', '//', 'data:', '#', '/', '?', 'mailto:', 'tel:')):
        return None
    # Strip existing ../ prefixes
    m = re.match(r'((?:\.\./)*)', path)
    existing = m.group(1) if m else ''
    bare = path[len(existing):]
    for shared in SHARED_DIRS:
        if bare.startswith(shared):
            new_path = needed_prefix + bare
            if new_path != path:
                return new_path
            return None  # already correct
    return None


def fix_file(en_path: Path) -> int:
    rel = en_path.relative_to(EN_DIR)
    depth = len(rel.parts) - 1
    needed_prefix = '../' * (depth + 1)

    content = en_path.read_text(encoding='utf-8-sig')
    original = content
    fix_count = [0]

    # 1. srcset (can contain multiple comma-separated entries)
    def fix_srcset(m):
        attr_val = m.group(1)
        parts = []
        changed = False
        for part in attr_val.split(','):
            part = part.strip()
            tokens = part.split(' ', 1)
            src = tokens[0]
            rest = ' ' + tokens[1] if len(tokens) > 1 else ''
            new_src = adjust_path(src, needed_prefix)
            if new_src:
                src = new_src
                changed = True
            parts.append(src + rest)
        if changed:
            fix_count[0] += 1
        return 'srcset="' + ', '.join(parts) + '"'

    content = re.sub(r'\bsrcset="([^"]+)"', fix_srcset, content)

    # 2. CSS url() — supports url(path), url('path'), url("path")
    def fix_css_url(m):
        quote = m.group(1) or ''
        path = m.group(2)
        end_quote = m.group(3) or ''
        new_path = adjust_path(path, needed_prefix)
        if new_path:
            fix_count[0] += 1
            return f'url({quote}{new_path}{end_quote})'
        return m.group(0)

    content = re.sub(r"url\((['\"]?)([^'\"\)\s]+)(['\"]?)\)", fix_css_url, content)

    # 3. Generic attribute fix: src, href, poster, data-src on any HTML tag
    # (greedy [^>]* failed because it consumed past target attribute — use direct attr match)
    def fix_attr(m):
        attr = m.group(1)
        _quote = m.group(2)
        path = m.group(3)
        end = m.group(4)
        new_path = adjust_path(path, needed_prefix)
        if new_path:
            fix_count[0] += 1
            return f'{attr}={_quote}{new_path}{end}'
        return m.group(0)

    # Match each attr individually (not anchored to tag start)
    content = re.sub(r'\b(src|href|poster|data-src)=("|\')([^"\']+)("|\')',
                     fix_attr, content)

    if content != original:
        en_path.write_text(content, encoding='utf-8')
        print(f"  ✓ {rel}: {fix_count[0]} fixes")
    return fix_count[0]


def main():
    total = 0
    for f in sorted(EN_DIR.rglob("*.html")):
        total += fix_file(f)
    print(f"\nTotal path fixes: {total}")


if __name__ == "__main__":
    main()
