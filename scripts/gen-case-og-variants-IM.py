#!/usr/bin/env python3
"""
5 more design variants (I-M):
  I · Isometric 3D Dashboard — tilted dashboard mockup, SaaS feel
  J · Newspaper Broadsheet — vintage masthead + huge serif headline
  K · Pop Art Halftone — Lichtenstein dots + bold colors + speech burst
  L · Liquid Mercury — organic gooey metaball blobs, futuristic
  M · Architectural Blueprint — technical drawing on blueprint paper
"""
import importlib.util
import subprocess
from pathlib import Path
from PIL import Image

ROOT = Path("/Users/imac/SEO/command-center")
HTML_BASE = ROOT / "og-per-case"
PNG_BASE = ROOT / "og-previews" / "per-case"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

for v in ["vI", "vJ", "vK", "vL", "vM"]:
    (HTML_BASE / v).mkdir(parents=True, exist_ok=True)
    (PNG_BASE / v).mkdir(parents=True, exist_ok=True)

# Reuse CASES from previous gen script
spec = importlib.util.spec_from_file_location("prev", ROOT / "scripts" / "gen-case-og-variants-DH.py")
prev = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prev)
CASES = prev.CASES

# ============== I · ISOMETRIC 3D DASHBOARD ==============
TPL_I = """<!DOCTYPE html><html lang="ka"><head><meta charset="UTF-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ background: #1a1a1a; min-height: 100vh; display: flex; align-items: center; justify-content: center; font-family: 'Inter', sans-serif; }}
.og {{
  width: 1200px; height: 630px; position: relative; overflow: hidden;
  background:
    radial-gradient(circle at 80% 30%, rgba(139,92,246,0.18) 0%, transparent 50%),
    radial-gradient(circle at 20% 80%, rgba(20,184,166,0.14) 0%, transparent 50%),
    linear-gradient(135deg, #050818 0%, #0a0d1f 100%);
  color: #fff;
}}
.grid-bg {{ position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px);
  background-size: 40px 40px;
  mask-image: radial-gradient(ellipse 70% 60% at 60% 50%, #000 30%, transparent 100%);
}}
.top {{ position: absolute; top: 32px; left: 48px; right: 48px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
.logo {{ font-weight: 800; font-size: 22px; letter-spacing: -0.02em; }}
.logo span {{ background: linear-gradient(135deg, #8B5CF6, #14B8A6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
.pill {{ padding: 6px 14px; background: rgba(139,92,246,0.15); border: 1px solid rgba(139,92,246,0.4); color: #c4b5fd; border-radius: 100px; font-size: 12px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; }}

.scene {{ position: absolute; left: 50%; top: 50%; transform: translate(-50%, -47%) rotateX(50deg) rotateZ(-30deg); transform-style: preserve-3d; width: 760px; height: 480px; }}
.iso-card {{ position: absolute; border-radius: 18px; box-shadow: 0 30px 60px rgba(0,0,0,0.5); }}
.iso-base {{ left: 0; top: 0; width: 760px; height: 480px;
  background: linear-gradient(135deg, #1a1f3a 0%, #11142a 100%);
  border: 1px solid rgba(255,255,255,0.08); padding: 36px; }}
.dash-head {{ display: flex; justify-content: space-between; align-items: center; padding-bottom: 16px; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 18px; }}
.dash-head .t {{ font-size: 13px; color: rgba(255,255,255,0.6); letter-spacing: 0.08em; text-transform: uppercase; font-weight: 600; }}
.dash-head .live {{ display: flex; align-items: center; gap: 6px; font-size: 11px; color: #5eead4; }}
.dash-head .live::before {{ content: ''; width: 8px; height: 8px; border-radius: 50%; background: #5eead4; box-shadow: 0 0 8px #5eead4; }}
.dash-kpi {{ display: grid; grid-template-columns: 1.6fr 1fr; gap: 16px; height: calc(100% - 76px); }}
.kpi-main {{ background: linear-gradient(135deg, rgba(139,92,246,0.18) 0%, rgba(20,184,166,0.12) 100%); border: 1px solid rgba(255,255,255,0.12); border-radius: 14px; padding: 22px; display: flex; flex-direction: column; justify-content: space-between; }}
.kpi-main .k {{ font-size: 12px; color: rgba(255,255,255,0.65); letter-spacing: 0.12em; text-transform: uppercase; font-weight: 600; }}
.kpi-main .n {{ font-size: {metric_size_iso}px; font-weight: 900; line-height: 0.9; letter-spacing: -0.05em;
  background: linear-gradient(180deg, #fff 0%, #c4b5fd 50%, #5eead4 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
.kpi-main .delta {{ font-size: 13px; color: #5eead4; font-weight: 700; }}
.kpi-side {{ display: grid; grid-template-rows: 1fr 1fr; gap: 12px; }}
.kpi-tile {{ background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 14px; }}
.kpi-tile .l {{ font-size: 10px; color: rgba(255,255,255,0.55); letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 8px; }}
.kpi-tile .v {{ font-size: 18px; font-weight: 800; color: #fff; }}
.kpi-tile .bars {{ display: flex; gap: 3px; align-items: end; margin-top: 8px; height: 30px; }}
.kpi-tile .bars span {{ flex: 1; background: linear-gradient(180deg, #8B5CF6, #14B8A6); border-radius: 2px 2px 0 0; }}
.kpi-tile .spark {{ width: 100%; height: 28px; margin-top: 6px; }}

.content {{ position: absolute; top: 110px; left: 48px; z-index: 12; max-width: 480px; }}
.kicker {{ font-size: 13px; color: #c4b5fd; letter-spacing: 0.18em; text-transform: uppercase; margin-bottom: 10px; font-weight: 700; }}
h1 {{ font-size: 42px; font-weight: 900; line-height: 1.05; letter-spacing: -0.03em; }}
.deck {{ font-size: 14px; color: rgba(255,255,255,0.65); margin-top: 14px; line-height: 1.5; }}

.bot {{ position: absolute; bottom: 28px; left: 48px; right: 48px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
.bot .meta {{ font-size: 12px; color: rgba(255,255,255,0.55); }}
.bot .arr {{ font-size: 14px; color: #c4b5fd; font-weight: 700; }}
</style></head><body>
<div class="og">
  <div class="grid-bg"></div>
  <div class="top"><div class="logo">10×<span>SEO</span></div><span class="pill">⬢ {industry} · {tf}</span></div>
  <div class="scene">
    <div class="iso-card iso-base">
      <div class="dash-head"><div class="t">10xseo · case dashboard</div><div class="live">LIVE</div></div>
      <div class="dash-kpi">
        <div class="kpi-main">
          <div class="k">{kicker}</div>
          <div class="n">{metric}</div>
          <div class="delta">↑ since baseline</div>
        </div>
        <div class="kpi-side">
          <div class="kpi-tile">
            <div class="l">TRAFFIC</div><div class="v">+{growth_short}</div>
            <div class="bars"><span style="height:30%"></span><span style="height:45%"></span><span style="height:62%"></span><span style="height:78%"></span><span style="height:92%"></span><span style="height:100%"></span></div>
          </div>
          <div class="kpi-tile">
            <div class="l">TIMEFRAME</div><div class="v">{tf}</div>
            <svg class="spark" viewBox="0 0 100 28" preserveAspectRatio="none"><polyline points="0,26 20,22 40,16 60,10 80,5 100,2" fill="none" stroke="#5eead4" stroke-width="2"/></svg>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="content">
    <div class="kicker">{kicker}</div>
    <h1>{title}</h1>
    <div class="deck">{bottom}</div>
  </div>
  <div class="bot"><span class="meta">10xseo.ge/case-studies</span><span class="arr">სრული ისტორია →</span></div>
</div></body></html>
"""

# ============== J · NEWSPAPER BROADSHEET ==============
TPL_J = """<!DOCTYPE html><html lang="ka"><head><meta charset="UTF-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Lora:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ background: #1a1a1a; min-height: 100vh; display: flex; align-items: center; justify-content: center; font-family: 'Lora', Georgia, serif; }}
.og {{
  width: 1200px; height: 630px; position: relative; overflow: hidden;
  background: #f5efe1;
  background-image:
    radial-gradient(circle at 30% 20%, rgba(0,0,0,0.015) 0, transparent 30%),
    radial-gradient(circle at 70% 80%, rgba(0,0,0,0.02) 0, transparent 30%),
    repeating-linear-gradient(0deg, transparent 0, transparent 25px, rgba(0,0,0,0.012) 25px, rgba(0,0,0,0.012) 26px);
  color: #0a0a0a; padding: 28px 50px;
}}
.masthead {{ display: flex; justify-content: space-between; align-items: baseline; border-bottom: 1.5px solid #000; padding-bottom: 8px; }}
.name {{ font-family: 'Playfair Display', serif; font-weight: 900; font-size: 38px; letter-spacing: -0.02em; }}
.name em {{ font-style: italic; font-weight: 400; }}
.date {{ font-family: 'Playfair Display', serif; font-style: italic; font-size: 13px; }}
.subhead {{ display: flex; justify-content: space-between; border-top: 1px solid #000; border-bottom: 4px double #000; padding: 4px 0; margin-bottom: 24px; font-size: 11px; letter-spacing: 0.2em; text-transform: uppercase; font-weight: 700; }}

.breaking {{ display: inline-block; background: #BC1F26; color: #fff; padding: 3px 10px; font-size: 11px; letter-spacing: 0.18em; text-transform: uppercase; font-weight: 800; font-family: 'Lora', serif; margin-bottom: 12px; }}
.deck {{ font-family: 'Playfair Display', serif; font-style: italic; font-size: 17px; color: #444; margin-bottom: 12px; line-height: 1.45; }}
h1 {{ font-family: 'Playfair Display', serif; font-weight: 900; font-size: 76px; line-height: 0.95; letter-spacing: -0.025em; margin-bottom: 16px; }}
h1 em {{ font-style: italic; color: #BC1F26; }}

.metric-line {{ display: flex; align-items: baseline; gap: 20px; border-top: 1px solid rgba(0,0,0,0.4); border-bottom: 1px solid rgba(0,0,0,0.4); padding: 14px 0; margin-top: 4px; }}
.metric-line .m {{ font-family: 'Playfair Display', serif; font-weight: 900; font-size: 120px; letter-spacing: -0.05em; line-height: 0.85; color: #BC1F26; }}
.metric-line .ml {{ font-style: italic; font-size: 18px; color: #444; }}
.metric-line .tf-c {{ margin-left: auto; text-align: right; }}
.metric-line .tf-c .v {{ font-family: 'Playfair Display', serif; font-weight: 900; font-size: 30px; line-height: 1; }}
.metric-line .tf-c .l {{ font-size: 11px; color: #444; letter-spacing: 0.15em; text-transform: uppercase; margin-top: 2px; }}

.bot {{ position: absolute; bottom: 22px; left: 50px; right: 50px; display: flex; justify-content: space-between; align-items: end; border-top: 1px solid rgba(0,0,0,0.3); padding-top: 10px; font-size: 11px; letter-spacing: 0.12em; text-transform: uppercase; color: #444; }}
.bot .b {{ font-family: 'Playfair Display', serif; font-style: italic; color: #BC1F26; text-transform: none; letter-spacing: 0; font-size: 14px; border-bottom: 1px solid #BC1F26; padding-bottom: 1px; }}
</style></head><body>
<div class="og">
  <header class="masthead">
    <div class="name">10×SEO <em>· The Daily</em></div>
    <div class="date">{year} · ISSUE №{issue}</div>
  </header>
  <div class="subhead"><span>10XSEO.GE</span><span>CASE STUDY · {industry}</span><span>VOL III</span></div>
  <span class="breaking">★ Breaking</span>
  <h1>{title}</h1>
  <div class="deck">{kicker} — {bottom}.</div>
  <div class="metric-line">
    <div class="m">{metric}</div>
    <div class="ml">{kicker}</div>
    <div class="tf-c"><div class="v">{tf}</div><div class="l">timeframe</div></div>
  </div>
  <div class="bot"><span>Continued on page 2</span><span class="b">10xseo.ge/case-studies →</span></div>
</div></body></html>
"""

# ============== K · POP ART HALFTONE ==============
TPL_K = """<!DOCTYPE html><html lang="ka"><head><meta charset="UTF-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800;900&family=Bungee&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ background: #1a1a1a; min-height: 100vh; display: flex; align-items: center; justify-content: center; font-family: 'Inter', sans-serif; }}
.og {{
  width: 1200px; height: 630px; position: relative; overflow: hidden;
  background: #fef7d7;
  background-image:
    radial-gradient(circle at 1px 1px, rgba(0,0,0,0.25) 1px, transparent 0);
  background-size: 14px 14px;
  color: #1a1a1a;
}}
.bg-burst {{ position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); width: 1000px; height: 1000px;
  background: conic-gradient(from 0deg, #ff5e3a 0deg 22.5deg, #fdd119 22.5deg 45deg, #ff5e3a 45deg 67.5deg, #fdd119 67.5deg 90deg, #ff5e3a 90deg 112.5deg, #fdd119 112.5deg 135deg, #ff5e3a 135deg 157.5deg, #fdd119 157.5deg 180deg, #ff5e3a 180deg 202.5deg, #fdd119 202.5deg 225deg, #ff5e3a 225deg 247.5deg, #fdd119 247.5deg 270deg, #ff5e3a 270deg 292.5deg, #fdd119 292.5deg 315deg, #ff5e3a 315deg 337.5deg, #fdd119 337.5deg 360deg);
  opacity: 0.55; clip-path: circle(46% at center); }}
.bg-circle {{ position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); width: 720px; height: 720px;
  border-radius: 50%; background: radial-gradient(circle, #fdd119 0%, transparent 70%); opacity: 0.85; }}

.top {{ position: absolute; top: 28px; left: 40px; right: 40px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
.logo {{ font-family: 'Bungee', sans-serif; font-size: 22px; letter-spacing: 0.02em; color: #1a1a1a; }}
.logo span {{ color: #ff5e3a; }}
.pill {{ font-family: 'Bungee', sans-serif; font-size: 11px; padding: 6px 14px; background: #1a1a1a; color: #fdd119; border: 3px solid #1a1a1a; letter-spacing: 0.08em; text-transform: uppercase; }}

.zap {{ position: absolute; left: 50%; top: 48%; transform: translate(-50%, -50%) rotate(-6deg); z-index: 8;
  width: 760px; padding: 24px 36px; background: #fff;
  border: 6px solid #1a1a1a; box-shadow: 12px 12px 0 #1a1a1a; text-align: center; }}
.bubble-tail {{ position: absolute; bottom: -36px; left: 80px; width: 0; height: 0;
  border-left: 26px solid transparent; border-right: 26px solid transparent; border-top: 40px solid #1a1a1a; }}
.bubble-tail::before {{ content: ''; position: absolute; top: -52px; left: -19px;
  border-left: 19px solid transparent; border-right: 19px solid transparent; border-top: 28px solid #fff; }}
.zap .kicker {{ font-family: 'Bungee', sans-serif; font-size: 18px; color: #ff5e3a; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 8px; }}
.zap .num {{ font-family: 'Bungee', sans-serif; font-size: {metric_size_pop}px; line-height: 0.9; letter-spacing: -0.02em; color: #1a1a1a; -webkit-text-stroke: 1px #1a1a1a;
  text-shadow: 6px 6px 0 #ff5e3a; }}
.zap .ttl {{ font-family: 'Bungee', sans-serif; font-size: 22px; line-height: 1; letter-spacing: 0; color: #1a1a1a; margin-top: 10px; }}

.bot {{ position: absolute; bottom: 24px; left: 40px; right: 40px; display: flex; justify-content: space-between; align-items: center; z-index: 10; font-family: 'Bungee', sans-serif; }}
.bot .meta {{ font-size: 11px; color: #1a1a1a; letter-spacing: 0.1em; text-transform: uppercase; }}
.bot .arr {{ font-size: 16px; color: #ff5e3a; letter-spacing: 0.05em; }}
</style></head><body>
<div class="og">
  <div class="bg-circle"></div><div class="bg-burst"></div>
  <div class="top"><div class="logo">10×<span>SEO</span>!</div><span class="pill">★ {industry} · {tf}</span></div>
  <div class="zap">
    <div class="kicker">{kicker_short_pop}!</div>
    <div class="num">{metric}</div>
    <div class="ttl">{title_pop}</div>
    <div class="bubble-tail"></div>
  </div>
  <div class="bot"><span class="meta">{bottom}</span><span class="arr">10xseo.ge ↗</span></div>
</div></body></html>
"""

# ============== L · LIQUID MERCURY ==============
TPL_L = """<!DOCTYPE html><html lang="ka"><head><meta charset="UTF-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800;900&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ background: #1a1a1a; min-height: 100vh; display: flex; align-items: center; justify-content: center; font-family: 'Inter', sans-serif; }}
.og {{
  width: 1200px; height: 630px; position: relative; overflow: hidden;
  background: linear-gradient(135deg, #0a0a1a 0%, #1a0a2a 50%, #0a1a2a 100%);
  color: #fff;
}}
.metaball-wrap {{ position: absolute; inset: 0; filter: blur(0px) contrast(1.4); }}
.blob {{ position: absolute; border-radius: 50%; filter: blur(45px); }}
.b1 {{ width: 520px; height: 520px; top: -80px; left: -100px;
  background: radial-gradient(circle at 30% 30%, #fff, #c4b5fd 30%, #8B5CF6 60%, #6D28D9); }}
.b2 {{ width: 460px; height: 460px; top: 50px; right: -80px;
  background: radial-gradient(circle at 70% 30%, #fff, #5eead4 30%, #14B8A6 60%, #0F766E); }}
.b3 {{ width: 380px; height: 380px; bottom: -100px; left: 30%;
  background: radial-gradient(circle at 50% 50%, #fff, #f9a8d4 30%, #EC4899 60%, #BE185D); }}
.b4 {{ width: 280px; height: 280px; top: 35%; left: 45%;
  background: radial-gradient(circle at 50% 30%, #fff, #93c5fd 30%, #3B82F6 60%); }}
.mercury-shine {{ position: absolute; inset: 0; background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, transparent 50%, rgba(255,255,255,0.04) 100%); pointer-events: none; }}
.veil {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,0.15) 0%, rgba(0,0,0,0.45) 100%); }}

.content {{ position: absolute; inset: 0; padding: 56px 64px; display: flex; flex-direction: column; justify-content: space-between; z-index: 10; }}
.top {{ display: flex; justify-content: space-between; align-items: center; }}
.logo {{ font-weight: 800; font-size: 24px; letter-spacing: -0.02em; }}
.logo span {{ background: linear-gradient(135deg, #fff, #c4b5fd); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
.pill {{ padding: 8px 18px; background: rgba(255,255,255,0.14); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.32); color: #fff; border-radius: 100px; font-size: 13px; font-weight: 700; letter-spacing: 0.04em; }}
.mid {{ text-align: center; }}
.kicker {{ font-size: 13px; color: rgba(255,255,255,0.7); letter-spacing: 0.22em; text-transform: uppercase; margin-bottom: 14px; font-weight: 700; }}
.num {{ font-size: {metric_size}px; font-weight: 900; line-height: 0.88; letter-spacing: -0.06em; color: #fff;
  text-shadow: 0 0 60px rgba(255,255,255,0.4), 0 4px 24px rgba(0,0,0,0.4);
  background: linear-gradient(180deg, #fff 0%, rgba(255,255,255,0.7) 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
.ttl {{ font-size: 30px; font-weight: 800; letter-spacing: -0.02em; margin-top: 16px; color: #fff; text-shadow: 0 2px 16px rgba(0,0,0,0.5); }}
.bot {{ display: flex; justify-content: space-between; align-items: end; }}
.meta {{ font-size: 14px; color: rgba(255,255,255,0.75); text-shadow: 0 1px 6px rgba(0,0,0,0.4); }}
.arr {{ font-size: 16px; color: #fff; font-weight: 700; text-shadow: 0 1px 6px rgba(0,0,0,0.4); }}
</style></head><body>
<div class="og">
  <div class="metaball-wrap">
    <div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div><div class="blob b4"></div>
  </div>
  <div class="mercury-shine"></div>
  <div class="veil"></div>
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

# ============== M · ARCHITECTURAL BLUEPRINT ==============
TPL_M = """<!DOCTYPE html><html lang="ka"><head><meta charset="UTF-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Special+Elite&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ background: #1a1a1a; min-height: 100vh; display: flex; align-items: center; justify-content: center; font-family: 'Inter', sans-serif; }}
.og {{
  width: 1200px; height: 630px; position: relative; overflow: hidden;
  background: #0c2845;
  background-image:
    linear-gradient(rgba(255,255,255,0.045) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.045) 1px, transparent 1px),
    linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px),
    radial-gradient(ellipse at center, rgba(255,255,255,0.04) 0%, transparent 80%);
  background-size: 60px 60px, 60px 60px, 12px 12px, 12px 12px, 100% 100%;
  color: #cfe4ff;
}}
.title-block {{ position: absolute; top: 30px; left: 50px; right: 50px;
  border: 1px solid rgba(207,228,255,0.4); padding: 16px 22px;
  display: flex; justify-content: space-between; align-items: center; background: rgba(12,40,69,0.4); }}
.title-block .logo {{ font-weight: 800; font-size: 20px; letter-spacing: -0.02em; color: #fff; }}
.title-block .logo span {{ color: #5eead4; }}
.title-block .info {{ display: flex; gap: 28px; font-family: 'Special Elite', monospace; font-size: 11px; color: rgba(207,228,255,0.7); letter-spacing: 0.1em; text-transform: uppercase; }}
.title-block .info span strong {{ color: #fff; margin-left: 6px; }}

.diagram {{ position: absolute; left: 50%; top: 52%; transform: translate(-50%, -50%); text-align: center; }}
.dim-line {{ display: flex; align-items: center; gap: 12px; margin-bottom: 14px; justify-content: center; }}
.dim-line .l {{ flex: 0 0 80px; height: 1px; background: #5eead4; position: relative; }}
.dim-line .l::before {{ content: ''; position: absolute; left: 0; top: -3px; width: 6px; height: 7px; border: 1px solid #5eead4; border-right: none; }}
.dim-line .l::after  {{ content: ''; position: absolute; right: 0; top: -3px; width: 6px; height: 7px; border: 1px solid #5eead4; border-left: none; }}
.dim-line .m {{ font-family: 'Special Elite', monospace; font-size: 11px; color: #5eead4; letter-spacing: 0.15em; text-transform: uppercase; }}
.num {{ font-size: {metric_size}px; font-weight: 800; line-height: 0.9; letter-spacing: -0.04em; color: #fff;
  text-shadow: 0 0 30px rgba(94,234,212,0.3); margin-bottom: 6px; }}
.num-frame {{ display: inline-block; padding: 18px 36px; border: 1.5px solid #5eead4; position: relative; }}
.num-frame::before {{ content: ''; position: absolute; top: -6px; left: -6px; width: 14px; height: 14px; border-top: 2px solid #fff; border-left: 2px solid #fff; }}
.num-frame::after  {{ content: ''; position: absolute; top: -6px; right: -6px; width: 14px; height: 14px; border-top: 2px solid #fff; border-right: 2px solid #fff; }}
.num-frame .corner-bl {{ position: absolute; bottom: -6px; left: -6px; width: 14px; height: 14px; border-bottom: 2px solid #fff; border-left: 2px solid #fff; }}
.num-frame .corner-br {{ position: absolute; bottom: -6px; right: -6px; width: 14px; height: 14px; border-bottom: 2px solid #fff; border-right: 2px solid #fff; }}
.ttl {{ font-family: 'Special Elite', monospace; font-size: 22px; color: #fff; letter-spacing: 0.05em; margin-top: 20px; }}
.deck {{ font-family: 'Special Elite', monospace; font-size: 12px; color: rgba(207,228,255,0.65); letter-spacing: 0.1em; margin-top: 8px; text-transform: uppercase; }}

.notes {{ position: absolute; bottom: 26px; left: 50px; right: 50px;
  border-top: 1px solid rgba(207,228,255,0.4); padding-top: 10px;
  display: flex; justify-content: space-between; font-family: 'Special Elite', monospace; font-size: 10px; color: rgba(207,228,255,0.6); letter-spacing: 0.12em; text-transform: uppercase; }}
.notes .arr {{ color: #5eead4; }}

.corner {{ position: absolute; width: 20px; height: 20px; border-color: #5eead4; }}
.tl {{ top: 8px; left: 8px; border-top: 1px solid; border-left: 1px solid; }}
.tr {{ top: 8px; right: 8px; border-top: 1px solid; border-right: 1px solid; }}
.bl {{ bottom: 8px; left: 8px; border-bottom: 1px solid; border-left: 1px solid; }}
.br {{ bottom: 8px; right: 8px; border-bottom: 1px solid; border-right: 1px solid; }}
</style></head><body>
<div class="og">
  <div class="corner tl"></div><div class="corner tr"></div><div class="corner bl"></div><div class="corner br"></div>
  <div class="title-block">
    <div class="logo">10×<span>SEO</span></div>
    <div class="info">
      <span>DWG №<strong>{issue}</strong></span>
      <span>SCALE<strong>1:1</strong></span>
      <span>DATE<strong>{year}</strong></span>
      <span>SECTOR<strong>{industry}</strong></span>
    </div>
  </div>
  <div class="diagram">
    <div class="dim-line"><div class="l"></div><div class="m">{kicker}</div><div class="l"></div></div>
    <div class="num-frame">
      <div class="num">{metric}</div>
      <span class="corner-bl"></span><span class="corner-br"></span>
    </div>
    <div class="ttl">{title}</div>
    <div class="deck">— {bottom} —</div>
  </div>
  <div class="notes"><span>BLUEPRINT · 10XSEO.GE/CASE-STUDIES</span><span class="arr">SHEET 1 OF 1 — APPROVED ✓</span></div>
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

# Per-case derived data for chapter / issue numbers
ISSUE_MAP = {"I":"001","II":"002","III":"003","IV":"004","V":"005","VI":"006","VII":"007","VIII":"008"}

def main():
    templates = {"vI": TPL_I, "vJ": TPL_J, "vK": TPL_K, "vL": TPL_L, "vM": TPL_M}
    # Compute derived fields
    chapters = ["I","II","III","IV","V","VI","VII","VII","VIII"]  # match CASES order
    for i, c in enumerate(CASES):
        c["issue"] = ISSUE_MAP.get(chapters[i], "001")
        # Growth short string for Iso tile
        m = c["metric"]
        if "%" in m: c["growth_short"] = m.replace("+","").replace("%","%")
        elif "×" in m or "x" in m: c["growth_short"] = m + "x"
        elif "TOP" in m: c["growth_short"] = "TOP"
        elif "+" in m: c["growth_short"] = m.replace(",","")[:6]
        else: c["growth_short"] = m[:6]
        # Iso metric size — slightly smaller for tile
        c["metric_size_iso"] = int(c["metric_size"] * 0.55)
        # Pop art metric size — same scale
        c["metric_size_pop"] = int(c["metric_size"] * 0.62)
        # Short title for pop
        c["title_pop"] = c["title"][:24]
        c["kicker_short_pop"] = c["kicker"][:22]

    print(f"Generating {len(CASES)} cases × {len(templates)} designs = {len(CASES)*len(templates)} variants")
    print("=" * 70)
    for vkey, tpl in templates.items():
        for c in CASES:
            data = dict(c); data["title_short"] = c["title"][:24]
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
