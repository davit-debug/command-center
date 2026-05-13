#!/usr/bin/env python3
"""
EN OG image generator v2 — fixes:
1. Uses REAL logo.webp image (not text-based)
2. Better flex layout to prevent overlap
3. Slightly smaller AI SEO sizes
4. Adds en versions for blog index + case studies index
"""
import subprocess
from pathlib import Path
from PIL import Image

ROOT = Path("/Users/imac/SEO/command-center")
OUT = ROOT / "images" / "og"
TEMP = ROOT / "og-en-v2-temp"
TEMP.mkdir(parents=True, exist_ok=True)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LOGO_PATH = f"file://{ROOT}/images/logo.webp"

TPL = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800;900&family=Bungee&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ background: #1a1a1a; min-height: 100vh; display: flex; align-items: center; justify-content: center; font-family: 'Inter', sans-serif; }}
.og {{
  width: 1200px; height: 630px; position: relative; overflow: hidden;
  background:
    radial-gradient(ellipse at 15% 50%, rgba(255,200,0,0.10) 0%, transparent 40%),
    radial-gradient(ellipse at 85% 50%, rgba(20,184,166,0.05) 0%, transparent 40%),
    linear-gradient(180deg, #0a1228 0%, #050a18 60%, #03060e 100%);
  color: #fff;
  display: flex; flex-direction: column; align-items: center; justify-content: space-between;
  padding: 56px 64px 44px;
}}
.top-area {{ height: 56px; display: flex; align-items: center; gap: 18px; }}
.icon {{ font-size: 36px; filter: drop-shadow(0 0 15px rgba(255,217,107,0.4)); }}
.pill {{
  padding: 8px 18px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.22);
  color: rgba(255,255,255,0.85); border-radius: 100px; font-size: 13px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase;
}}
.content {{ flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 14px; max-width: 1080px; padding: 0 20px; }}
.headline {{
  font-family: 'Bungee', 'Inter', sans-serif; font-weight: 900;
  font-size: {fs1}px; line-height: 0.95; letter-spacing: -0.02em; text-align: center;
  color: #FFD66B;
  text-shadow: 0 0 25px rgba(255,214,107,0.45), 0 0 50px rgba(255,196,0,0.2);
}}
.subline {{
  font-family: 'Bungee', 'Inter', sans-serif; font-weight: 900;
  font-size: {fs2}px; line-height: 1; letter-spacing: -0.01em; text-align: center;
  color: #fff;
  text-shadow: 0 0 20px rgba(255,255,255,0.3);
}}
.deck {{ font-size: 14px; color: rgba(255,255,255,0.6); letter-spacing: 0.05em; text-transform: uppercase; font-weight: 600; margin-top: 4px; }}
.logo-area {{ height: 44px; display: flex; align-items: center; justify-content: center; }}
.logo-img {{ height: 38px; width: auto; display: block; filter: drop-shadow(0 0 12px rgba(255,217,107,0.18)); }}
</style></head><body>
<div class="og">
  <div class="top-area">
    <span class="icon">{icon}</span>
    <span class="pill">{pill}</span>
  </div>
  <div class="content">
    <div class="headline">{line1}</div>
    {line2_block}
    {deck_block}
  </div>
  <div class="logo-area">
    <img class="logo-img" src="{logo}">
  </div>
</div></body></html>
"""

PAGES = [
    # SERVICES (10)
    {"file":"service-seo-mgmt-en", "icon":"📈", "pill":"Service",        "line1":"SEO",          "line2":"MANAGEMENT",     "deck":"Monthly · Full-Stack · ROI-driven",   "fs1":130, "fs2":105},
    {"file":"seo-consultation",    "icon":"💬", "pill":"Service",        "line1":"SEO",          "line2":"CONSULTATION",   "deck":"1-on-1 · 60-min Strategy Session",     "fs1":130, "fs2":88},
    {"file":"seo-strategy",        "icon":"🎯", "pill":"Service",        "line1":"SEO",          "line2":"STRATEGY",       "deck":"12-Month Roadmap · Custom-built",       "fs1":130, "fs2":115},
    {"file":"service-seo-copy-en", "icon":"✍",  "pill":"Service",        "line1":"SEO",          "line2":"COPYWRITING",    "deck":"Content That Converts",                 "fs1":130, "fs2":88},
    {"file":"copywriting",         "icon":"🖋", "pill":"Premium",        "line1":"UI/UX",        "line2":"COPYWRITING",    "deck":"Microcopy That Sells",                  "fs1":130, "fs2":88},
    {"file":"cro",                 "icon":"🔁", "pill":"Service",        "line1":"CRO",          "line2":"OPTIMIZATION",   "deck":"More Customers · Same Traffic",         "fs1":160, "fs2":100},
    {"file":"google-ads",          "icon":"💰", "pill":"Service",        "line1":"GOOGLE",       "line2":"ADS",            "deck":"Search · Display · Performance Max",    "fs1":130, "fs2":150},
    {"file":"ai-seo",              "icon":"🤖", "pill":"AI · GEO · AEO", "line1":"AI",          "line2":"SEO",            "deck":"ChatGPT · Perplexity · AI Overviews",   "fs1":175, "fs2":150},
    {"file":"seo-course",          "icon":"🎓", "pill":"Education",      "line1":"SEO",          "line2":"COURSE",         "deck":"12 Weeks · Hands-on · Certified",       "fs1":130, "fs2":130},
    {"file":"seo-audit-en",        "icon":"🔍", "pill":"Free",           "line1":"FREE SEO",     "line2":"AUDIT",          "deck":"100+ Factors · Loom Video · 24h",       "fs1":100, "fs2":150},

    # INDUSTRIES (4)
    {"file":"real-estate-seo",     "icon":"🏙", "pill":"Industry",       "line1":"REAL ESTATE",  "line2":"SEO",            "deck":"For Property Developers",                "fs1":88,  "fs2":150},
    {"file":"ecommerce-seo",       "icon":"🛒", "pill":"Industry",       "line1":"E-COMMERCE",   "line2":"SEO",            "deck":"Built for Repeatable Revenue",           "fs1":96,  "fs2":150},
    {"file":"healthcare-seo",      "icon":"🛡", "pill":"Industry",       "line1":"MEDICAL",      "line2":"SEO",            "deck":"YMYL-compliant · For Clinics",           "fs1":112, "fs2":150},
    {"file":"financial-seo",       "icon":"🏛", "pill":"Industry",       "line1":"FINANCIAL",    "line2":"SEO",            "deck":"YMYL-compliant · For Finance",           "fs1":96,  "fs2":150},

    # OTHER (12: 10 prev + 2 new for blog/case-studies index)
    {"file":"page-404-en",         "icon":"🚫", "pill":"Error 404",      "line1":"PAGE NOT",     "line2":"FOUND",          "deck":"Let's get you back on track",            "fs1":104, "fs2":150},
    {"file":"page-about-us-en",    "icon":"👥", "pill":"About",          "line1":"MEET",         "line2":"10×SEO",         "deck":"Georgia's #1 SEO Agency Team",           "fs1":150, "fs2":140},
    {"file":"page-contact-us-en",  "icon":"📞", "pill":"Contact",        "line1":"GET IN",       "line2":"TOUCH",          "deck":"Book a Free 15-Min Consultation",        "fs1":130, "fs2":150},
    {"file":"page-lead-form-en",   "icon":"📝", "pill":"Free",           "line1":"FREE SEO",     "line2":"CONSULT",        "deck":"15-Min Strategy Call · No-obligation",   "fs1":100, "fs2":130},
    {"file":"page-portfolio-en",   "icon":"🏆", "pill":"Portfolio",      "line1":"REAL",         "line2":"RESULTS",        "deck":"+247% Avg · 8× ROI · 30 Days",           "fs1":150, "fs2":130},
    {"file":"service-seo-tools-en","icon":"🔧", "pill":"Free Tools",     "line1":"SEO",          "line2":"TOOLS",          "deck":"Pixel · OG · Brief · Editor · More",     "fs1":140, "fs2":150},
    {"file":"page-services-en",    "icon":"🛠", "pill":"Services",       "line1":"SEO",          "line2":"SERVICES",       "deck":"Full Ecosystem for Growth",              "fs1":140, "fs2":130},
    {"file":"page-vacancies-en",   "icon":"💼", "pill":"Careers",        "line1":"JOIN OUR",     "line2":"TEAM",           "deck":"Work With Georgia's #1 SEO Agency",      "fs1":120, "fs2":170},
    {"file":"service-ra-aris-seo-en","icon":"❓","pill":"Learn",         "line1":"WHAT IS",      "line2":"SEO?",           "deck":"The Complete Beginner's Guide",          "fs1":120, "fs2":150},
    {"file":"roi-calculator",      "icon":"🧮", "pill":"Calculator",     "line1":"SEO ROI",      "line2":"CALCULATOR",     "deck":"Estimate Your SEO Investment Return",    "fs1":104, "fs2":110},
    # NEW: blog + case-studies index EN versions
    {"file":"page-blog-en",        "icon":"📝", "pill":"Blog",           "line1":"10×SEO",       "line2":"BLOG",           "deck":"SEO · AI · Digital Marketing Insights",  "fs1":150, "fs2":150},
    {"file":"page-case-studies-en","icon":"📊", "pill":"Real Results",   "line1":"+247%",        "line2":"CASE STUDIES",   "deck":"8 Studies · 8× ROI · 30-Day Wins",       "fs1":150, "fs2":94},
]

def gen(p):
    line2 = f'<div class="subline">{p["line2"]}</div>' if p.get("line2") else ""
    deck = f'<div class="deck">{p["deck"]}</div>' if p.get("deck") else ""
    html = TPL.format(icon=p["icon"], pill=p["pill"], line1=p["line1"],
                      line2_block=line2, deck_block=deck,
                      fs1=p["fs1"], fs2=p.get("fs2", 90), logo=LOGO_PATH)
    html_path = TEMP / f"{p['file']}.html"
    html_path.write_text(html, encoding="utf-8")
    raw = TEMP / f"_raw_{p['file']}.png"
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--hide-scrollbars", "--window-size=1200,800",
                    "--default-background-color=000000ff",
                    f"--screenshot={raw}", f"file://{html_path}"],
                   capture_output=True)
    img = Image.open(raw).convert("RGB")
    body = (26, 26, 26); start = 0
    for y in range(img.size[1]):
        if any(abs(img.getpixel((600, y))[i] - body[i]) > 5 for i in range(3)):
            start = y; break
    cropped = img.crop((0, start, 1200, start + 630))
    out_jpg = OUT / f"{p['file']}.jpg"
    cropped.save(out_jpg, "JPEG", quality=92, optimize=True, progressive=True)
    raw.unlink()
    import os
    return os.path.getsize(out_jpg)

def main():
    print(f"Generating {len(PAGES)} EN OG images v2 (real logo + fixed layout)")
    print("=" * 70)
    for p in PAGES:
        size = gen(p)
        print(f"  ✓ {p['file']:35} ({size/1024:.0f} KB)  — \"{p['line1']} {p.get('line2','')}\"")
    import shutil; shutil.rmtree(TEMP)

if __name__ == "__main__":
    main()
