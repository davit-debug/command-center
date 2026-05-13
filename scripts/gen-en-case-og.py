#!/usr/bin/env python3
"""Generate EN versions of case study OG images using F Cinematic template."""
import importlib.util
import subprocess
from pathlib import Path
from PIL import Image

ROOT = Path("/Users/imac/SEO/command-center")
OUT_DIR = ROOT / "images" / "og"
TEMP_DIR = ROOT / "og-en-case-temp"
TEMP_DIR.mkdir(parents=True, exist_ok=True)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Load F Cinematic template
spec = importlib.util.spec_from_file_location("dh", ROOT / "scripts" / "gen-case-og-variants-DH.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
TPL_F = mod.TPL_F

# EN case data — all 10 cases with English text
CASES_EN = [
    {"slug":"3x-in-28-days","og":"case-3x-28days-en","industry":"NEW PROJECT","metric":"3×","metric_size":380,"tf":"28 DAYS","year":"2024","kicker":"TRAFFIC IN 28 DAYS","title":"3× MORE.","bottom":"1,500+ clicks/month · #1 position"},
    {"slug":"trafikis-gaormageba-3-tveshi","og":"case-2x-traffic-en","industry":"CONSTRUCTION","metric":"×2","metric_size":380,"tf":"3 MONTHS","year":"2025","kicker":"TRAFFIC DOUBLED","title":"2× MORE VISITORS.","bottom":"Keyword Segmentation + Mapping"},
    {"slug":"250-percent-increase","og":"case-250-percent-en","industry":"CONSTRUCTION","metric":"+250%","metric_size":280,"tf":"3 MONTHS","year":"2025","kicker":"ORGANIC GROWTH","title":"2.5× IN 3 MONTHS.","bottom":"Competitive keyword strategy"},
    {"slug":"270-percent-increase","og":"case-270-percent-en","industry":"E-COMMERCE","metric":"+270%","metric_size":280,"tf":"3 MONTHS","year":"2025","kicker":"TRAFFIC + 45% SALES","title":"SHOPIFY REBUILD.","bottom":"Meta + product + CRO"},
    {"slug":"local-seo-result","og":"case-local-seo-en","industry":"LOCAL SEO","metric":"+60%","metric_size":280,"tf":"2 MONTHS","year":"2025","kicker":"PHONE CALLS","title":"LOCAL WORKS.","bottom":"GBP + Citations + Schema"},
    {"slug":"4200-yoveltviuri-vizitori-4-tveshi","og":"case-4200-visitors-en","industry":"HEALTHCARE","metric":"4,200+","metric_size":240,"tf":"4 MONTHS","year":"2025","kicker":"MONTHLY VISITORS","title":"YMYL NICHE WIN.","bottom":"E-E-A-T signals + schema markup"},
    {"slug":"seo-krizisidan-top-3mde","og":"case-crisis-top3-en","industry":"B2B","metric":"TOP-3","metric_size":260,"tf":"2 MONTHS","year":"2025","kicker":"GOOGLE RANKING","title":"FROM CRISIS TO TOP-3.","bottom":"Disavow + Recovery + Content rebuild"},
    {"slug":"seo-crisis-management","og":"case-crisis-mgmt-en","industry":"B2B","metric":"TOP-3","metric_size":260,"tf":"2 MONTHS","year":"2025","kicker":"GOOGLE RANKING","title":"FROM CRISIS TO TOP-3.","bottom":"Spam Cleanup + Technical Recovery"},
    {"slug":"stomatologiuri-klinikis-seo","og":"case-dental-en","industry":"DENTAL","metric":"+600%","metric_size":280,"tf":"6 MONTHS","year":"2026","kicker":"6 MONTHS — GOOGLE #1","title":"1,600+ VISITORS / MONTH.","bottom":"Schema · GBP · Service-specific landing"},
    {"slug":"318-percent-uk-shopify","og":"case-318-percent-uk-shopify-en","industry":"E-COMMERCE · UK","metric":"+318%","metric_size":280,"tf":"6 MONTHS","year":"2025","kicker":"CLICKS IN 6 MONTHS","title":"SHOPIFY · UK MARKET.","bottom":"1ClickBlinds — Search Console verified"},
]

def gen_one(c):
    html = TPL_F.format(**c)
    html_path = TEMP_DIR / f"{c['slug']}.html"
    html_path.write_text(html, encoding="utf-8")
    raw = TEMP_DIR / f"_raw_{c['slug']}.png"
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--hide-scrollbars", "--window-size=1200,800",
                    "--default-background-color=000000ff",
                    f"--screenshot={raw}", f"file://{html_path}"],
                   capture_output=True)
    img = Image.open(raw).convert("RGB")
    body = (26, 26, 26); start = 0
    for y in range(img.size[1]):
        if any(abs(img.getpixel((600,y))[i]-body[i])>5 for i in range(3)):
            start = y; break
    cropped = img.crop((0, start, 1200, start+630))
    out = OUT_DIR / f"{c['og']}.jpg"
    cropped.save(out, "JPEG", quality=90, optimize=True, progressive=True)
    raw.unlink()
    import os
    return os.path.getsize(out)

def main():
    print(f"Generating {len(CASES_EN)} EN case OG images (F Cinematic, English)")
    print("=" * 70)
    for c in CASES_EN:
        size = gen_one(c)
        print(f"  ✓ {c['og']:35} ({size/1024:.0f} KB)  — {c['metric']} · {c['title']}")
    import shutil; shutil.rmtree(TEMP_DIR)

if __name__ == "__main__":
    main()
