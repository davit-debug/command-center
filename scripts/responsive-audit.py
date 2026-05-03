#!/usr/bin/env python3
"""
Responsive Audit — Playwright orchestrator for 10xseo.ge

Runs each production page through 5 viewports, captures full-page screenshots,
runs axe-core a11y, console errors, layout shift, overflow + touch-target checks.

Outputs:
  audit/responsive/screenshots/{page}/{viewport}.png
  audit/responsive/data/{page}.json
  audit/responsive/report.html

Usage:
  audit/.venv/bin/python scripts/responsive-audit.py            # all 30 pages
  audit/.venv/bin/python scripts/responsive-audit.py --target index.html
  audit/.venv/bin/python scripts/responsive-audit.py --quick    # 1 viewport for smoke test
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT = REPO_ROOT / 'audit' / 'responsive'
SCREENSHOTS = OUTPUT / 'screenshots'
DATA = OUTPUT / 'data'
SERVER = 'http://localhost:8090'

# ────────────────────────────────────────────────────────────
# 30 production pages (the canonical launch surface)
# ────────────────────────────────────────────────────────────
PRODUCTION_PAGES = [
    'index.html',
    '404.html',
    'about-us.html',
    'services.html',
    'contact-us.html',
    'portfolio.html',
    'why-10xseo.html',
    'case-studies.html',
    'blog.html',
    'faq.html',
    'vacancies.html',
    'seo-management.html',
    'seo-consultation.html',
    'seo-strategy.html',
    'seo-copywriting.html',
    'seo-audit.html',
    'cro.html',
    'google-ads.html',
    'ai-seo.html',
    'seo-course.html',
    'seo-tools.html',
    'keyword-research.html',
    'copywriting.html',
    'ra-aris-seo.html',
    'seo-leqsikoni.html',
    'industries/construction.html',
    'industries/ecommerce.html',
    'industries/healthcare.html',
    'industries/financial-services.html',
    'blog/local-seo.html',
]

# 5 viewport profiles (real device baselines)
VIEWPORTS = [
    {'name': 'mobile-sm',  'width':  375, 'height':  667, 'device': 'iPhone SE'},
    {'name': 'mobile-md',  'width':  393, 'height':  852, 'device': 'iPhone 14 Pro'},
    {'name': 'tablet',     'width':  768, 'height': 1024, 'device': 'iPad mini'},
    {'name': 'laptop',     'width': 1280, 'height':  800, 'device': 'MacBook 13"'},
    {'name': 'desktop',    'width': 1920, 'height': 1080, 'device': 'Desktop FHD'},
]

AXE_CDN = 'https://cdn.jsdelivr.net/npm/axe-core@4.10.2/axe.min.js'

# ────────────────────────────────────────────────────────────
# Per-page audit
# ────────────────────────────────────────────────────────────
def audit_page(playwright, page_path, viewports, verbose=True):
    """Audit one page across all viewports. Returns dict of findings."""
    chromium = playwright.chromium
    browser = chromium.launch(headless=True)
    findings = {
        'page': page_path,
        'url': f'{SERVER}/{page_path}',
        'viewports': {},
    }

    safe_name = page_path.replace('/', '__').replace('.html', '')
    page_screenshots_dir = SCREENSHOTS / safe_name
    page_screenshots_dir.mkdir(parents=True, exist_ok=True)

    for vp in viewports:
        if verbose:
            print(f"  [{vp['name']:9s}] {vp['width']}×{vp['height']}", end=' ', flush=True)
        ctx = browser.new_context(
            viewport={'width': vp['width'], 'height': vp['height']},
            device_scale_factor=2,
            is_mobile=vp['width'] < 768,
            has_touch=vp['width'] < 1024,
            user_agent='Mozilla/5.0 (compatible; ResponsiveAudit/1.0)',
        )
        page = ctx.new_page()

        console_errors = []
        page.on('console', lambda msg: console_errors.append({'type': msg.type, 'text': msg.text})
                if msg.type in ('error', 'warning') else None)
        page_errors = []
        page.on('pageerror', lambda exc: page_errors.append(str(exc)))

        v_data = {
            'console_errors': console_errors,
            'page_errors': page_errors,
        }

        try:
            t0 = time.time()
            page.goto(f'{SERVER}/{page_path}', wait_until='networkidle', timeout=30000)
            v_data['load_ms'] = int((time.time() - t0) * 1000)

            # Settle animations
            page.wait_for_timeout(800)

            # ── Layout / overflow checks ──────────────────────────────
            metrics = page.evaluate('''() => {
                const html = document.documentElement;
                const body = document.body;
                return {
                    scrollWidth: html.scrollWidth,
                    clientWidth: html.clientWidth,
                    bodyScrollWidth: body.scrollWidth,
                    bodyClientWidth: body.clientWidth,
                    scrollHeight: html.scrollHeight,
                    clientHeight: html.clientHeight,
                };
            }''')
            v_data['metrics'] = metrics
            v_data['has_horizontal_overflow'] = metrics['scrollWidth'] > metrics['clientWidth'] + 1

            # ── Find elements that overflow viewport horizontally ────
            overflow_elements = page.evaluate('''(vw) => {
                const out = [];
                const all = document.querySelectorAll('body *');
                for (const el of all) {
                    const rect = el.getBoundingClientRect();
                    if (rect.right > vw + 2 && rect.width > 20) {
                        const tag = el.tagName.toLowerCase();
                        const cls = (el.className && typeof el.className === 'string') ? el.className.slice(0, 60) : '';
                        const id = el.id || '';
                        out.push({ tag, cls, id, x: Math.round(rect.left), w: Math.round(rect.width), right: Math.round(rect.right) });
                        if (out.length >= 8) break;
                    }
                }
                return out;
            }''', vp['width'])
            v_data['overflow_elements'] = overflow_elements

            # ── Touch target audit (interactive elements < 44px) ────
            if vp['width'] < 768:
                touch_targets = page.evaluate('''() => {
                    const out = [];
                    const sel = 'a, button, input[type="button"], input[type="submit"], [role="button"], [onclick]';
                    const all = document.querySelectorAll(sel);
                    for (const el of all) {
                        const rect = el.getBoundingClientRect();
                        if (rect.width === 0 || rect.height === 0) continue;
                        const minSide = Math.min(rect.width, rect.height);
                        if (minSide < 44) {
                            const tag = el.tagName.toLowerCase();
                            const text = (el.innerText || el.value || el.getAttribute('aria-label') || '').slice(0, 40);
                            out.push({ tag, text, w: Math.round(rect.width), h: Math.round(rect.height) });
                            if (out.length >= 12) break;
                        }
                    }
                    return out;
                }''')
                v_data['touch_targets_under_44px'] = touch_targets

            # ── Cumulative Layout Shift on scroll ────────────────────
            cls_value = page.evaluate('''async () => {
                let cls = 0;
                const obs = new PerformanceObserver(list => {
                    for (const e of list.getEntries()) {
                        if (!e.hadRecentInput) cls += e.value;
                    }
                });
                obs.observe({ type: 'layout-shift', buffered: true });
                window.scrollTo(0, document.body.scrollHeight / 2);
                await new Promise(r => setTimeout(r, 600));
                window.scrollTo(0, document.body.scrollHeight);
                await new Promise(r => setTimeout(r, 600));
                window.scrollTo(0, 0);
                await new Promise(r => setTimeout(r, 400));
                obs.disconnect();
                return Number(cls.toFixed(4));
            }''')
            v_data['cls'] = cls_value

            # ── axe-core a11y ────────────────────────────────────────
            try:
                page.add_script_tag(url=AXE_CDN)
                axe = page.evaluate('''async () => {
                    const r = await axe.run(document, {
                        runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21aa'] }
                    });
                    return r.violations.map(v => ({
                        id: v.id,
                        impact: v.impact,
                        help: v.help,
                        description: v.description,
                        nodes: v.nodes.length,
                        sample: v.nodes.slice(0, 2).map(n => ({
                            html: n.html.slice(0, 200),
                            target: n.target,
                            failureSummary: (n.failureSummary || '').slice(0, 200),
                        })),
                    }));
                }''')
                v_data['axe_violations'] = axe
            except Exception as ex:
                v_data['axe_error'] = str(ex)

            # ── Screenshot ───────────────────────────────────────────
            shot_path = page_screenshots_dir / f"{vp['name']}.png"
            page.screenshot(path=str(shot_path), full_page=True)
            v_data['screenshot'] = str(shot_path.relative_to(OUTPUT))

            if verbose:
                axe_count = len(v_data.get('axe_violations', []))
                ovf = '⚠OVF' if v_data.get('has_horizontal_overflow') else '   '
                touch = len(v_data.get('touch_targets_under_44px', []))
                cls_warn = '⚠CLS' if cls_value > 0.1 else '   '
                touch_warn = f'⚠T{touch}' if touch > 0 else '    '
                print(f"  axe={axe_count:2d}  CLS={cls_value:.3f}{cls_warn}  {ovf}  {touch_warn}  ({v_data['load_ms']}ms)")

        except Exception as ex:
            v_data['error'] = str(ex)
            if verbose:
                print(f"  ✗ ERROR: {ex}")

        findings['viewports'][vp['name']] = v_data
        ctx.close()

    browser.close()
    return findings


# ────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', help='Single page (relative path)')
    parser.add_argument('--quick', action='store_true', help='Only mobile-sm viewport')
    parser.add_argument('--limit', type=int, help='Limit number of pages')
    args = parser.parse_args()

    SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)

    pages = [args.target] if args.target else PRODUCTION_PAGES
    if args.limit:
        pages = pages[:args.limit]
    viewports = [VIEWPORTS[0]] if args.quick else VIEWPORTS

    print(f"Audit: {len(pages)} pages × {len(viewports)} viewports = {len(pages)*len(viewports)} runs")
    print(f"Output: {OUTPUT.relative_to(REPO_ROOT)}/")
    print()

    t_start = time.time()
    all_findings = []
    with sync_playwright() as pw:
        for i, page_path in enumerate(pages, 1):
            print(f"[{i:2d}/{len(pages)}] {page_path}")
            findings = audit_page(pw, page_path, viewports)
            all_findings.append(findings)

            # Save per-page JSON
            safe_name = page_path.replace('/', '__').replace('.html', '')
            with open(DATA / f'{safe_name}.json', 'w', encoding='utf-8') as f:
                json.dump(findings, f, ensure_ascii=False, indent=2)

    elapsed = int(time.time() - t_start)
    print(f"\n✓ Done in {elapsed//60}m {elapsed%60}s")
    print(f"Run: python3 scripts/responsive-report.py  to generate HTML dashboard")

    # Save aggregate
    with open(OUTPUT / 'all-findings.json', 'w', encoding='utf-8') as f:
        json.dump({'pages': all_findings, 'elapsed_sec': elapsed}, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    sys.exit(main())
