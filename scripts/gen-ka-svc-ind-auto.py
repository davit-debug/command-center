#!/usr/bin/env python3
"""Auto-pick best Gemini variant per page + regenerate OGs. v6 yellow style + real logo."""
import subprocess
from pathlib import Path
from PIL import Image

ROOT = Path("/Users/imac/SEO/command-center")
OUT = ROOT / "images" / "og"
TEMP = ROOT / "og-ka-auto-temp"
TEMP.mkdir(exist_ok=True)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LOGO_PATH = f"file://{ROOT}/images/logo.webp"

# Auto-picked best variants per page (based on grammar + marketing strength)
PICKS = [
    # 4 SERVICES
    {"file":"service-consultation", "icon":"💬", "pill":"სტრატეგია 1:1",
     "line1":"პასუხები შენს", "line2":"კითხვებზე", "deck":"60 წუთში მიიღე წლების გამოცდილებაზე დაფუძნებული სტრატეგია პირდაპირ ექსპერტისგან.",
     "fs1":92, "fs2":140},
    {"file":"service-seo-copy", "icon":"✍", "pill":"ექსპერტული კოპირაიტინგი",
     "line1":"არა რობოტული", "line2":"ცოცხალი ტექსტი", "deck":"ვწერთ ადამიანებისთვის, არა მხოლოდ ალგორითმებისთვის — შექმენი ემოციური კავშირი.",
     "fs1":88, "fs2":90},
    {"file":"service-copywriting", "icon":"🖋", "pill":"შეაჩერე დანაკარგი",
     "line1":"ბუნდოვანი ტექსტი", "line2":"გართმევს კლიენტებს", "deck":"გამოასწორე შეცდომები დღესვე და დაინახე კონვერტაციის მყისიერი ზრდა.",
     "fs1":78, "fs2":80},
    {"file":"service-seo-audit", "icon":"🔍", "pill":"სხვაგვარი მიდგომა",
     "line1":"ჯერ ნახე", "line2":"შემდეგ გადაიხადე", "deck":"ჩვენ არ ვითხოვთ ფულს, სანამ არ დაგანახებთ საიტის ყველა პრობლემას.",
     "fs1":120, "fs2":78},

    # 4 INDUSTRIES
    {"file":"construction-burj", "icon":"🏙", "pill":"დეველოპერებისთვის",
     "line1":"კონკურენტი", "line2":"უკვე პირველია", "deck":"სანამ ფიქრობთ, თქვენი კონკურენტები Google-იდან იზიდავენ მყიდველებს. დრო ფულია.",
     "fs1":120, "fs2":98},
    {"file":"ecommerce-tower", "icon":"🛒", "pill":"E-COMMERCE SEO",
     "line1":"მეტი გაყიდვები", "line2":"შენს მაღაზიაში", "deck":"მიიყვანე შენი ონლაინ მაღაზია Google-ის პირველ გვერდზე და გაზარდე შემოსავალი.",
     "fs1":108, "fs2":108},
    {"file":"healthcare-tower", "icon":"🛡", "pill":"სამედიცინო SEO",
     "line1":"მეტი პაციენტი", "line2":"Google-იდან", "deck":"ჩვენი სტრატეგიით თქვენი კლინიკა გახდება პასუხი პაციენტის პირველსავე კითხვაზე.",
     "fs1":110, "fs2":130},
    {"file":"financial-tower", "icon":"🏛", "pill":"YMYL ექსპერტიზა",
     "line1":"ექსპერტული SEO", "line2":"სანდო შედეგები", "deck":"ჩვენ გვესმის ფინანსური რეგულაციები და ვქმნით უსაფრთხო ზრდის სტრატეგიებს.",
     "fs1":110, "fs2":104},
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
  color: #FFD66B; text-shadow: 0 0 25px rgba(255,214,107,0.45), 0 0 50px rgba(255,196,0,0.2);
}}
.subline {{
  font-family: 'Bungee', 'Inter', sans-serif; font-weight: 900;
  font-size: {fs2}px; line-height: 1; letter-spacing: -0.01em; text-align: center;
  color: #fff; text-shadow: 0 0 20px rgba(255,255,255,0.3);
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
  <div class="logo-area"><img class="logo-img" src="{logo}"></div>
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
    print(f"  ✓ {p['file']}.jpg ({os.path.getsize(out)/1024:.0f} KB) — \"{p['line1']} {p['line2']}\"")

import shutil; shutil.rmtree(TEMP)
print(f"\nGenerated 8 KA OGs (4 services + 4 industries) auto-picked.")
