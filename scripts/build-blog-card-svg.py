#!/usr/bin/env python3
"""Generate 10xSEO-branded blog card thumbnails as SVG.

Matches the existing KA card style:
- Dark navy radial gradient background with bright blue center
- "10xSEO" wordmark at top (10x white, SEO gold)
- Main topic in large white bold uppercase
- Subtitle in gold bold uppercase
- "WWW.10XSEO.GE" with cursor icon at bottom

Output: 1200x630 SVG files (16:9 ratio, same slot as existing webp).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "images" / "blog"

CARDS = [
    {
        "slug": "what-is-aeo",
        "topic": "WHAT IS AEO?",
        "subtitle": "ANSWER ENGINE OPTIMIZATION",
        "topic_size": 80,
        "subtitle_size": 38,
    },
    {
        "slug": "aeo-optimization-agency-dubai",
        "topic": "AEO DUBAI",
        "subtitle": "CHATGPT SEO FOR UAE",
        "topic_size": 96,
        "subtitle_size": 42,
    },
]


def render(card: dict) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630" role="img" aria-label="{card['topic']} — {card['subtitle']}">
  <defs>
    <radialGradient id="bg-{card['slug']}" cx="50%" cy="42%" r="68%">
      <stop offset="0%" stop-color="#1e40af" stop-opacity="0.9"/>
      <stop offset="45%" stop-color="#1e1b4b" stop-opacity="1"/>
      <stop offset="100%" stop-color="#0a0a2e" stop-opacity="1"/>
    </radialGradient>
    <filter id="glow-{card['slug']}" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="1200" height="630" fill="url(#bg-{card['slug']})"/>

  <!-- Subtle blue glow accent (center) -->
  <ellipse cx="600" cy="320" rx="350" ry="200" fill="#3b82f6" opacity="0.18"/>

  <!-- 10xSEO wordmark (top center) -->
  <g transform="translate(600, 145)">
    <text text-anchor="middle" font-family="Inter, -apple-system, sans-serif"
          font-size="58" font-weight="900" letter-spacing="-1">
      <tspan fill="#ffffff">10x</tspan><tspan fill="#D4A017">SEO</tspan>
    </text>
  </g>

  <!-- Main topic -->
  <text x="600" y="315" text-anchor="middle"
        font-family="Inter, -apple-system, sans-serif"
        font-size="{card['topic_size']}" font-weight="900" fill="#ffffff"
        letter-spacing="-2"
        filter="url(#glow-{card['slug']})">{card['topic']}</text>

  <!-- Subtitle -->
  <text x="600" y="400" text-anchor="middle"
        font-family="Inter, -apple-system, sans-serif"
        font-size="{card['subtitle_size']}" font-weight="700" fill="#D4A017"
        letter-spacing="3">{card['subtitle']}</text>

  <!-- WWW.10XSEO.GE + cursor (bottom) -->
  <g transform="translate(600, 555)">
    <text text-anchor="middle" font-family="Inter, -apple-system, sans-serif"
          font-size="28" font-weight="800" fill="#ffffff" letter-spacing="3">WWW.10XSEO.GE</text>
    <!-- Cursor pointer icon, positioned right of text -->
    <g transform="translate(168, -6)">
      <path d="M0 0 L0 22 L6 16 L10 24 L13 23 L9 15 L17 15 Z"
            fill="#D4A017" stroke="#ffffff" stroke-width="0.5"/>
    </g>
  </g>
</svg>
"""


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for card in CARDS:
        path = OUT_DIR / f"{card['slug']}-card.svg"
        path.write_text(render(card), encoding="utf-8")
        print(f"✓ Wrote {path.relative_to(ROOT)} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
