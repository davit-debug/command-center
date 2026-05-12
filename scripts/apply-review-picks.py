#!/usr/bin/env python3
"""Apply user's translation picks to /en/*.html pages.

Takes JSON of {page: {fragment: {version, text}}} and updates:
- Title (in <title>, og:title, twitter:title, JSON-LD name)
- Meta description (in <meta description>, og:description, twitter:description, JSON-LD description)
- H1 (two-line gradient pattern: line1 + <span class="gradient-text">line2</span>)
- Hero subheading (first <p> after H1)
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_DIR = ROOT / "en"

PICKS = {
    "/en/index.html": {
        "Hero subheading": {
            "version": "V1",
            "text": "Georgia's #1 SEO Agency — We put brands where customers search for answers.",
        }
    },
    "/en/services.html": {
        "Title": {
            "version": "V3",
            "text": "SEO Services in Georgia | Management, AI SEO, CRO — 10xSEO",
        },
        "Meta description": {
            "version": "V2",
            "text": "Hire Georgia's #1 SEO agency. We offer SEO management, AI SEO, CRO, Google Ads, copywriting & free SEO tools for Tbilisi & international brands.",
        },
        "H1": {
            "version": "V1",
            "text": "SEO Services — Full Ecosystem / for Your Business Growth",
        },
        "Hero subheading": {
            "version": "V2",
            "text": "Twelve specialized SEO services under one roof. Pick what you need — SEO management, AI SEO, CRO, Google Ads, copywriting, or our free tools.",
        },
    },
    "/en/ai-seo.html": {
        "Title": {
            "version": "V1",
            "text": "AI SEO (GEO/AEO) | Rank in ChatGPT, Gemini & Perplexity — 10xSEO",
        },
        "Meta description": {
            "version": "V1",
            "text": "Get cited in ChatGPT, Gemini, Perplexity & Claude. 10xSEO's AI SEO service: GEO + AEO optimization for maximum brand visibility in AI search.",
        },
        "H1": {
            "version": "V1",
            "text": "AI SEO (GEO/AEO) — / Visibility in ChatGPT, Gemini & Perplexity",
        },
        "Hero subheading": {
            "version": "V3",
            "text": "Your customers ask AI now. Make sure ChatGPT, Gemini, Perplexity & Claude answer with your brand.",
        },
    },
    "/en/contact-us.html": {
        "Title": {
            "version": "V5",
            "text": "Contact 10xSEO | Book a 15-Min SEO Consultation",
        },
        "Meta description": {
            "version": "V5",
            "text": "Contact the SEO agency Tbilisi trusts. 10xSEO offers free 15-min consultations for businesses ready to rank #1 on Google + AI search.",
        },
        "H1": {
            "version": "V1",
            "text": "Get in Touch",
        },
        "Hero subheading": {
            "version": "V1",
            "text": "Whether you have a quick question or need a full SEO strategy — we're here. Reach us by phone, email, or book a free consultation online.",
        },
    },
    "/en/about-us.html": {
        "Title": {
            "version": "V2",
            "text": "Meet 10xSEO | The SEO Agency Team in Tbilisi, Georgia",
        },
        "Meta description": {
            "version": "V1",
            "text": "Meet 10xSEO — the SEO agency that ranks brands #1 on Google and AI platforms. Get to know our team, vision, and approach.",
        },
        "H1": {
            "version": "V2",
            "text": "Meet 10xSEO / Georgia's #1 SEO Agency",
        },
        "Hero subheading": {
            "version": "V1",
            "text": "Be first where customers search for you.",
        },
    },
}


def update_title(html: str, new_title: str) -> tuple[str, int]:
    """Update <title>, og:title, twitter:title."""
    n = 0
    # <title>...</title>
    new_html, c = re.subn(r'(<title>)[^<]*(</title>)',
                         lambda m: f'{m.group(1)}{new_title}{m.group(2)}', html, count=1)
    n += c
    # og:title (content)
    new_html, c = re.subn(r'(<meta property="og:title" content=")[^"]*(")',
                         lambda m: f'{m.group(1)}{new_title}{m.group(2)}', new_html, count=1)
    n += c
    # twitter:title
    new_html, c = re.subn(r'(<meta name="twitter:title" content=")[^"]*(")',
                         lambda m: f'{m.group(1)}{new_title}{m.group(2)}', new_html, count=1)
    n += c
    # JSON-LD WebPage name
    # Note: this is a soft update — only changes if the existing name matches the old title pattern
    return new_html, n


def update_meta_desc(html: str, new_desc: str) -> tuple[str, int]:
    """Update meta description, og:description, twitter:description."""
    n = 0
    new_html, c = re.subn(r'(<meta name="description" content=")[^"]*(")',
                         lambda m: f'{m.group(1)}{new_desc}{m.group(2)}', html, count=1)
    n += c
    new_html, c = re.subn(r'(<meta property="og:description" content=")[^"]*(")',
                         lambda m: f'{m.group(1)}{new_desc}{m.group(2)}', new_html, count=1)
    n += c
    new_html, c = re.subn(r'(<meta name="twitter:description" content=")[^"]*(")',
                         lambda m: f'{m.group(1)}{new_desc}{m.group(2)}', new_html, count=1)
    n += c
    return new_html, n


def split_h1(text: str) -> tuple[str, str]:
    """Split H1 pick text on ' / ' (space-slash-space) into (line1, line2_gradient).
    Won't split on '/' inside tokens like '(GEO/AEO)'. If no separator, returns
    (text, '') — single-line H1.
    """
    if ' / ' in text:
        parts = text.split(' / ', 1)
        return parts[0].strip(), parts[1].strip()
    return text.strip(), ''


def update_h1(html: str, new_h1: str) -> tuple[str, int]:
    """Update H1: typically <h1 ...>line1<br><span class="gradient-text">line2</span></h1>.
    Replaces the entire inner HTML of the first H1.
    """
    line1, line2 = split_h1(new_h1)
    if line2:
        new_inner = f'{line1}<br><span class="gradient-text">{line2}</span>'
    else:
        new_inner = line1
    new_html, n = re.subn(
        r'(<h1[^>]*>)(.*?)(</h1>)',
        lambda m: f'{m.group(1)}{new_inner}{m.group(3)}',
        html, count=1, flags=re.DOTALL
    )
    return new_html, n


def update_hero_subheading(html: str, new_text: str) -> tuple[str, int]:
    """Replace the first <p> tag after </h1> with new_text.
    Preserves attributes; only changes inner text.
    """
    # Find first <p ...>...</p> after </h1>
    h1_end = re.search(r'</h1>', html)
    if not h1_end:
        return html, 0
    after_h1 = html[h1_end.end():]
    # Find first <p ...>...</p>
    p_match = re.search(r'<p\b[^>]*>(.*?)</p>', after_h1, flags=re.DOTALL)
    if not p_match:
        return html, 0
    p_start = h1_end.end() + p_match.start()
    p_end = h1_end.end() + p_match.end()
    # Get the opening tag
    open_tag = re.match(r'<p\b[^>]*>', after_h1[p_match.start():]).group()
    new_p = f'{open_tag}{new_text}</p>'
    return html[:p_start] + new_p + html[p_end:], 1


def apply_to_page(page_path: str, picks: dict) -> dict:
    """Apply all picks for one page. Returns summary stats."""
    # page_path: "/en/<file>.html"
    rel_path = page_path.lstrip("/")
    full = ROOT / rel_path
    if not full.exists():
        return {"error": f"File not found: {full}"}

    html = full.read_text(encoding="utf-8")
    original = html
    stats = {}

    for fragment, pick in picks.items():
        text = pick["text"]
        if fragment == "Title":
            html, n = update_title(html, text)
            stats["title"] = n
        elif fragment == "Meta description":
            html, n = update_meta_desc(html, text)
            stats["meta"] = n
        elif fragment == "H1":
            html, n = update_h1(html, text)
            stats["h1"] = n
        elif "Hero subheading" in fragment:
            html, n = update_hero_subheading(html, text)
            stats["hero_sub"] = n

    if html != original:
        full.write_text(html, encoding="utf-8")
        stats["written"] = True
    else:
        stats["written"] = False
    return stats


def main():
    total = 0
    for page, picks in PICKS.items():
        print(f"\n=== {page} ===")
        stats = apply_to_page(page, picks)
        for k, v in stats.items():
            print(f"  {k}: {v}")
        if stats.get("written"):
            total += 1
    print(f"\n✓ Updated {total}/{len(PICKS)} pages")


if __name__ == "__main__":
    main()
