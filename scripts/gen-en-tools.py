#!/usr/bin/env python3
"""Generate 7 EN tool OGs + update meta tags."""
import subprocess, re
from pathlib import Path
from PIL import Image

ROOT = Path("/Users/imac/SEO/command-center")
OUT = ROOT / "images" / "og"
TEMP = ROOT / "og-tools-en-temp"
TEMP.mkdir(exist_ok=True)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LOGO = f"file://{ROOT}/images/logo.webp"

TOOLS = [
    {"file":"tool-content-brief-en", "html":"en/tools/content-brief-builder.html",
     "icon":"📋", "pill":"FREE TOOL",
     "line1":"CONTENT BRIEF", "line2":"BUILDER",
     "deck":"Generate complete SEO content briefs in seconds.",
     "fs1":102, "fs2":134},
    {"file":"tool-keyword-density-en", "html":"en/tools/keyword-density.html",
     "icon":"🔢", "pill":"FREE TOOL",
     "line1":"KEYWORD", "line2":"DENSITY",
     "deck":"Check keyword frequency and avoid over-optimization.",
     "fs1":150, "fs2":150},
    {"file":"tool-numbers-words-en", "html":"en/tools/numbers-to-words.html",
     "icon":"🔤", "pill":"FREE TOOL",
     "line1":"NUMBERS", "line2":"TO WORDS",
     "deck":"Convert numbers to spelled-out words instantly.",
     "fs1":146, "fs2":146},
    {"file":"tool-og-preview-en", "html":"en/tools/og-preview.html",
     "icon":"📱", "pill":"FREE TOOL",
     "line1":"OPEN GRAPH", "line2":"PREVIEW",
     "deck":"See your social share card on Facebook, X, LinkedIn before posting.",
     "fs1":118, "fs2":150},
    {"file":"tool-pixel-width-en", "html":"en/tools/pixel-width-checker.html",
     "icon":"📏", "pill":"FREE TOOL",
     "line1":"PIXEL WIDTH", "line2":"CHECKER",
     "deck":"Check meta title and description pixel width for Google SERP.",
     "fs1":115, "fs2":140},
    {"file":"tool-readability-en", "html":"en/tools/readability-score.html",
     "icon":"📖", "pill":"FREE TOOL",
     "line1":"READABILITY", "line2":"SCORE",
     "deck":"Measure text readability with Flesch-Kincaid and grade-level scoring.",
     "fs1":116, "fs2":150},
    {"file":"tool-content-editor-en", "html":"en/tools/seo-content-editor.html",
     "icon":"✏", "pill":"FREE TOOL",
     "line1":"SEO CONTENT", "line2":"EDITOR",
     "deck":"Real-time SEO optimization while you write — score and suggestions.",
     "fs1":118, "fs2":150},
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

for t in TOOLS:
    html = TPL.format(**t, logo=LOGO)
    hp = TEMP / f"{t['file']}.html"
    hp.write_text(html, encoding="utf-8")
    raw = TEMP / f"_raw_{t['file']}.png"
    subprocess.run([CHROME,"--headless","--disable-gpu","--no-sandbox","--hide-scrollbars",
                    "--window-size=1200,800","--default-background-color=000000ff",
                    f"--screenshot={raw}",f"file://{hp}"], capture_output=True)
    img = Image.open(raw).convert("RGB")
    body = (26,26,26); start = 0
    for y in range(img.size[1]):
        if any(abs(img.getpixel((600,y))[i]-body[i])>5 for i in range(3)):
            start = y; break
    out = OUT / f"{t['file']}.jpg"
    img.crop((0, start, 1200, start+630)).save(out, "JPEG", quality=92, optimize=True, progressive=True)
    raw.unlink()
    import os
    print(f"  ✓ {t['file']}.jpg ({os.path.getsize(out)/1024:.0f} KB)")

    # Update EN tool HTML meta tag to point to new EN file
    html_path = ROOT / t['html']
    if html_path.exists():
        content = html_path.read_text(encoding="utf-8")
        new_url = f"https://10xseo.ge/images/og/{t['file']}.jpg"
        new_content = re.sub(
            r'(<meta\s+(?:property|name)="(?:og:image|twitter:image)"\s+content=")https://10xseo\.ge/images/og/[^"]+\.jpg"',
            rf'\1{new_url}"',
            content
        )
        if new_content != content:
            html_path.write_text(new_content, encoding="utf-8")
            print(f"    └ meta updated: {t['html']}")

import shutil; shutil.rmtree(TEMP)
print(f"\nGenerated 7 EN tool OGs + meta tag updates.")
