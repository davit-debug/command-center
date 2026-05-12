#!/usr/bin/env python3
"""
Generate 3 ADDITIONAL design variants per case study (A=Split, B=Chart, C=Editorial).
Output: og-previews/per-case/v{A,B,C}/case-{slug}.png (1200x630).
Does NOT overwrite the V1 JPGs in images/og/.
"""
import os
import subprocess
from pathlib import Path
from PIL import Image

ROOT = Path("/Users/imac/SEO/command-center")
HTML_BASE = ROOT / "og-per-case"
PNG_BASE = ROOT / "og-previews" / "per-case"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

for v in ["vA", "vB", "vC"]:
    (HTML_BASE / v).mkdir(parents=True, exist_ok=True)
    (PNG_BASE / v).mkdir(parents=True, exist_ok=True)

CASES = [
    {"slug": "3x-in-28-days", "og": "case-3x-28days", "industry": "ახალი პროექტი",
     "metric": "3×", "metric_size": 380, "tf": "28 დღე", "year": "2024",
     "kicker": "ტრაფიკი 28 დღეში", "title": "სამჯერ მეტი.",
     "bottom": "1,500+ clicks/თვე · #1 პოზიცია", "chapter": "I"},
    {"slug": "trafikis-gaormageba-3-tveshi", "og": "case-2x-traffic", "industry": "სამშენებლო",
     "metric": "×2", "metric_size": 380, "tf": "3 თვე", "year": "2025",
     "kicker": "ტრაფიკის გაორმაგება", "title": "ორჯერ მეტი ვიზიტი.",
     "bottom": "Keyword segmentation + mapping", "chapter": "II"},
    {"slug": "250-percent-increase", "og": "case-250-percent", "industry": "სამშენებლო",
     "metric": "+250%", "metric_size": 280, "tf": "3 თვე", "year": "2025",
     "kicker": "ორგანული ზრდა", "title": "სამ თვეში — 2.5×.",
     "bottom": "კონკურენტული keyword მიდგომა", "chapter": "III"},
    {"slug": "270-percent-increase", "og": "case-270-percent", "industry": "E-commerce",
     "metric": "+270%", "metric_size": 280, "tf": "3 თვე", "year": "2025",
     "kicker": "ტრაფიკი + 45% გაყიდვა", "title": "Shopify-ის გადახედვა.",
     "bottom": "Meta + product + CRO", "chapter": "IV"},
    {"slug": "local-seo-result", "og": "case-local-seo", "industry": "Local SEO",
     "metric": "+60%", "metric_size": 280, "tf": "2 თვე", "year": "2025",
     "kicker": "სატელეფონო ზარები", "title": "ლოკალურმა მუშაობა იცის.",
     "bottom": "GBP + ციტატები + სქემა", "chapter": "V"},
    {"slug": "4200-yoveltviuri-vizitori-4-tveshi", "og": "case-4200-visitors", "industry": "სამედიცინო",
     "metric": "4,200+", "metric_size": 240, "tf": "4 თვე", "year": "2025",
     "kicker": "ვიზიტორი თვეში", "title": "YMYL ნიშის ხსნა.",
     "bottom": "E-E-A-T + schema markup", "chapter": "VI"},
    {"slug": "seo-krizisidan-top-3mde", "og": "case-crisis-top3", "industry": "B2B",
     "metric": "TOP-3", "metric_size": 260, "tf": "2 თვე", "year": "2025",
     "kicker": "Google-ის რანკი", "title": "კრიზისიდან TOP-3-მდე.",
     "bottom": "disavow + recovery + content", "chapter": "VII"},
    {"slug": "seo-crisis-management", "og": "case-crisis-mgmt", "industry": "B2B",
     "metric": "TOP-3", "metric_size": 260, "tf": "2 თვე", "year": "2025",
     "kicker": "Google-ის რანკი", "title": "კრიზისიდან TOP-3-მდე.",
     "bottom": "Spam cleanup + technical recovery", "chapter": "VII"},
    {"slug": "stomatologiuri-klinikis-seo", "og": "case-dental", "industry": "სტომატოლოგია",
     "metric": "+600%", "metric_size": 280, "tf": "6 თვე", "year": "2026",
     "kicker": "6 თვეში — Google #1", "title": "1,600+ ვიზიტორი თვეში.",
     "bottom": "Schema · GBP · ლანდინგი", "chapter": "VIII"},
]

# ============== Template A: SPLIT LAYOUT ==============
TPL_A = """<!DOCTYPE html>
<html lang="ka">
<head>
<meta charset="UTF-8">
<title>OG A · {slug}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ background: #1a1a1a; min-height: 100vh; display: flex; align-items: center; justify-content: center; font-family: 'Inter', sans-serif; }}
  .og {{
    width: 1200px; height: 630px; position: relative; overflow: hidden;
    background: #020710; color: #fff;
    display: grid; grid-template-columns: 540px 1fr;
  }}
  .left {{
    background:
      radial-gradient(ellipse at 30% 80%, rgba(20,184,166,0.18) 0%, transparent 60%),
      linear-gradient(160deg, #0a0a1a 0%, #020710 100%);
    padding: 56px 48px;
    display: flex; flex-direction: column; justify-content: space-between;
    border-right: 1px solid rgba(255,255,255,0.08);
  }}
  .logo {{ font-weight: 800; font-size: 26px; letter-spacing: -0.02em; }}
  .logo span {{ background: linear-gradient(135deg, #8B5CF6, #14B8A6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
  .ind-row {{ display: flex; align-items: center; gap: 8px; }}
  .ind-row .pill {{ font-size: 12px; padding: 5px 12px; background: rgba(139,92,246,0.15); border: 1px solid rgba(139,92,246,0.35); color: #c4b5fd; border-radius: 100px; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase; }}
  .ind-row .yr {{ font-size: 12px; color: #94a3b8; font-family: monospace; letter-spacing: 0.08em; }}
  h1 {{ font-size: 42px; font-weight: 900; line-height: 1.05; letter-spacing: -0.03em; margin: 18px 0 16px; }}
  .kicker {{ font-size: 14px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.18em; margin-bottom: 8px; }}
  .bottom-l {{ font-size: 14px; color: #94a3b8; line-height: 1.5; }}
  .bottom-l strong {{ color: #fff; }}
  .right {{
    background:
      radial-gradient(circle at 50% 50%, rgba(139,92,246,0.32) 0%, transparent 65%),
      linear-gradient(135deg, #1a1530 0%, #0c0a1e 100%);
    padding: 48px; display: flex; flex-direction: column; justify-content: space-between; align-items: end;
  }}
  .domain {{ font-size: 13px; color: #94a3b8; font-family: monospace; letter-spacing: 0.05em; }}
  .num-wrap {{ width: 100%; text-align: center; }}
  .num {{
    font-size: {metric_size}px; font-weight: 900; line-height: 0.9; letter-spacing: -0.06em;
    background: linear-gradient(180deg, #fff 0%, #c4b5fd 50%, #14B8A6 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    text-shadow: 0 0 80px rgba(139,92,246,0.4);
  }}
  .num-label {{ font-size: 16px; color: rgba(255,255,255,0.5); text-transform: uppercase; letter-spacing: 0.18em; margin-top: 12px; }}
  .arr {{ font-size: 18px; color: #8B5CF6; font-weight: 700; }}
</style>
</head>
<body>
<div class="og">
  <div class="left">
    <div>
      <div class="logo">10×<span>SEO</span></div>
      <div style="margin-top: 32px;">
        <div class="ind-row"><span class="pill">{industry}</span><span class="yr">· {tf} · {year}</span></div>
        <div class="kicker" style="margin-top: 18px;">{kicker}</div>
        <h1>{title}</h1>
      </div>
    </div>
    <div class="bottom-l">{bottom}</div>
  </div>
  <div class="right">
    <span class="domain">10xseo.ge/case-studies</span>
    <div class="num-wrap">
      <div class="num">{metric}</div>
      <div class="num-label">შედეგი</div>
    </div>
    <span class="arr">სრული ისტორია →</span>
  </div>
</div>
</body>
</html>
"""

# ============== Template B: CHART HERO ==============
TPL_B = """<!DOCTYPE html>
<html lang="ka">
<head>
<meta charset="UTF-8">
<title>OG B · {slug}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ background: #1a1a1a; min-height: 100vh; display: flex; align-items: center; justify-content: center; font-family: 'Inter', sans-serif; }}
  .og {{
    width: 1200px; height: 630px; position: relative; overflow: hidden;
    background:
      radial-gradient(ellipse at 80% 80%, rgba(20,184,166,0.20) 0%, transparent 60%),
      radial-gradient(ellipse at 20% 20%, rgba(139,92,246,0.18) 0%, transparent 60%),
      linear-gradient(180deg, #020710 0%, #0a0f1c 100%);
    color: #fff;
  }}
  .chart {{ position: absolute; left: 0; right: 0; bottom: 60px; width: 100%; height: 460px; }}
  .top {{ position: absolute; top: 36px; left: 48px; right: 48px; display: flex; justify-content: space-between; align-items: center; z-index: 3; }}
  .logo {{ font-weight: 800; font-size: 22px; letter-spacing: -0.02em; }}
  .logo span {{ background: linear-gradient(135deg, #8B5CF6, #14B8A6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
  .pill {{ padding: 6px 14px; background: rgba(20,184,166,0.15); border: 1px solid rgba(20,184,166,0.35); color: #5eead4; border-radius: 100px; font-size: 13px; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase; }}
  .content {{ position: absolute; top: 100px; left: 48px; right: 48px; z-index: 3; }}
  .kicker {{ font-size: 14px; color: #5eead4; letter-spacing: 0.18em; text-transform: uppercase; margin-bottom: 10px; font-weight: 600; }}
  h1 {{ font-size: 48px; font-weight: 900; line-height: 1.0; letter-spacing: -0.03em; max-width: 600px; }}
  .num-block {{ position: absolute; right: 48px; bottom: 110px; text-align: right; z-index: 4; }}
  .num {{
    font-size: {metric_size}px; font-weight: 900; line-height: 0.85; letter-spacing: -0.06em;
    background: linear-gradient(180deg, #fff 0%, #14B8A6 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    text-shadow: 0 0 60px rgba(20,184,166,0.5);
  }}
  .num-label {{ font-size: 14px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.15em; margin-top: 6px; }}
  .bottom {{ position: absolute; bottom: 36px; left: 48px; right: 48px; display: flex; justify-content: space-between; align-items: center; z-index: 3; }}
  .bottom-l {{ font-size: 13px; color: #94a3b8; }}
  .arr {{ font-size: 16px; color: #5eead4; font-weight: 700; }}
</style>
</head>
<body>
<div class="og">
  <svg class="chart" viewBox="0 0 1200 460" preserveAspectRatio="none">
    <defs>
      <linearGradient id="gline" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#8B5CF6"/><stop offset="100%" stop-color="#14B8A6"/></linearGradient>
      <linearGradient id="garea" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#14B8A6" stop-opacity="0.42"/><stop offset="100%" stop-color="#14B8A6" stop-opacity="0"/></linearGradient>
      <filter id="gloss"><feGaussianBlur stdDeviation="4"/></filter>
    </defs>
    <g stroke="rgba(255,255,255,0.04)" stroke-width="1">
      <line x1="0" y1="115" x2="1200" y2="115"/><line x1="0" y1="230" x2="1200" y2="230"/><line x1="0" y1="345" x2="1200" y2="345"/>
    </g>
    <polyline points="0,400 100,395 200,380 350,355 480,310 600,250 720,185 830,125 920,75 1020,42 1100,22 1200,12" fill="none" stroke="url(#gline)" stroke-width="14" stroke-linecap="round" stroke-linejoin="round" filter="url(#gloss)" opacity="0.6"/>
    <polyline points="0,400 100,395 200,380 350,355 480,310 600,250 720,185 830,125 920,75 1020,42 1100,22 1200,12" fill="none" stroke="url(#gline)" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
    <polygon points="0,400 100,395 200,380 350,355 480,310 600,250 720,185 830,125 920,75 1020,42 1100,22 1200,12 1200,460 0,460" fill="url(#garea)"/>
    <circle cx="1200" cy="12" r="14" fill="#fff" opacity="0.4" filter="url(#gloss)"/>
    <circle cx="1200" cy="12" r="9" fill="#14B8A6"/>
    <circle cx="1200" cy="12" r="4" fill="#fff"/>
  </svg>
  <div class="top">
    <div class="logo">10×<span>SEO</span></div>
    <span class="pill">⬢ {industry} · {tf}</span>
  </div>
  <div class="content">
    <div class="kicker">{kicker}</div>
    <h1>{title}</h1>
  </div>
  <div class="num-block">
    <div class="num">{metric}</div>
    <div class="num-label">{year}</div>
  </div>
  <div class="bottom">
    <div class="bottom-l">{bottom}</div>
    <span class="arr">10xseo.ge →</span>
  </div>
</div>
</body>
</html>
"""

# ============== Template C: EDITORIAL MAGAZINE ==============
TPL_C = """<!DOCTYPE html>
<html lang="ka">
<head>
<meta charset="UTF-8">
<title>OG C · {slug}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&family=Lora:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ background: #1a1a1a; min-height: 100vh; display: flex; align-items: center; justify-content: center; font-family: 'Lora', Georgia, serif; }}
  .og {{
    width: 1200px; height: 630px; position: relative; overflow: hidden;
    background: #F5F1E8; color: #0F172A; padding: 48px 64px;
    background-image:
      radial-gradient(circle at 85% 15%, rgba(184,134,11,0.06) 0, transparent 40%),
      radial-gradient(circle at 15% 85%, rgba(184,61,42,0.06) 0, transparent 40%);
  }}
  .masthead {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #0F172A; padding-bottom: 14px; margin-bottom: 4px; }}
  .name {{ font-family: 'Playfair Display', serif; font-weight: 900; font-size: 24px; letter-spacing: -0.02em; text-transform: uppercase; }}
  .name span {{ font-style: italic; font-weight: 400; }}
  .vol {{ font-size: 12px; letter-spacing: 0.18em; text-transform: uppercase; color: #475569; }}
  .rule-d {{ border-top: 1px solid #0F172A; border-bottom: 4px double #0F172A; height: 5px; margin-bottom: 28px; }}
  .body {{ display: grid; grid-template-columns: 220px 1fr; gap: 40px; align-items: start; }}
  .ch-num {{ font-family: 'Playfair Display', serif; font-weight: 900; font-size: 120px; line-height: 0.9; color: #0F172A; letter-spacing: -0.04em; }}
  .ch-label {{ font-family: 'Playfair Display', serif; font-style: italic; font-size: 14px; color: #B83D2A; letter-spacing: 0.1em; text-transform: uppercase; margin-top: 6px; }}
  .ind-tag {{ display: inline-block; font-size: 11px; padding: 4px 10px; background: #ECE6D6; color: #475569; letter-spacing: 0.12em; text-transform: uppercase; margin-top: 10px; font-family: 'Lora', serif; }}
  .deck {{ font-family: 'Playfair Display', serif; font-style: italic; font-size: 22px; line-height: 1.4; color: #475569; margin-bottom: 18px; }}
  h1 {{ font-family: 'Playfair Display', serif; font-weight: 900; font-size: 52px; line-height: 1.05; letter-spacing: -0.025em; margin-bottom: 18px; color: #0F172A; }}
  h1 em {{ font-style: italic; color: #B83D2A; }}
  .metric-strip {{ display: flex; align-items: baseline; gap: 14px; padding-top: 16px; border-top: 1px solid rgba(15,23,42,0.18); }}
  .metric-strip .m {{ font-family: 'Playfair Display', serif; font-weight: 900; font-size: 72px; letter-spacing: -0.04em; line-height: 0.9; color: #B83D2A; }}
  .metric-strip .ml {{ font-family: 'Lora', serif; font-style: italic; font-size: 16px; color: #475569; }}
  .metric-strip .tf {{ font-family: 'Lora', serif; font-style: italic; font-size: 14px; color: #94a3b8; margin-left: auto; }}
  .bottom-c {{ position: absolute; bottom: 28px; left: 64px; right: 64px; display: flex; justify-content: space-between; font-size: 11px; letter-spacing: 0.12em; text-transform: uppercase; color: #475569; padding-top: 12px; border-top: 1px solid rgba(15,23,42,0.12); }}
  .bottom-c .read {{ font-family: 'Playfair Display', serif; font-style: italic; color: #B83D2A; text-transform: none; letter-spacing: 0; font-size: 16px; border-bottom: 1px solid #B83D2A; padding-bottom: 1px; }}
</style>
</head>
<body>
<div class="og">
  <header class="masthead">
    <div class="name">10×SEO · <span>The Quarterly</span></div>
    <div class="vol">CASE STUDY · {year}</div>
  </header>
  <div class="rule-d"></div>
  <div class="body">
    <div>
      <div class="ch-num">{chapter}.</div>
      <div class="ch-label">თავი</div>
      <span class="ind-tag">{industry} · {tf}</span>
    </div>
    <div>
      <div class="deck">{kicker}</div>
      <h1>{title}</h1>
      <div class="metric-strip">
        <div class="m">{metric}</div>
        <div class="ml">{kicker_short}</div>
        <div class="tf">{tf}</div>
      </div>
    </div>
  </div>
  <div class="bottom-c">
    <span>{bottom}</span>
    <span class="read">სრული ისტორია →</span>
  </div>
</div>
</body>
</html>
"""

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
    # detect og card top (first non-body-color pixel)
    body_rgb = (26, 26, 26)
    start = 0
    for y in range(0, img.size[1]):
        px = img.getpixel((600, y))
        if any(abs(px[i] - body_rgb[i]) > 5 for i in range(3)):
            start = y; break
    cropped = img.crop((0, start, 1200, start + 630))
    cropped.save(dst_png, optimize=True)

def main():
    templates = {"vA": TPL_A, "vB": TPL_B, "vC": TPL_C}
    print(f"Generating {len(CASES)} cases × {len(templates)} designs = {len(CASES)*len(templates)} variants")
    print("=" * 70)
    for vkey, tpl in templates.items():
        for c in CASES:
            data = dict(c)
            data["kicker_short"] = c["kicker"][:30]
            html = tpl.format(**data)
            html_path = HTML_BASE / vkey / f"{c['slug']}.html"
            html_path.write_text(html, encoding="utf-8")
            raw = HTML_BASE / vkey / f"_raw_{c['slug']}.png"
            screenshot(html_path, raw)
            final = PNG_BASE / vkey / f"{c['og']}.png"
            crop_to_og(raw, final)
            raw.unlink()
            print(f"  ✓ {vkey} · {c['slug']:40} → {final.name}")
    print()
    print("Done. Compare at og-per-case-compare.html (to be built)")

if __name__ == "__main__":
    main()
