#!/usr/bin/env python3
"""Apply user's translation picks to /en/*.html pages.

Takes a PICKS dict of {page: {fragment: {version, text} | {custom: text}}} and
updates: title (in <title>, og:title, twitter:title), meta description
(in <meta>, og:description, twitter:description), H1 (two-line gradient
pattern), and hero subheading (first <p> after H1).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_DIR = ROOT / "en"

# Strip trailing markdown parser artifacts like:  ` (literal KA translation)
ARTIFACT_RE = re.compile(r"`\s*\([^)]+\)\s*$")


def clean_text(s: str) -> str:
    """Remove trailing parser artifacts (e.g. `` ` (current)``) from pick text."""
    return ARTIFACT_RE.sub("", s).rstrip("`").rstrip()


PICKS = {
    "/en/index.html": {
        "Hero subheading": {"version": "V1", "text": "Georgia's #1 SEO Agency — We put brands where customers search for answers."},
    },
    "/en/services.html": {
        "Title": {"version": "V3", "text": "SEO Services in Georgia | Management, AI SEO, CRO — 10xSEO"},
        "Meta description": {"version": "V2", "text": "Hire Georgia's #1 SEO agency. We offer SEO management, AI SEO, CRO, Google Ads, copywriting & free SEO tools for Tbilisi & international brands."},
        "H1": {"version": "V1", "text": "SEO Services — Full Ecosystem / for Your Business Growth"},
        "Hero subheading": {"version": "V2", "text": "Twelve specialized SEO services under one roof. Pick what you need — SEO management, AI SEO, CRO, Google Ads, copywriting, or our free tools."},
    },
    "/en/ai-seo.html": {
        "Title": {"version": "V1", "text": "AI SEO (GEO/AEO) | Rank in ChatGPT, Gemini & Perplexity — 10xSEO"},
        "Meta description": {"version": "V1", "text": "Get cited in ChatGPT, Gemini, Perplexity & Claude. 10xSEO's AI SEO service: GEO + AEO optimization for maximum brand visibility in AI search."},
        "H1": {"version": "V1", "text": "AI SEO (GEO/AEO) — / Visibility in ChatGPT, Gemini & Perplexity"},
        "Hero subheading": {"version": "V3", "text": "Your customers ask AI now. Make sure ChatGPT, Gemini, Perplexity & Claude answer with your brand."},
    },
    "/en/contact-us.html": {
        "Title": {"version": "V5", "text": "Contact 10xSEO | Book a 15-Min SEO Consultation"},
        "Meta description": {"version": "V5", "text": "Contact the SEO agency Tbilisi trusts. 10xSEO offers free 15-min consultations for businesses ready to rank #1 on Google + AI search."},
        "H1": {"version": "V1", "text": "Get in Touch"},
        "Hero subheading": {"version": "V1", "text": "Whether you have a quick question or need a full SEO strategy — we're here. Reach us by phone, email, or book a free consultation online."},
    },
    "/en/about-us.html": {
        "Title": {"version": "V2", "text": "Meet 10xSEO | The SEO Agency Team in Tbilisi, Georgia"},
        "Meta description": {"version": "V1", "text": "Meet 10xSEO — the SEO agency that ranks brands #1 on Google and AI platforms. Get to know our team, vision, and approach."},
        "H1": {"version": "V2", "text": "Meet 10xSEO / Georgia's #1 SEO Agency"},
        "Hero subheading": {"version": "V1", "text": "Be first where customers search for you."},
    },
    # === SERVICE PAGES (new) ===
    "/en/seo-management.html": {
        "Title": {"version": "V5", "text": "Hire 10xSEO — Monthly SEO Management for Ambitious Brands"},
        "Meta description": {"version": "V4", "text": "Stop juggling SEO yourself. 10xSEO's monthly management package handles everything: technical, content, links, AEO/GEO. Live dashboard + 10-min SLA."},
        "H1": {"version": "V5", "text": "Monthly SEO Management / Built for Compound Growth"},
        "Hero subheading": {"version": "V3", "text": "Monthly retainer for businesses that want results, not status reports. Live dashboard, weekly reviews, and a guaranteed 10-minute response window during business hours."},
    },
    "/en/seo-consultation.html": {
        "Title": {"version": "V1", "text": "SEO Consultation 1:1 — Expert Strategy Sessions | 10xSEO"},
        "Meta description": {"version": "V1", "text": "Get 1:1 SEO consultation from a 14-year veteran. Solve technical SEO challenges, get clear answers, and a custom action plan. Book a session with 10xSEO."},
        "H1": {"version": "V1", "text": "One-on-One SEO Session with an Expert"},
        "Hero subheading": {"version": "V2", "text": "Sometimes you don't need a full SEO retainer — you need one hour with the right expert. Strategy review, audit feedback, or a single focused problem."},
    },
    "/en/seo-strategy.html": {
        "Title": {"version": "V3", "text": "Custom SEO Strategy + Roadmap | 10xSEO Georgia"},
        "Meta description": {"version": "V1", "text": "Get a complete SEO strategy for your project: in-depth analysis, competitor research, market study, and step-by-step optimization roadmap from 10xSEO."},
        "H1": {"version": "V2", "text": "Custom SEO Strategy / Built Around Your Goals"},
        "Hero subheading": {"version": "V4", "text": "12 months of SEO mapped out with milestones, owners, and KPIs. Delivered as a working document your team can execute against, not a static PDF."},
    },
    "/en/seo-copywriting.html": {
        "Title": {"version": "V5", "text": "Premium SEO Copywriting for Ambitious Brands | 10xSEO"},
        "Meta description": {"version": "V1", "text": "SEO copywriting for business: homepages, blogs, articles, press releases. Content that ranks on Google's first page and converts visitors into customers."},
        "H1": {"version": "V1", "text": "SEO Copywriting — Content That Gets You / Found on Google"},
        "Hero subheading": {"version": "V1", "text": "Content that works for both the algorithms and your sales growth."},
    },
    "/en/copywriting.html": {
        "Title": {"version": "V1", "text": "UI/UX Copywriting — Words That Drive User Behavior | 10xSEO"},
        "Meta description": {"version": "V3", "text": "Bad UI copy costs you customers. 10xSEO's UI/UX copywriters audit and rewrite your interface so visitors actually finish what they came to do."},
        "H1": {"version": "V1", "text": "Copy That Drives User Action"},
        "Hero subheading": {"version": "V1", "text": "Your website speaks to clients through its text. We ensure this language is simple, consistent, polished, and precisely answers the questions your potential customers have."},
    },
    "/en/cro.html": {
        "Title": {"version": "V5", "text": "Increase Conversions Without Increasing Ad Spend | 10xSEO CRO"},
        "Meta description": {"version": "V1", "text": "CRO services from 10xSEO: improve conversion rates with data analysis & A/B testing. Turn visits into real sales without increasing your ad spend."},
        "H1": {"version": "V1", "text": "Conversion Rate Optimization (CRO) — Increase Sales with Your Existing Traffic"},
        "Hero subheading": {"version": "V3", "text": "CRO rooted in heatmaps, user interviews, and revenue data — not opinions. Most clients see 15–60% conversion lift within 90 days."},
    },
    "/en/google-ads.html": {
        "Title": {"version": "V1", "text": "Google Ads Management — Targeted Campaigns That Convert | 10xSEO"},
        "Meta description": {"version": "V2", "text": "Stop wasting Google Ads budget. 10xSEO manages search, shopping, display, and YouTube campaigns built around ROI — not impressions or vanity clicks."},
        "H1": {"version": "V1", "text": "Google Ads Management — Paid Advertising That Pays Off"},
        "Hero subheading": {"version": "V1", "text": "Profitable Google Ads campaigns for Tbilisi and international brands. Search, Shopping, PMax, Display, YouTube — every campaign engineered around revenue, not vanity metrics."},
    },
    "/en/seo-audit.html": {
        "Title": {"version": "V1", "text": "Free SEO Audit — Loom Video Analysis in 72 Hours | 10xSEO"},
        "Meta description": {"version": "V1", "text": "Free SEO audit: 10-minute Loom video where our expert reviews your site's issues, analyzes competitors, and shows real growth potential. Delivered in 72 hours."},
        "H1": {"version": "V1", "text": "Free SEO Audit: Get a Personal Video Analysis in 72 Hours"},
        "Hero subheading": {"version": "V1", "text": "Our expert will record a video review for you, providing a step-by-step analysis of your site's issues, competitor strategies, and real growth opportunities for your brand."},
    },
    "/en/seo-course.html": {
        "Title": {"version": "V3", "text": "Learn SEO from Georgia's #1 Practitioner | 10xSEO Course"},
        "Meta description": {"version": "V1", "text": "SEO course by Davit Tsilosani — 12 hands-on sessions, real-world examples, and an internship opportunity at 10xSEO. Learn from Georgia's leading practitioner."},
        "H1": {"version": "V1", "text": "SEO Course: 12 Intensive Workshops"},
        "Hero subheading": {"version": "V1", "text": "Here, you will learn to use the tools that market leaders use to dominate the top positions."},
    },
    # === INDUSTRY PAGES ===
    "/en/industries/construction.html": {
        "Title": {"version": "V1", "text": "Construction & Real Estate SEO — Scale Your Sales | 10xSEO"},
        "Meta description": {"version": "V4", "text": "Stop wasting marketing on developer-buyer mismatch. 10xSEO's real estate SEO targets the exact searches your future buyers make — and turns them into tours."},
        "H1": {"version": "V2", "text": "Real Estate SEO / That Sells Units, Not Clicks"},
        "Hero subheading": {"version": "V1", "text": "From SEO to Google Ads: Five services to grow your project's sales. One team, unified accountability, and maximum visibility."},
    },
    "/en/industries/healthcare.html": {
        "Title": {"custom": "Medical SEO + AEO | 10xSEO"},
        "Meta description": {"version": "V1", "text": "SEO & AEO strategies for clinics. Strengthen your Google rankings, attract patients, and rank in AI search answers. Healthcare SEO experts at 10xSEO."},
        "H1": {"version": "V3", "text": "Rank #1 Where Patients Search / Healthcare SEO from 10xSEO"},
        "Hero subheading": {"version": "V3", "text": "Specialized SEO for clinics and medical brands in Tbilisi and beyond. E-E-A-T signals, expert-reviewed content, and patient-intent keyword targeting."},
    },
    "/en/industries/financial-services.html": {
        "Title": {"version": "V4", "text": "YMYL-Compliant Financial Services SEO | 10xSEO Georgia"},
        "Meta description": {"version": "V2", "text": "Financial services SEO for banks, insurance, fintech, and accounting firms. YMYL-compliant content, AEO visibility, and conversion-focused product pages."},
        "H1": {"version": "V1", "text": "Financial SEO Services"},
        "Hero subheading": {"version": "V1", "text": "Delivered with industry expertise, regulatory compliance, and measurable results."},
    },
    "/en/industries/ecommerce.html": {
        "Title": {"version": "V1", "text": "E-commerce SEO Services — Grow Online Sales | 10xSEO"},
        "Meta description": {"version": "V1", "text": "E-commerce SEO: take your products to international markets via search engines. Full technical support for online stores and organic growth strategy."},
        "H1": {"version": "V2", "text": "E-commerce SEO / Built for Repeatable Revenue"},
        "Hero subheading": {"version": "V1", "text": "Shopify, WooCommerce, Magento - Experience in global markets: Georgia, USA, UK, United Arab Emirates"},
    },
}


def update_title(html: str, new_title: str) -> tuple[str, int]:
    n = 0
    new_html, c = re.subn(r'(<title>)[^<]*(</title>)',
                         lambda m: f'{m.group(1)}{new_title}{m.group(2)}', html, count=1)
    n += c
    new_html, c = re.subn(r'(<meta property="og:title" content=")[^"]*(")',
                         lambda m: f'{m.group(1)}{new_title}{m.group(2)}', new_html, count=1)
    n += c
    new_html, c = re.subn(r'(<meta name="twitter:title" content=")[^"]*(")',
                         lambda m: f'{m.group(1)}{new_title}{m.group(2)}', new_html, count=1)
    n += c
    return new_html, n


def update_meta_desc(html: str, new_desc: str) -> tuple[str, int]:
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
    """Split on ' / ' (space-slash-space). '(GEO/AEO)' stays intact."""
    if ' / ' in text:
        parts = text.split(' / ', 1)
        return parts[0].strip(), parts[1].strip()
    return text.strip(), ''


def update_h1(html: str, new_h1: str) -> tuple[str, int]:
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
    h1_end = re.search(r'</h1>', html)
    if not h1_end:
        return html, 0
    after_h1 = html[h1_end.end():]
    p_match = re.search(r'<p\b[^>]*>(.*?)</p>', after_h1, flags=re.DOTALL)
    if not p_match:
        return html, 0
    p_start = h1_end.end() + p_match.start()
    p_end = h1_end.end() + p_match.end()
    open_tag = re.match(r'<p\b[^>]*>', after_h1[p_match.start():]).group()
    new_p = f'{open_tag}{new_text}</p>'
    return html[:p_start] + new_p + html[p_end:], 1


def get_pick_text(pick: dict) -> str:
    """Extract the text from a pick dict, handling both 'text' and 'custom' fields,
    and stripping markdown parser artifacts."""
    raw = pick.get("custom") or pick.get("text") or ""
    return clean_text(raw)


def apply_to_page(page_path: str, picks: dict) -> dict:
    rel_path = page_path.lstrip("/")
    full = ROOT / rel_path
    if not full.exists():
        return {"error": f"File not found: {full}"}

    html = full.read_text(encoding="utf-8")
    original = html
    stats = {}

    for fragment, pick in picks.items():
        text = get_pick_text(pick)
        if not text:
            continue
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
