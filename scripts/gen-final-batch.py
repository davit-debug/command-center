#!/usr/bin/env python3
"""Final batch: KA seo-audit update + 14 EN equivalents matching recent KA picks."""
import subprocess
from pathlib import Path
from PIL import Image

ROOT = Path("/Users/imac/SEO/command-center")
OUT = ROOT / "images" / "og"
TEMP = ROOT / "og-final-temp"
TEMP.mkdir(exist_ok=True)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LOGO = f"file://{ROOT}/images/logo.webp"

ITEMS = [
    # KA SEO AUDIT UPDATE
    {"file":"service-seo-audit", "icon":"🔍", "pill":"უფასო · 72 საათში",
     "line1":"უფასო", "line2":"SEO აუდიტი",
     "deck":"ჩვენ არ ვითხოვთ ფულს, სანამ არ დაგანახებთ საიტის ყველა პრობლემას.",
     "fs1":160, "fs2":110},

    # ===== 14 EN MIRRORS =====
    {"file":"service-seo-mgmt-en", "icon":"📈", "pill":"FLAT FEE",
     "line1":"YOUR SEO", "line2":"DEPARTMENT",
     "deck":"Full team and processes for your business growth, in one package.",
     "fs1":108, "fs2":108},
    {"file":"seo-strategy", "icon":"🎯", "pill":"FOR GROWTH",
     "line1":"SEO", "line2":"STRATEGIC PLAN",
     "deck":"Double your organic traffic and outpace competitors with our 12-month plan.",
     "fs1":170, "fs2":88},
    {"file":"cro", "icon":"🔁", "pill":"CRO SERVICE",
     "line1":"CONVERSION", "line2":"OPTIMIZATION",
     "deck":"Increase sales by maximizing your existing web traffic.",
     "fs1":115, "fs2":108},
    {"file":"google-ads", "icon":"💰", "pill":"MORE CONVERSIONS",
     "line1":"TARGETED ADS", "line2":"SALES GROWTH",
     "deck":"Turn interested viewers into real customers with effective methods.",
     "fs1":92, "fs2":105},
    {"file":"ai-seo", "icon":"🤖", "pill":"BRAND AUTHORITY",
     "line1":"BECOME THE SOURCE", "line2":"FOR AI ANSWERS",
     "deck":"We help AI models recognize your brand as the expert.",
     "fs1":80, "fs2":95},
    {"file":"seo-course", "icon":"🎓", "pill":"PRACTICAL COURSE",
     "line1":"SEO", "line2":"FULL COURSE",
     "deck":"Learn from zero to advanced through real projects and get certified.",
     "fs1":170, "fs2":135},
    {"file":"seo-consultation", "icon":"💬", "pill":"1:1 STRATEGY",
     "line1":"ANSWERS TO", "line2":"YOUR QUESTIONS",
     "deck":"Get years of expertise in a 60-min session — strategy directly from an expert.",
     "fs1":115, "fs2":105},
    {"file":"service-seo-copy-en", "icon":"✍", "pill":"EXPERT COPYWRITING",
     "line1":"NOT ROBOTIC", "line2":"LIVING TEXT",
     "deck":"We write for humans, not just algorithms — create emotional connection.",
     "fs1":115, "fs2":120},
    {"file":"copywriting", "icon":"🖋", "pill":"STOP THE LOSS",
     "line1":"VAGUE TEXT", "line2":"LOSES CLIENTS",
     "deck":"Fix mistakes today and see conversion increase immediately.",
     "fs1":118, "fs2":118},
    {"file":"seo-audit-en", "icon":"🔍", "pill":"FREE · 24H",
     "line1":"FREE", "line2":"SEO AUDIT",
     "deck":"We don't ask for money before showing you all the issues on your site.",
     "fs1":170, "fs2":130},

    # 4 EN INDUSTRIES
    {"file":"real-estate-seo", "icon":"🏙", "pill":"DREAM HOME",
     "line1":"HELP BUYERS", "line2":"FIND THEIR HOME",
     "deck":"You build dreams — we help people find them.",
     "fs1":112, "fs2":92},
    {"file":"ecommerce-seo", "icon":"🛒", "pill":"E-COMMERCE SEO",
     "line1":"MORE SALES", "line2":"IN YOUR STORE",
     "deck":"Bring your online store to Google's first page and grow revenue.",
     "fs1":120, "fs2":110},
    {"file":"healthcare-seo", "icon":"🛡", "pill":"MEDICAL SEO",
     "line1":"MORE PATIENTS", "line2":"FROM GOOGLE",
     "deck":"Our strategy makes your clinic the answer to patients' first question.",
     "fs1":108, "fs2":130},
    {"file":"financial-seo", "icon":"🏛", "pill":"FINANCIAL SECTOR",
     "line1":"SEO", "line2":"FOR FINANCIAL SECTOR",
     "deck":"We understand financial regulations and craft safe growth strategies.",
     "fs1":175, "fs2":72},
]

TPL = """<!DOCTYPE html><html><head><meta charset="UTF-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800;900&family=Bungee&display=swap" rel="stylesheet">
<style>
* {{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:#1a1a1a;min-height:100vh;display:flex;align-items:center;justify-content:center;font-family:'Inter',sans-serif}}
.og{{width:1200px;height:630px;position:relative;overflow:hidden;
  background:radial-gradient(ellipse at 15% 50%,rgba(255,200,0,0.10) 0%,transparent 40%),
    radial-gradient(ellipse at 85% 50%,rgba(20,184,166,0.05) 0%,transparent 40%),
    linear-gradient(180deg,#0a1228 0%,#050a18 60%,#03060e 100%);
  color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:56px 64px 44px}}
.top-area{{height:56px;display:flex;align-items:center;gap:18px}}
.icon{{font-size:36px;filter:drop-shadow(0 0 15px rgba(255,217,107,0.4))}}
.pill{{padding:8px 18px;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.22);color:rgba(255,255,255,0.85);border-radius:100px;font-size:13px;font-weight:700;letter-spacing:0.16em;text-transform:uppercase}}
.content{{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;max-width:1080px;padding:0 20px}}
.headline{{font-family:'Bungee','Inter',sans-serif;font-weight:900;font-size:{fs1}px;line-height:0.95;letter-spacing:-0.02em;text-align:center;color:#FFD66B;text-shadow:0 0 25px rgba(255,214,107,0.45),0 0 50px rgba(255,196,0,0.2)}}
.subline{{font-family:'Bungee','Inter',sans-serif;font-weight:900;font-size:{fs2}px;line-height:1;letter-spacing:-0.01em;text-align:center;color:#fff;text-shadow:0 0 20px rgba(255,255,255,0.3)}}
.deck{{font-size:15px;color:rgba(255,255,255,0.6);letter-spacing:0.04em;font-weight:600;margin-top:8px;text-align:center;max-width:900px;line-height:1.4}}
.logo-area{{height:44px;display:flex;align-items:center;justify-content:center}}
.logo-img{{height:38px;width:auto;display:block;filter:drop-shadow(0 0 12px rgba(255,217,107,0.18))}}
</style></head><body>
<div class="og">
<div class="top-area"><span class="icon">{icon}</span><span class="pill">{pill}</span></div>
<div class="content"><div class="headline">{line1}</div><div class="subline">{line2}</div><div class="deck">{deck}</div></div>
<div class="logo-area"><img class="logo-img" src="{logo}"></div>
</div></body></html>"""

for p in ITEMS:
    html = TPL.format(**p, logo=LOGO)
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
print(f"\nGenerated {len(ITEMS)} OG files (1 KA + 14 EN)")
