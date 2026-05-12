#!/usr/bin/env python3
"""
3-Phase QA for case-study OG images.

PHASE 1 — File validation:
  - all expected files exist
  - dimensions exactly 1200x630
  - file size in healthy range (5-300 KB)

PHASE 2 — Pixel analysis:
  - no body bleed-through at 4 corners (Chrome window bg ≠ card bg)
  - center of card has rendered content (variance > threshold)
  - top-left logo area + bottom-right CTA area have content

PHASE 3 — Content mapping:
  - each case-studies/*.html og:image points to expected file
  - referenced JPG exists on disk
  - og:image:width/height match actual file
  - filename consistency: slug ↔ og-filename mapping intact

Outputs PASS/FAIL/WARN per item and a summary report.
"""
import os, re, sys
from pathlib import Path
from PIL import Image
from collections import defaultdict

ROOT = Path("/Users/imac/SEO/command-center")
CASES_DIR = ROOT / "case-studies"
OG_JPG_DIR = ROOT / "images" / "og"
OG_PREV = ROOT / "og-previews" / "per-case"

# Slug → og-filename mapping (must match generator scripts + actual HTML meta tags)
SLUG_OG = {
    "3x-in-28-days":                       "case-3x-28days",
    "trafikis-gaormageba-3-tveshi":        "case-2x-traffic",
    "250-percent-increase":                "case-250-percent",
    "270-percent-increase":                "case-270-percent",
    "local-seo-result":                    "case-local-seo",
    "4200-yoveltviuri-vizitori-4-tveshi":  "case-4200-visitors",
    "seo-krizisidan-top-3mde":             "case-crisis-top3",
    "seo-crisis-management":               "case-crisis-mgmt",
    "stomatologiuri-klinikis-seo":         "case-dental",
}

# Expected metric per case (used in Phase 3 content sanity check via visual inspection note)
EXPECTED_METRIC = {
    "3x-in-28-days":                       "3×",
    "trafikis-gaormageba-3-tveshi":        "×2",
    "250-percent-increase":                "+250%",
    "270-percent-increase":                "+270%",
    "local-seo-result":                    "+60%",
    "4200-yoveltviuri-vizitori-4-tveshi":  "4,200+",
    "seo-krizisidan-top-3mde":             "TOP-3",
    "seo-crisis-management":               "TOP-3",
    "stomatologiuri-klinikis-seo":         "+600%",
}

VARIANTS = ["V1", "vA", "vB", "vC", "vD", "vE", "vF", "vG", "vH", "vI", "vJ", "vK", "vL", "vM"]

# Tracking
results = []  # [(phase, level, key, msg)]
counters = defaultdict(int)

C = {"R":"\033[31m","G":"\033[32m","Y":"\033[33m","B":"\033[34m","M":"\033[35m","X":"\033[0m","BOLD":"\033[1m","DIM":"\033[2m"}

def log(phase, level, key, msg):
    counters[level] += 1
    color = {"PASS":C["G"], "WARN":C["Y"], "FAIL":C["R"]}.get(level, "")
    print(f"  {color}[{level:4}]{C['X']} {key}: {msg}")
    results.append((phase, level, key, msg))

def get_variant_path(case_slug, og_name, variant):
    """Path to the preview JPG for given case + variant."""
    if variant == "V1":
        return OG_PREV / f"{og_name}.jpg"
    return OG_PREV / variant / f"{og_name}.jpg"

def get_production_jpg(og_name):
    return OG_JPG_DIR / f"{og_name}.jpg"

# ============== PHASE 1: FILE VALIDATION ==============
def phase1():
    print(f"\n{C['BOLD']}{C['M']}━━━ PHASE 1 · FILE VALIDATION ━━━{C['X']}")
    print(f"{C['DIM']}Check: existence, dimensions (1200×630), file size (5-300 KB){C['X']}\n")
    for slug, og_name in SLUG_OG.items():
        for variant in VARIANTS:
            p = get_variant_path(slug, og_name, variant)
            key = f"{variant:3} · {og_name}"
            if not p.exists():
                log(1, "FAIL", key, f"missing: {p.relative_to(ROOT)}")
                continue
            try:
                img = Image.open(p)
                w, h = img.size
                size_kb = p.stat().st_size / 1024
                if (w, h) != (1200, 630):
                    log(1, "FAIL", key, f"dim {w}×{h} ≠ 1200×630")
                elif size_kb > 300:
                    log(1, "WARN", key, f"size {size_kb:.0f} KB > 300 KB (heavy)")
                elif size_kb < 5:
                    log(1, "FAIL", key, f"size {size_kb:.1f} KB < 5 KB (likely broken)")
                else:
                    log(1, "PASS", key, f"{w}×{h}, {size_kb:.0f} KB")
            except Exception as e:
                log(1, "FAIL", key, f"open error: {e}")
        # Production JPG
        jp = get_production_jpg(og_name)
        if not jp.exists():
            log(1, "FAIL", f"JPG · {og_name}", f"missing: {jp.relative_to(ROOT)}")
        else:
            img = Image.open(jp)
            w, h = img.size
            size_kb = jp.stat().st_size / 1024
            if (w, h) != (1200, 630):
                log(1, "FAIL", f"JPG · {og_name}", f"dim {w}×{h} ≠ 1200×630")
            elif size_kb > 300:
                log(1, "WARN", f"JPG · {og_name}", f"size {size_kb:.0f} KB > 300 KB")
            else:
                log(1, "PASS", f"JPG · {og_name}", f"{w}×{h}, {size_kb:.0f} KB JPEG")

# ============== PHASE 2: PIXEL ANALYSIS ==============
BODY_BG = (26, 26, 26)  # Chrome headless body bg
BODY_TOL = 6

def is_body_bg(px):
    return all(abs(px[i] - BODY_BG[i]) <= BODY_TOL for i in range(3))

def pixel_variance(img, region):
    """Return color variance of a region (higher = more content). region=(x,y,w,h)."""
    x, y, w, h = region
    pixels = []
    for px_x in range(x, x+w, max(1, w//30)):
        for px_y in range(y, y+h, max(1, h//30)):
            pixels.append(img.getpixel((px_x, px_y)))
    # Variance approximation: max-min of luminance
    lums = [0.299*p[0]+0.587*p[1]+0.114*p[2] for p in pixels]
    return max(lums) - min(lums)

def phase2():
    print(f"\n{C['BOLD']}{C['M']}━━━ PHASE 2 · PIXEL ANALYSIS ━━━{C['X']}")
    print(f"{C['DIM']}Check: no body bleed, 4 zones have content (logo/badge/metric/CTA){C['X']}\n")
    for slug, og_name in SLUG_OG.items():
        for variant in VARIANTS:
            p = get_variant_path(slug, og_name, variant)
            key = f"{variant:3} · {og_name}"
            if not p.exists():
                continue
            img = Image.open(p).convert("RGB")
            issues = []
            # 1. Check 4 corners — should NOT be body bg
            for cx, cy, name in [(2,2,"TL"), (1197,2,"TR"), (2,627,"BL"), (1197,627,"BR")]:
                px = img.getpixel((cx, cy))
                if is_body_bg(px):
                    issues.append(f"body bleed @ {name}")
            # 2. Logo region (top-left, x=48-150, y=40-100) — should have content
            logo_var = pixel_variance(img, (48, 40, 200, 80))
            if logo_var < 30:
                issues.append(f"logo zone low contrast ({logo_var:.0f})")
            # 3. Center metric region (x=350-850, y=200-450)
            metric_var = pixel_variance(img, (350, 200, 500, 250))
            if metric_var < 60:
                issues.append(f"metric zone too uniform ({metric_var:.0f})")
            # 4. Bottom area (CTA/meta, y=540-625)
            bottom_var = pixel_variance(img, (50, 540, 1100, 80))
            if bottom_var < 30:
                issues.append(f"bottom zone too uniform ({bottom_var:.0f})")
            if issues:
                log(2, "WARN", key, "; ".join(issues))
            else:
                log(2, "PASS", key, f"logo={logo_var:.0f} metric={metric_var:.0f} bottom={bottom_var:.0f}")

# ============== PHASE 3: CONTENT MAPPING ==============
META_RE = re.compile(r'<meta\s+property="og:image"\s+content="([^"]+)"', re.IGNORECASE)
META_W_RE = re.compile(r'<meta\s+property="og:image:width"\s+content="([^"]+)"', re.IGNORECASE)
META_H_RE = re.compile(r'<meta\s+property="og:image:height"\s+content="([^"]+)"', re.IGNORECASE)

def phase3():
    print(f"\n{C['BOLD']}{C['M']}━━━ PHASE 3 · CONTENT MAPPING ━━━{C['X']}")
    print(f"{C['DIM']}Check: HTML og:image meta tag → expected JPG file → exists on disk{C['X']}\n")
    for slug, og_name in SLUG_OG.items():
        html = CASES_DIR / f"{slug}.html"
        key = f"meta · {slug[:35]}"
        if not html.exists():
            log(3, "FAIL", key, f"HTML not found: case-studies/{slug}.html")
            continue
        content = html.read_text(encoding="utf-8")
        m = META_RE.search(content)
        if not m:
            log(3, "FAIL", key, "no og:image meta tag")
            continue
        og_url = m.group(1)
        expected = f"https://10xseo.ge/images/og/{og_name}.jpg"
        if og_url != expected:
            log(3, "FAIL", key, f"meta points to {og_url}, expected {expected}")
            continue
        # Check width/height meta
        mw = META_W_RE.search(content)
        mh = META_H_RE.search(content)
        if not mw or not mh:
            log(3, "WARN", key, "og:image:width or og:image:height missing")
            continue
        if mw.group(1) != "1200" or mh.group(1) != "630":
            log(3, "FAIL", key, f"meta dims {mw.group(1)}×{mh.group(1)} ≠ 1200×630")
            continue
        # JPG exists
        jp = get_production_jpg(og_name)
        if not jp.exists():
            log(3, "FAIL", key, f"referenced JPG missing on disk")
            continue
        log(3, "PASS", key, f"meta ↔ {og_name}.jpg ↔ disk all aligned")

def summary():
    print(f"\n{C['BOLD']}{C['M']}━━━ SUMMARY ━━━{C['X']}")
    total = sum(counters.values())
    print(f"  Total checks: {total}")
    print(f"  {C['G']}PASS:{C['X']} {counters['PASS']}")
    print(f"  {C['Y']}WARN:{C['X']} {counters['WARN']}")
    print(f"  {C['R']}FAIL:{C['X']} {counters['FAIL']}")
    # Per-phase
    phases_counts = defaultdict(lambda: defaultdict(int))
    for ph, lvl, _, _ in results:
        phases_counts[ph][lvl] += 1
    print()
    for ph in [1, 2, 3]:
        c = phases_counts[ph]
        line = f"  Phase {ph}: PASS={c['PASS']:3} WARN={c['WARN']:3} FAIL={c['FAIL']:3}"
        print(line)
    print()
    if counters['FAIL'] == 0 and counters['WARN'] == 0:
        print(f"  {C['G']}{C['BOLD']}✓ All clean — 100% pass.{C['X']}")
        return 0
    elif counters['FAIL'] == 0:
        print(f"  {C['Y']}⚠ {counters['WARN']} warnings, no failures.{C['X']}")
        return 0
    else:
        print(f"  {C['R']}✗ {counters['FAIL']} failures.{C['X']}")
        return 1

def main():
    phase1()
    phase2()
    phase3()
    return summary()

if __name__ == "__main__":
    sys.exit(main())
