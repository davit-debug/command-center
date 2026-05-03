#!/usr/bin/env python3
"""Phase 1: structural verification of V29 FAQ on all patched pages."""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent

PAGES = [
    # Live production pages only (allowlisted in .gitignore)
    'index.html',
    'seo-audit.html', 'seo-management.html', 'seo-consultation.html',
    'seo-course.html', 'seo-copywriting.html', 'copywriting.html',
    'cro.html', 'google-ads.html', 'ai-seo.html',
    'offer-premium.html', 'offer-premium-convert.html', 'offer-premium-brand.html',
    # Disabled pages excluded: keyword-research, roi-calculator, offer
]

CHECKS = [
    ('id="v29-items"',     'v29-items div'),
    ('id="v29-more-btn"',  'see-more button'),
    ('id="v29-more-wrap"', 'see-more wrapper'),
    ('var faqData',        'faqData JS array'),
    ('.v29-card',          'V29 CSS'),
    ('.v29-more-btn',      'see-more CSS'),
    ('INITIAL=6',          'INITIAL=6 constant'),
    ('#D4A017',            'gold accent color'),
    ('rgba(139,92,246',    'violet accent (button)'),
    ('rgba(212,160,23',    'gold glassmorphism'),
    (re.compile(r'expanded\s*=\s*!\s*expanded'), 'toggle expand/collapse'),
    ('v29-extra-hidden',   'hidden-remainder class'),
]

def main():
    print(f"{'page':<35} {'Qs':>4}  status")
    print("-" * 90)
    all_ok = True
    for page in PAGES:
        path = ROOT / page
        if not path.exists():
            print(f"{page:<35}   --  NOT FOUND")
            all_ok = False
            continue
        text = path.read_text(encoding='utf-8')

        # Count questions
        m = re.search(r'var faqData\s*=\s*\[(.*?)\];', text, re.DOTALL)
        if m:
            qs = len(re.findall(r'q\s*:\s*"', m.group(1)))
        else:
            qs = 0

        missing = []
        for needle, name in CHECKS:
            if hasattr(needle, 'search'):
                if not needle.search(text):
                    missing.append(name)
            else:
                if needle not in text:
                    missing.append(name)
        if missing:
            print(f"{page:<35} {qs:>4}  MISSING: {', '.join(missing)}")
            all_ok = False
        else:
            # Extra: confirm only ONE FAQ section
            faq_count = text.count('<!-- ========== FAQ — V29 Gold Glassmorphism')
            if faq_count > 1:
                print(f"{page:<35} {qs:>4}  WARN: {faq_count} V29 banners")
                all_ok = False
            else:
                btn_msg = "" if qs > 6 else "(no btn — Qs ≤ 6)"
                print(f"{page:<35} {qs:>4}  OK {btn_msg}")

    print("-" * 90)
    print("ALL CHECKS PASSED" if all_ok else "SOME CHECKS FAILED")
    return 0 if all_ok else 1

if __name__ == '__main__':
    raise SystemExit(main())
