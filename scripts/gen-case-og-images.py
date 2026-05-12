#!/usr/bin/env python3
"""
Generate per-case OG images using V1 Big Number Hero template.
Writes HTML to og-per-case/, screenshots to og-previews/per-case/,
JPGs overwriting images/og/case-*.jpg.
"""
import os
import subprocess
import sys
from pathlib import Path
from PIL import Image

ROOT = Path("/Users/imac/SEO/command-center")
OG_HTML_DIR = ROOT / "og-per-case"
OG_PNG_DIR = ROOT / "og-previews" / "per-case"
OG_JPG_DIR = ROOT / "images" / "og"
OG_HTML_DIR.mkdir(parents=True, exist_ok=True)
OG_PNG_DIR.mkdir(parents=True, exist_ok=True)

CASES = [
    {
        "slug": "3x-in-28-days", "og": "case-3x-28days",
        "badge": "ახალი პროექტი · 28 დღე",
        "metric": "3×", "metric_size": 380,
        "kicker": "ტრაფიკი 28 დღეში",
        "title": "სამჯერ მეტი.",
        "bottom": "1,500+ clicks/თვე · ერთი keyword #1 პოზიციაზე",
    },
    {
        "slug": "trafikis-gaormageba-3-tveshi", "og": "case-2x-traffic",
        "badge": "სამშენებლო · 3 თვე",
        "metric": "×2", "metric_size": 380,
        "kicker": "ტრაფიკის გაორმაგება",
        "title": "ორჯერ მეტი ვიზიტი.",
        "bottom": "Keyword segmentation + keyword mapping",
    },
    {
        "slug": "250-percent-increase", "og": "case-250-percent",
        "badge": "სამშენებლო · 3 თვე",
        "metric": "+250%", "metric_size": 280,
        "kicker": "ორგანული ზრდა",
        "title": "სამ თვეში — 2.5×.",
        "bottom": "კონკურენტული keyword მიდგომა",
    },
    {
        "slug": "270-percent-increase", "og": "case-270-percent",
        "badge": "E-commerce · 3 თვე",
        "metric": "+270%", "metric_size": 280,
        "kicker": "ტრაფიკი + 45% გაყიდვა",
        "title": "Shopify-ის გადახედვა.",
        "bottom": "Meta + product page + CRO სტრუქტურა",
    },
    {
        "slug": "local-seo-result", "og": "case-local-seo",
        "badge": "Local SEO · 2 თვე",
        "metric": "+60%", "metric_size": 280,
        "kicker": "სატელეფონო ზარები",
        "title": "ლოკალურმა მუშაობა იცის.",
        "bottom": "GBP + ციტატები + ლოკალური სქემა",
    },
    {
        "slug": "4200-yoveltviuri-vizitori-4-tveshi", "og": "case-4200-visitors",
        "badge": "სამედიცინო · 4 თვე",
        "metric": "4,200+", "metric_size": 240,
        "kicker": "ვიზიტორი ყოველთვიურად",
        "title": "YMYL ნიშის ხსნა.",
        "bottom": "E-E-A-T სიგნალები + schema markup",
    },
    {
        "slug": "seo-krizisidan-top-3mde", "og": "case-crisis-top3",
        "badge": "B2B · 2 თვე",
        "metric": "TOP-3", "metric_size": 260,
        "kicker": "Google-ის რანკი",
        "title": "კრიზისიდან TOP-3-მდე.",
        "bottom": "disavow + on-page recovery + content rebuild",
    },
    {
        "slug": "seo-crisis-management", "og": "case-crisis-mgmt",
        "badge": "B2B · 2 თვე",
        "metric": "TOP-3", "metric_size": 260,
        "kicker": "Google-ის რანკი",
        "title": "კრიზისიდან TOP-3-მდე.",
        "bottom": "Spam links cleanup + technical recovery",
    },
    {
        "slug": "stomatologiuri-klinikis-seo", "og": "case-dental",
        "badge": "სტომატოლოგია · 6 თვე",
        "metric": "+600%", "metric_size": 280,
        "kicker": "6 თვეში — Google #1",
        "title": "1,600+ ვიზიტორი თვეში.",
        "bottom": "Schema · GBP · სერვის-სპეციფიური ლანდინგი",
    },
]

TEMPLATE = """<!DOCTYPE html>
<html lang="ka">
<head>
<meta charset="UTF-8">
<title>OG · {slug}</title>
<meta name="robots" content="noindex, nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ background: #1a1a1a; min-height: 100vh; display: flex; align-items: center; justify-content: center; font-family: 'Inter', sans-serif; }}
  .og {{
    width: 1200px; height: 630px; position: relative; overflow: hidden;
    background:
      radial-gradient(circle at 85% 50%, rgba(139,92,246,0.25) 0%, transparent 60%),
      radial-gradient(circle at 15% 80%, rgba(20,184,166,0.18) 0%, transparent 55%),
      linear-gradient(135deg, #020710 0%, #0a0a1a 100%);
    color: #fff; padding: 64px;
    display: flex; flex-direction: column; justify-content: space-between;
  }}
  .top {{ display: flex; justify-content: space-between; align-items: center; }}
  .logo {{ display: flex; align-items: center; gap: 12px; font-weight: 800; font-size: 28px; letter-spacing: -0.02em; }}
  .logo .x {{ background: linear-gradient(135deg, #8B5CF6, #14B8A6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
  .badge {{ padding: 10px 20px; background: rgba(139,92,246,0.18); border: 1px solid rgba(139,92,246,0.4); color: #c4b5fd; border-radius: 100px; font-size: 16px; font-weight: 600; letter-spacing: 0.02em; }}
  .hero {{ display: flex; flex-direction: column; align-items: center; text-align: center; gap: 12px; }}
  .num {{
    font-size: {metric_size}px; font-weight: 900; line-height: 0.9; letter-spacing: -0.06em;
    background: linear-gradient(180deg, #fff 0%, #a78bfa 60%, #14B8A6 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    text-shadow: 0 0 80px rgba(139,92,246,0.3);
  }}
  .label {{ text-align: center; }}
  .label .small {{ font-size: 16px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.18em; margin-bottom: 8px; }}
  .label .big {{ font-size: 38px; font-weight: 800; line-height: 1.1; letter-spacing: -0.03em; }}
  .bottom {{ display: flex; justify-content: space-between; align-items: end; }}
  .meta {{ font-size: 16px; color: #94a3b8; max-width: 720px; line-height: 1.45; }}
  .meta strong {{ color: #fff; font-weight: 700; }}
  .arrow {{ font-size: 24px; color: #8B5CF6; font-weight: 700; }}
</style>
</head>
<body>
<div class="og">
  <div class="top">
    <div class="logo">10×<span class="x">SEO</span></div>
    <div class="badge">⬢ {badge}</div>
  </div>
  <div class="hero">
    <div class="num">{metric}</div>
    <div class="label">
      <div class="small">{kicker}</div>
      <div class="big">{title}</div>
    </div>
  </div>
  <div class="bottom">
    <div class="meta">{bottom}</div>
    <div class="arrow">10xseo.ge →</div>
  </div>
</div>
</body>
</html>
"""

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def gen_html(case):
    html = TEMPLATE.format(**case)
    out = OG_HTML_DIR / f"{case['slug']}.html"
    out.write_text(html, encoding="utf-8")
    return out

def screenshot(html_path, out_png):
    subprocess.run([
        CHROME, "--headless", "--disable-gpu", "--no-sandbox",
        "--hide-scrollbars", "--window-size=1200,800",
        "--default-background-color=000000ff",
        f"--screenshot={out_png}",
        f"file://{html_path}",
    ], capture_output=True)

def crop_to_og(src_png, dst_png):
    img = Image.open(src_png)
    # detect og card top by scanning down
    start = 0
    for y in range(0, img.size[1]):
        px = img.getpixel((600, y))
        if abs(px[0]-26) > 5 or abs(px[1]-26) > 5 or abs(px[2]-26) > 5:
            start = y
            break
    cropped = img.crop((0, start, 1200, start + 630))
    cropped.save(dst_png, optimize=True)
    return cropped

def png_to_jpg(png_path, jpg_path):
    img = Image.open(png_path)
    rgb = Image.new("RGB", img.size, (2, 7, 16))
    if img.mode == "RGBA":
        rgb.paste(img, mask=img.split()[3])
    else:
        rgb.paste(img)
    rgb.save(jpg_path, "JPEG", quality=90, optimize=True, progressive=True)
    return os.path.getsize(jpg_path)

def main():
    print(f"Generating {len(CASES)} per-case OG images")
    print("=" * 70)
    for c in CASES:
        html = gen_html(c)
        raw_png = OG_PNG_DIR / f"_raw_{c['slug']}.png"
        screenshot(html, raw_png)
        final_png = OG_PNG_DIR / f"{c['og']}.png"
        crop_to_og(raw_png, final_png)
        raw_png.unlink()  # clean up raw
        jpg_path = OG_JPG_DIR / f"{c['og']}.jpg"
        size = png_to_jpg(final_png, jpg_path)
        print(f"  ✓ {c['slug']:40} → {c['og']}.jpg  ({size:>6,} bytes)")

if __name__ == "__main__":
    main()
