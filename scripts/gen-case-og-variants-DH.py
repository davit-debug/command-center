#!/usr/bin/env python3
"""
Generate 5 NEW visually distinct design variants per case (D-H):
  D · Glass Morphism Stack — 3 frosted glass cards layered with depth
  E · Aurora Iridescent — flowing iridescent gradient mesh
  F · Cinematic Spotlight — dark with single dramatic light cone
  G · Cyberpunk Neon Grid — Tron-style perspective grid floor
  H · Confetti Burst — radial particles emanating from center

Outputs: og-previews/per-case/v{D,E,F,G,H}/case-{slug}.jpg (1200x630)
Does NOT touch existing variants or production JPGs.
"""
import os
import subprocess
from pathlib import Path
from PIL import Image

ROOT = Path("/Users/imac/SEO/command-center")
HTML_BASE = ROOT / "og-per-case"
PNG_BASE = ROOT / "og-previews" / "per-case"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

for v in ["vD", "vE", "vF", "vG", "vH"]:
    (HTML_BASE / v).mkdir(parents=True, exist_ok=True)
    (PNG_BASE / v).mkdir(parents=True, exist_ok=True)

CASES = [
    {"slug":"3x-in-28-days","og":"case-3x-28days","industry":"ახალი პროექტი","metric":"3×","metric_size":380,"tf":"28 დღე","year":"2024","kicker":"ტრაფიკი 28 დღეში","title":"სამჯერ მეტი.","bottom":"1,500+ clicks/თვე"},
    {"slug":"trafikis-gaormageba-3-tveshi","og":"case-2x-traffic","industry":"სამშენებლო","metric":"×2","metric_size":380,"tf":"3 თვე","year":"2025","kicker":"ტრაფიკის გაორმაგება","title":"ორჯერ მეტი ვიზიტი.","bottom":"Keyword mapping"},
    {"slug":"250-percent-increase","og":"case-250-percent","industry":"სამშენებლო","metric":"+250%","metric_size":280,"tf":"3 თვე","year":"2025","kicker":"ორგანული ზრდა","title":"სამ თვეში — 2.5×.","bottom":"კონკურენტული მისადგომი"},
    {"slug":"270-percent-increase","og":"case-270-percent","industry":"E-commerce","metric":"+270%","metric_size":280,"tf":"3 თვე","year":"2025","kicker":"ტრაფიკი + 45% გაყიდვა","title":"Shopify გადახედვა.","bottom":"Meta + CRO"},
    {"slug":"local-seo-result","og":"case-local-seo","industry":"Local SEO","metric":"+60%","metric_size":280,"tf":"2 თვე","year":"2025","kicker":"სატელეფონო ზარები","title":"ლოკალურმა მუშაობა იცის.","bottom":"GBP + სქემა"},
    {"slug":"4200-yoveltviuri-vizitori-4-tveshi","og":"case-4200-visitors","industry":"სამედიცინო","metric":"4,200+","metric_size":240,"tf":"4 თვე","year":"2025","kicker":"ვიზიტორი თვეში","title":"YMYL ნიშის ხსნა.","bottom":"E-E-A-T + schema"},
    {"slug":"seo-krizisidan-top-3mde","og":"case-crisis-top3","industry":"B2B","metric":"TOP-3","metric_size":260,"tf":"2 თვე","year":"2025","kicker":"Google-ის რანკი","title":"კრიზისიდან TOP-3.","bottom":"disavow + recovery"},
    {"slug":"seo-crisis-management","og":"case-crisis-mgmt","industry":"B2B","metric":"TOP-3","metric_size":260,"tf":"2 თვე","year":"2025","kicker":"Google-ის რანკი","title":"კრიზისიდან TOP-3.","bottom":"Spam cleanup"},
    {"slug":"stomatologiuri-klinikis-seo","og":"case-dental","industry":"სტომატოლოგია","metric":"+600%","metric_size":280,"tf":"6 თვე","year":"2026","kicker":"6 თვეში — Google #1","title":"1,600+ ვიზიტორი თვეში.","bottom":"Schema · GBP · ლანდინგი"},
]

# ============== D · GLASS MORPHISM STACK ==============
TPL_D = """<!DOCTYPE html><html lang="ka"><head><meta charset="UTF-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ background: #1a1a1a; min-height: 100vh; display: flex; align-items: center; justify-content: center; font-family: 'Inter', sans-serif; }}
.og {{
  width: 1200px; height: 630px; position: relative; overflow: hidden;
  background:
    radial-gradient(circle at 25% 30%, #6D28D9 0%, transparent 50%),
    radial-gradient(circle at 75% 70%, #0F766E 0%, transparent 50%),
    radial-gradient(circle at 60% 20%, #DB2777 0%, transparent 40%),
    linear-gradient(135deg, #0A0218 0%, #021420 100%);
  color: #fff;
}}
.noise {{ position: absolute; inset: 0; opacity: 0.04;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"); }}
.top {{ position: absolute; top: 36px; left: 48px; right: 48px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
.logo {{ font-weight: 800; font-size: 22px; letter-spacing: -0.02em; }}
.logo span {{ background: linear-gradient(135deg, #c4b5fd, #5eead4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
.pill {{ padding: 7px 16px; background: rgba(255,255,255,0.1); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.18); color: #fff; border-radius: 100px; font-size: 13px; font-weight: 600; letter-spacing: 0.04em; }}
.stack {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -52%); width: 880px; height: 380px; }}
.glass {{ position: absolute; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.18); border-radius: 28px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.18); }}
.g-back {{ left: 0; top: 0; width: 100%; height: 100%; transform: rotate(-3deg) translateY(8px); opacity: 0.7; background: rgba(255,255,255,0.04); }}
.g-mid  {{ left: 0; top: 0; width: 100%; height: 100%; transform: rotate(2deg); opacity: 0.85; background: rgba(255,255,255,0.05); }}
.g-front {{ left: 0; top: 0; width: 100%; height: 100%; padding: 44px 56px; display: flex; flex-direction: column; justify-content: space-between; }}
.k {{ font-size: 13px; color: rgba(255,255,255,0.65); letter-spacing: 0.18em; text-transform: uppercase; font-weight: 600; }}
.num {{ font-size: calc({metric_size}px * 0.72); font-weight: 900; letter-spacing: -0.06em; line-height: 0.9; text-align: center;
  background: linear-gradient(180deg, #fff 0%, #c4b5fd 60%, #5eead4 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 0 0 60px rgba(196,181,253,0.4); }}
.bot {{ display: flex; justify-content: space-between; align-items: end; }}
.bot .ttl {{ font-size: 24px; font-weight: 800; letter-spacing: -0.02em; }}
.bot .sub {{ font-size: 13px; color: rgba(255,255,255,0.65); margin-top: 4px; }}
.arr {{ font-size: 14px; color: rgba(255,255,255,0.8); font-weight: 600; }}
</style></head><body>
<div class="og"><div class="noise"></div>
  <div class="top"><div class="logo">10×<span>SEO</span></div><span class="pill">⬢ {industry} · {tf}</span></div>
  <div class="stack">
    <div class="glass g-back"></div>
    <div class="glass g-mid"></div>
    <div class="glass g-front">
      <div><div class="k">{kicker}</div></div>
      <div class="num">{metric}</div>
      <div class="bot">
        <div><div class="ttl">{title}</div><div class="sub">{bottom}</div></div>
        <span class="arr">10xseo.ge →</span>
      </div>
    </div>
  </div>
</div></body></html>
"""

# ============== E · AURORA IRIDESCENT ==============
TPL_E = """<!DOCTYPE html><html lang="ka"><head><meta charset="UTF-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ background: #1a1a1a; min-height: 100vh; display: flex; align-items: center; justify-content: center; font-family: 'Inter', sans-serif; }}
.og {{
  width: 1200px; height: 630px; position: relative; overflow: hidden;
  background: #050505; color: #fff;
}}
.aurora {{ position: absolute; inset: 0; }}
.blob {{ position: absolute; border-radius: 50%; filter: blur(80px); mix-blend-mode: screen; }}
.b1 {{ width: 700px; height: 700px; top: -120px; left: -150px; background: #8B5CF6; }}
.b2 {{ width: 600px; height: 600px; top: 100px; right: -80px; background: #14B8A6; }}
.b3 {{ width: 500px; height: 500px; bottom: -100px; left: 30%; background: #EC4899; }}
.b4 {{ width: 400px; height: 400px; top: 40%; left: 35%; background: #3B82F6; opacity: 0.7; }}
.b5 {{ width: 350px; height: 350px; bottom: 20%; right: 25%; background: #FB923C; opacity: 0.6; }}
.veil {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,0.18) 0%, rgba(0,0,0,0.45) 100%); }}
.noise {{ position: absolute; inset: 0; opacity: 0.06;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"); }}
.content {{ position: absolute; inset: 0; padding: 56px 64px; display: flex; flex-direction: column; justify-content: space-between; z-index: 5; }}
.top {{ display: flex; justify-content: space-between; align-items: center; }}
.logo {{ font-weight: 800; font-size: 24px; letter-spacing: -0.02em; }}
.logo span {{ background: linear-gradient(135deg, #fff, #c4b5fd); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
.pill {{ padding: 8px 18px; background: rgba(255,255,255,0.12); backdrop-filter: blur(16px); border: 1px solid rgba(255,255,255,0.22); color: #fff; border-radius: 100px; font-size: 14px; font-weight: 600; letter-spacing: 0.04em; }}
.mid {{ text-align: center; }}
.num {{ font-size: {metric_size}px; font-weight: 900; line-height: 0.88; letter-spacing: -0.06em;
  background: linear-gradient(90deg, #ff6ec7 0%, #c4b5fd 25%, #5eead4 50%, #93c5fd 75%, #fbb6ce 100%);
  background-size: 200% 100%;
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 4px 20px rgba(255,255,255,0.3)); }}
.kicker {{ font-size: 14px; color: rgba(255,255,255,0.85); letter-spacing: 0.22em; text-transform: uppercase; margin-bottom: 14px; font-weight: 700; }}
.ttl {{ font-size: 32px; font-weight: 800; letter-spacing: -0.02em; margin-top: 20px; }}
.bot {{ display: flex; justify-content: space-between; align-items: end; }}
.meta {{ font-size: 14px; color: rgba(255,255,255,0.7); }}
.arr {{ font-size: 16px; color: #fff; font-weight: 700; }}
</style></head><body>
<div class="og">
  <div class="aurora"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div><div class="blob b4"></div><div class="blob b5"></div></div>
  <div class="veil"></div><div class="noise"></div>
  <div class="content">
    <div class="top"><div class="logo">10×<span>SEO</span></div><span class="pill">⬢ {industry} · {tf}</span></div>
    <div class="mid">
      <div class="kicker">{kicker}</div>
      <div class="num">{metric}</div>
      <div class="ttl">{title}</div>
    </div>
    <div class="bot"><span class="meta">{bottom}</span><span class="arr">10xseo.ge →</span></div>
  </div>
</div></body></html>
"""

# ============== F · CINEMATIC SPOTLIGHT ==============
TPL_F = """<!DOCTYPE html><html lang="ka"><head><meta charset="UTF-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&family=Cinzel:wght@500;700;900&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ background: #1a1a1a; min-height: 100vh; display: flex; align-items: center; justify-content: center; font-family: 'Inter', sans-serif; }}
.og {{
  width: 1200px; height: 630px; position: relative; overflow: hidden;
  background: radial-gradient(ellipse 700px 400px at 50% 50%, rgba(255,217,140,0.18) 0%, rgba(255,217,140,0.05) 30%, transparent 60%),
              linear-gradient(180deg, #000 0%, #0a0608 100%);
  color: #fff;
}}
.cone {{ position: absolute; top: -50px; left: 50%; transform: translateX(-50%);
  width: 0; height: 0; border-left: 280px solid transparent; border-right: 280px solid transparent;
  border-top: 700px solid rgba(255,217,140,0.08); filter: blur(40px); opacity: 0.8; }}
.cone2 {{ position: absolute; top: -100px; left: 50%; transform: translateX(-50%);
  width: 0; height: 0; border-left: 180px solid transparent; border-right: 180px solid transparent;
  border-top: 700px solid rgba(255,217,140,0.12); filter: blur(20px); }}
.grain {{ position: absolute; inset: 0; opacity: 0.08;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"); }}
.vignette {{ position: absolute; inset: 0; background: radial-gradient(ellipse at center, transparent 30%, rgba(0,0,0,0.6) 100%); }}
.content {{ position: absolute; inset: 0; padding: 48px 64px; display: flex; flex-direction: column; justify-content: space-between; z-index: 10; }}
.top {{ display: flex; justify-content: space-between; align-items: center; }}
.logo {{ font-weight: 800; font-size: 22px; letter-spacing: -0.02em; }}
.logo span {{ color: #FFD98C; }}
.pill {{ padding: 6px 14px; background: rgba(255,217,140,0.1); border: 1px solid rgba(255,217,140,0.35); color: #FFD98C; border-radius: 0; font-size: 12px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; font-family: 'Cinzel', serif; }}
.mid {{ text-align: center; }}
.presents {{ font-family: 'Cinzel', serif; font-size: 14px; color: rgba(255,217,140,0.85); letter-spacing: 0.4em; text-transform: uppercase; margin-bottom: 18px; font-weight: 500; }}
.num {{ font-size: {metric_size}px; font-weight: 900; line-height: 0.9; letter-spacing: -0.05em;
  background: linear-gradient(180deg, #FFE8B0 0%, #FFC44D 50%, #B8860B 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 0 40px rgba(255,196,77,0.5)); font-family: 'Cinzel', serif; }}
.ttl {{ font-family: 'Cinzel', serif; font-size: 30px; font-weight: 700; letter-spacing: 0.05em; margin-top: 20px; color: #fff; }}
.bot {{ display: flex; justify-content: space-between; align-items: end; }}
.meta {{ font-size: 12px; color: rgba(255,255,255,0.55); letter-spacing: 0.1em; text-transform: uppercase; font-family: 'Cinzel', serif; }}
.arr {{ font-size: 14px; color: #FFD98C; font-weight: 600; letter-spacing: 0.15em; text-transform: uppercase; font-family: 'Cinzel', serif; }}
</style></head><body>
<div class="og"><div class="cone"></div><div class="cone2"></div><div class="grain"></div><div class="vignette"></div>
  <div class="content">
    <div class="top"><div class="logo">10×<span>SEO</span></div><span class="pill">{industry} · {tf}</span></div>
    <div class="mid">
      <div class="presents">— A 10×SEO Story —</div>
      <div class="num">{metric}</div>
      <div class="ttl">{title}</div>
    </div>
    <div class="bot"><span class="meta">{bottom}</span><span class="arr">10xseo.ge →</span></div>
  </div>
</div></body></html>
"""

# ============== G · CYBERPUNK NEON GRID ==============
TPL_G = """<!DOCTYPE html><html lang="ka"><head><meta charset="UTF-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Inter:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ background: #1a1a1a; min-height: 100vh; display: flex; align-items: center; justify-content: center; font-family: 'Inter', sans-serif; }}
.og {{
  width: 1200px; height: 630px; position: relative; overflow: hidden;
  background: linear-gradient(180deg, #0a0118 0%, #1a0633 50%, #2d0858 100%);
  color: #fff;
}}
.grid {{ position: absolute; bottom: 0; left: 0; right: 0; height: 360px;
  background-image:
    linear-gradient(to right, rgba(255,0,224,0.5) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(0,255,255,0.4) 1px, transparent 1px);
  background-size: 60px 30px;
  transform: perspective(500px) rotateX(60deg);
  transform-origin: bottom; }}
.horizon {{ position: absolute; top: 270px; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent 0%, #ff00e0 50%, transparent 100%);
  filter: blur(1px); box-shadow: 0 0 20px #ff00e0, 0 0 40px #ff00e0; }}
.sun {{ position: absolute; top: 110px; left: 50%; transform: translateX(-50%);
  width: 280px; height: 280px; border-radius: 50%;
  background: radial-gradient(circle, #ff00e0 0%, #ff6ec7 40%, transparent 70%);
  filter: blur(10px); opacity: 0.9; }}
.sun-disc {{ position: absolute; top: 130px; left: 50%; transform: translateX(-50%);
  width: 220px; height: 220px; border-radius: 50%;
  background: linear-gradient(180deg, #ffeb3b 0%, #ff6ec7 50%, #ff00e0 100%);
  box-shadow: 0 0 80px rgba(255,0,224,0.6), inset 0 -20px 40px rgba(255,0,224,0.5); }}
.scan {{ position: absolute; left: 0; right: 0; top: 240px;
  height: 6px; background: rgba(0,255,255,0.15);
  box-shadow: 0 0 30px rgba(0,255,255,0.6); }}
.scan2 {{ position: absolute; left: 0; right: 0; top: 250px;
  height: 3px; background: rgba(0,255,255,0.4); }}
.top {{ position: absolute; top: 36px; left: 48px; right: 48px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
.logo {{ font-family: 'Orbitron', sans-serif; font-weight: 900; font-size: 20px; letter-spacing: 0.05em; color: #fff; text-shadow: 0 0 10px rgba(255,255,255,0.5); }}
.logo span {{ color: #00ffff; text-shadow: 0 0 12px #00ffff; }}
.pill {{ padding: 7px 16px; background: rgba(0,255,255,0.08); border: 1px solid rgba(0,255,255,0.5); color: #00ffff; border-radius: 0; font-size: 12px; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; font-family: 'Orbitron', sans-serif; box-shadow: 0 0 10px rgba(0,255,255,0.3); }}
.center {{ position: absolute; left: 50%; top: 52%; transform: translate(-50%, -50%); text-align: center; z-index: 8; }}
.num {{ font-family: 'Orbitron', sans-serif; font-size: {metric_size}px; font-weight: 900; line-height: 0.9; letter-spacing: -0.04em;
  background: linear-gradient(180deg, #fff 0%, #00ffff 60%, #ff00e0 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 0 30px rgba(0,255,255,0.7)) drop-shadow(0 0 60px rgba(255,0,224,0.5)); }}
.ttl {{ font-family: 'Orbitron', sans-serif; font-size: 22px; font-weight: 700; letter-spacing: 0.1em; margin-top: 12px; color: #00ffff; text-shadow: 0 0 12px rgba(0,255,255,0.6); text-transform: uppercase; }}
.bot {{ position: absolute; bottom: 32px; left: 48px; right: 48px; display: flex; justify-content: space-between; align-items: end; z-index: 10; }}
.meta {{ font-family: 'Orbitron', sans-serif; font-size: 11px; color: rgba(0,255,255,0.7); letter-spacing: 0.18em; text-transform: uppercase; }}
.arr {{ font-family: 'Orbitron', sans-serif; font-size: 14px; color: #ff00e0; font-weight: 700; letter-spacing: 0.15em; text-shadow: 0 0 10px rgba(255,0,224,0.6); }}
</style></head><body>
<div class="og">
  <div class="sun-disc"></div><div class="sun"></div><div class="horizon"></div>
  <div class="scan"></div><div class="scan2"></div><div class="grid"></div>
  <div class="top"><div class="logo">10×<span>SEO</span></div><span class="pill">{industry} · {tf}</span></div>
  <div class="center">
    <div class="num">{metric}</div>
    <div class="ttl">{title_short}</div>
  </div>
  <div class="bot"><span class="meta">{bottom}</span><span class="arr">10xseo.ge ↗</span></div>
</div></body></html>
"""

# ============== H · CONFETTI BURST ==============
TPL_H = """<!DOCTYPE html><html lang="ka"><head><meta charset="UTF-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ background: #1a1a1a; min-height: 100vh; display: flex; align-items: center; justify-content: center; font-family: 'Inter', sans-serif; }}
.og {{
  width: 1200px; height: 630px; position: relative; overflow: hidden;
  background:
    radial-gradient(circle at 50% 50%, rgba(139,92,246,0.25) 0%, transparent 50%),
    linear-gradient(135deg, #0a0a1a 0%, #16092e 100%);
  color: #fff;
}}
.rays {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 1000px; height: 1000px;
  background: conic-gradient(from 0deg,
    rgba(139,92,246,0.18) 0deg, transparent 8deg,
    rgba(20,184,166,0.16) 30deg, transparent 38deg,
    rgba(236,72,153,0.16) 60deg, transparent 68deg,
    rgba(234,179,8,0.14) 90deg, transparent 98deg,
    rgba(59,130,246,0.16) 120deg, transparent 128deg,
    rgba(139,92,246,0.18) 150deg, transparent 158deg,
    rgba(20,184,166,0.16) 180deg, transparent 188deg,
    rgba(236,72,153,0.16) 210deg, transparent 218deg,
    rgba(234,179,8,0.14) 240deg, transparent 248deg,
    rgba(59,130,246,0.16) 270deg, transparent 278deg,
    rgba(139,92,246,0.18) 300deg, transparent 308deg,
    rgba(20,184,166,0.16) 330deg, transparent 338deg);
  filter: blur(20px); }}
.confetti {{ position: absolute; inset: 0; }}
.c {{ position: absolute; width: 12px; height: 4px; border-radius: 2px; }}
.c.sq {{ width: 8px; height: 8px; border-radius: 1px; }}
.c.tri {{ width: 0; height: 0; border-left: 6px solid transparent; border-right: 6px solid transparent; border-bottom: 10px solid; background: transparent !important; }}
.glow-ring {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 540px; height: 540px;
  border-radius: 50%; box-shadow: 0 0 100px 30px rgba(139,92,246,0.3), 0 0 200px 60px rgba(20,184,166,0.15); opacity: 0.8; }}
.top {{ position: absolute; top: 36px; left: 48px; right: 48px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
.logo {{ font-weight: 800; font-size: 24px; letter-spacing: -0.02em; }}
.logo span {{ background: linear-gradient(135deg, #c4b5fd, #5eead4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
.pill {{ padding: 8px 18px; background: rgba(255,255,255,0.1); backdrop-filter: blur(8px); border: 1px solid rgba(255,255,255,0.18); color: #fff; border-radius: 100px; font-size: 13px; font-weight: 600; letter-spacing: 0.04em; }}
.center {{ position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); text-align: center; z-index: 8; }}
.kicker {{ font-size: 13px; color: rgba(255,255,255,0.7); letter-spacing: 0.22em; text-transform: uppercase; margin-bottom: 12px; font-weight: 700; }}
.num {{ font-size: {metric_size}px; font-weight: 900; line-height: 0.88; letter-spacing: -0.06em;
  background: linear-gradient(135deg, #fff 0%, #c4b5fd 40%, #5eead4 80%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 0 50px rgba(196,181,253,0.5)); }}
.ttl {{ font-size: 26px; font-weight: 800; letter-spacing: -0.02em; margin-top: 16px; }}
.bot {{ position: absolute; bottom: 36px; left: 48px; right: 48px; display: flex; justify-content: space-between; align-items: end; z-index: 10; }}
.meta {{ font-size: 14px; color: rgba(255,255,255,0.65); }}
.arr {{ font-size: 16px; font-weight: 700; background: linear-gradient(135deg, #c4b5fd, #5eead4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
</style></head><body>
<div class="og">
  <div class="rays"></div>
  <div class="confetti">
    <div class="c"     style="top: 8%;  left: 12%; background: #8B5CF6; transform: rotate(35deg);"></div>
    <div class="c sq"  style="top: 14%; left: 28%; background: #14B8A6; transform: rotate(15deg);"></div>
    <div class="c"     style="top: 22%; left: 6%;  background: #EC4899; transform: rotate(-40deg);"></div>
    <div class="c tri" style="top: 6%;  left: 80%; border-bottom-color: #EAB308; transform: rotate(20deg);"></div>
    <div class="c"     style="top: 18%; left: 88%; background: #3B82F6; transform: rotate(-25deg);"></div>
    <div class="c sq"  style="top: 28%; left: 92%; background: #FB923C; transform: rotate(45deg);"></div>
    <div class="c"     style="top: 70%; left: 8%;  background: #EAB308; transform: rotate(60deg);"></div>
    <div class="c tri" style="top: 78%; left: 22%; border-bottom-color: #EC4899; transform: rotate(-30deg);"></div>
    <div class="c sq"  style="top: 84%; left: 14%; background: #14B8A6; transform: rotate(20deg);"></div>
    <div class="c"     style="top: 72%; left: 84%; background: #8B5CF6; transform: rotate(-50deg);"></div>
    <div class="c sq"  style="top: 82%; left: 92%; background: #3B82F6; transform: rotate(30deg);"></div>
    <div class="c tri" style="top: 88%; left: 76%; border-bottom-color: #14B8A6; transform: rotate(15deg);"></div>
    <div class="c"     style="top: 40%; left: 4%;  background: #c4b5fd; transform: rotate(70deg);"></div>
    <div class="c sq"  style="top: 56%; left: 96%; background: #5eead4; transform: rotate(-20deg);"></div>
  </div>
  <div class="glow-ring"></div>
  <div class="top"><div class="logo">10×<span>SEO</span></div><span class="pill">⬢ {industry} · {tf}</span></div>
  <div class="center">
    <div class="kicker">{kicker}</div>
    <div class="num">{metric}</div>
    <div class="ttl">{title}</div>
  </div>
  <div class="bot"><span class="meta">{bottom}</span><span class="arr">10xseo.ge →</span></div>
</div></body></html>
"""

def screenshot(html_path, out_png):
    subprocess.run([
        CHROME, "--headless", "--disable-gpu", "--no-sandbox",
        "--hide-scrollbars", "--window-size=1200,800",
        "--default-background-color=000000ff",
        f"--screenshot={out_png}",
        f"file://{html_path}",
    ], capture_output=True)

def crop_to_og(src_png, dst_jpg):
    img = Image.open(src_png).convert("RGB")
    body_rgb = (26, 26, 26)
    start = 0
    for y in range(0, img.size[1]):
        px = img.getpixel((600, y))
        if any(abs(px[i] - body_rgb[i]) > 5 for i in range(3)):
            start = y; break
    cropped = img.crop((0, start, 1200, start + 630))
    cropped.save(dst_jpg, "JPEG", quality=90, optimize=True, progressive=True)

def main():
    templates = {"vD": TPL_D, "vE": TPL_E, "vF": TPL_F, "vG": TPL_G, "vH": TPL_H}
    print(f"Generating {len(CASES)} cases × {len(templates)} designs = {len(CASES)*len(templates)} variants")
    print("=" * 70)
    for vkey, tpl in templates.items():
        for c in CASES:
            data = dict(c)
            data["title_short"] = c["title"][:24]
            html = tpl.format(**data)
            html_path = HTML_BASE / vkey / f"{c['slug']}.html"
            html_path.write_text(html, encoding="utf-8")
            raw = HTML_BASE / vkey / f"_raw_{c['slug']}.png"
            screenshot(html_path, raw)
            final = PNG_BASE / vkey / f"{c['og']}.jpg"
            crop_to_og(raw, final)
            raw.unlink()
            print(f"  ✓ {vkey} · {c['slug']:40} → {final.name}")

if __name__ == "__main__":
    main()
