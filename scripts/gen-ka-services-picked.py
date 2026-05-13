#!/usr/bin/env python3
"""Generate 6 KA service OGs based on user's Gemini picks. Yellow v6 style + real logo."""
import subprocess
from pathlib import Path
from PIL import Image

ROOT = Path("/Users/imac/SEO/command-center")
OUT = ROOT / "images" / "og"
TEMP = ROOT / "og-ka-svc-temp"
TEMP.mkdir(exist_ok=True)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LOGO_PATH = f"file://{ROOT}/images/logo.webp"

# User's picks + appropriate fs1/fs2 sizes per text length + icons
PICKS = [
    {"file":"service-seo-mgmt", "icon":"📈", "pill":"ფიქსირებული ფასი",
     "line1":"თქვენი SEO", "line2":"დეპარტამენტი", "deck":"სრული გუნდი და პროცესები თქვენი ბიზნესის ზრდისთვის, ერთ პაკეტში.",
     "fs1":92, "fs2":92},
    {"file":"service-seo-strategy", "icon":"🎯", "pill":"ზრდისთვის",
     "line1":"SEO", "line2":"სტრატეგიული გეგმა", "deck":"გააორმაგე ორგანული ტრაფიკი და გაუსწარი კონკურენტებს ჩვენი 12-თვიანი გეგმით.",
     "fs1":160, "fs2":86},
    {"file":"service-cro", "icon":"🔁", "pill":"CRO სერვისი",
     "line1":"კონვერსიის", "line2":"ოპტიმიზაცია", "deck":"გაზარდეთ გაყიდვები თქვენი არსებული ვებ-ტრაფიკის მაქსიმალური გამოყენებით.",
     "fs1":108, "fs2":108},
    {"file":"service-google-ads", "icon":"💰", "pill":"მეტი კონვერსია",
     "line1":"მიზნობრივი რეკლამა", "line2":"გაყიდვების ზრდა", "deck":"გადააქციეთ დაინტერესებული მნახველები რეალურ მომხმარებლებად ეფექტური მეთოდებით.",
     "fs1":76, "fs2":80},
    {"file":"service-ai-seo", "icon":"🤖", "pill":"ბრენდის ავტორიტეტი",
     "line1":"გახდი წყარო", "line2":"AI პასუხებისთვის", "deck":"ჩვენ ვეხმარებით AI მოდელებს, რომ შენი ბრენდი ექსპერტად აღიქვან.",
     "fs1":94, "fs2":80},
    {"file":"service-seo-course", "icon":"🎓", "pill":"პრაქტიკული კურსი",
     "line1":"SEO", "line2":"სრული კურსი", "deck":"ისწავლე ნოლიდან advanced-მდე რეალურ პროექტებზე მუშაობით და მიიღე სერტიფიკატი.",
     "fs1":160, "fs2":115},
]

TPL = """<!DOCTYPE html><html lang="ka"><head><meta charset="UTF-8">
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
  color: rgba(255,255,255,0.85); border-radius: 100px; font-size: 13px; font-weight: 700; letter-spacing: 0.16em; text-transform: uppercase;
}}
.content {{ flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; max-width: 1080px; padding: 0 20px; }}
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
.deck {{ font-size: 15px; color: rgba(255,255,255,0.6); letter-spacing: 0.04em; font-weight: 600; margin-top: 8px; text-align: center; max-width: 900px; line-height: 1.4; }}
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
    <div class="subline">{line2}</div>
    <div class="deck">{deck}</div>
  </div>
  <div class="logo-area">
    <img class="logo-img" src="{logo}">
  </div>
</div></body></html>
"""

for p in PICKS:
    html = TPL.format(**p, logo=LOGO_PATH)
    hp = TEMP / f"{p['file']}.html"
    hp.write_text(html, encoding="utf-8")
    raw = TEMP / f"_raw_{p['file']}.png"
    subprocess.run([CHROME,"--headless","--disable-gpu","--no-sandbox","--hide-scrollbars",
                    "--window-size=1200,800","--default-background-color=000000ff",
                    f"--screenshot={raw}",f"file://{hp}"], capture_output=True)
    img = Image.open(raw).convert("RGB")
    body = (26,26,26); start = 0
    for y in range(img.size[1]):
        if any(abs(img.getpixel((600,y))[i]-body[i])>5 for i in range(3)):
            start = y; break
    out = OUT / f"{p['file']}.jpg"
    img.crop((0, start, 1200, start+630)).save(out, "JPEG", quality=92, optimize=True, progressive=True)
    raw.unlink()
    import os
    print(f"  ✓ {p['file']}.jpg ({os.path.getsize(out)/1024:.0f} KB)  — \"{p['line1']} {p['line2']}\"")

import shutil; shutil.rmtree(TEMP)
print(f"\nGenerated 6 KA service OGs.")
