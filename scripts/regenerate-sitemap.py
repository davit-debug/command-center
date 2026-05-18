#!/usr/bin/env python3
"""Regenerate sitemap.xml from current KEEP pages in command-center/.

Bilingual: includes both KA (root) and EN (/en/) URLs with xhtml:link
hreflang annotations linking each page to its translation counterpart.
"""
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent  # command-center/
OUT = ROOT / "sitemap.xml"
DOMAIN = "https://10xseo.ge"

# Pages to EXCLUDE from sitemap (system pages, campaign landings, noindex)
# Matched against rel path; both root and en/ variants excluded.
# Rule: any page with <meta name="robots" content="noindex"> belongs here —
# listing noindex URLs in sitemap is a Google policy violation.
EXCLUDE = {
    "404.html",
    "en/404.html",
    "lead-form.html",
    "en/lead-form.html",
    # Legal pages — noindex (low SEO value, not for organic discovery)
    "privacy-policy.html",
    "cookies-policy.html",
    "terms-of-service.html",
    "en/privacy-policy.html",
    "en/cookies-policy.html",
    "en/terms-of-service.html",
    # Test/preview/admin pages (P0 audit finding: must not be indexed)
    "og-review.html",
    "og-test.html",
    "cta-picker.html",
    "cta-microcopy.html",
    "cta-segments.html",
    "cta-sitemap.html",
}

# Skipped from translation — these are KA-only (no /en/ counterpart).
# Used to suppress hreflang="en" annotation for these pages.
KA_ONLY = {
    "blog.html",
    "seo-leqsikoni.html",
    "ai-leqsikoni.html",
    "startup-leqsikoni.html",
}
KA_ONLY_PREFIXES = ("blog/",)

# EN-only blog posts (no KA counterpart — written natively in English).
# These appear in the sitemap under /en/blog/ without an alternate hreflang.
EN_ONLY = {
    "en/blog/what-is-aeo.html",
    "en/blog/aeo-optimization-agency-dubai.html",
}

# Priority + changefreq by page type
def page_meta(rel: str) -> tuple[float, str]:
    """Return (priority, changefreq) for a page."""
    if rel == "index.html":
        return (1.0, "weekly")

    # Blog & case-study indexes
    if rel in ("blog.html", "case-studies.html", "portfolio.html"):
        return (0.8, "weekly")

    # Blog posts
    if rel.startswith("blog/"):
        return (0.7, "yearly")

    # Case study details
    if rel.startswith("case-studies/"):
        return (0.7, "yearly")

    # Industries
    if rel.startswith("industries/"):
        return (0.8, "monthly")

    # Tools (sub-pages)
    if rel.startswith("tools/"):
        return (0.6, "monthly")

    # Tools landing
    if rel == "seo-tools.html":
        return (0.8, "monthly")

    # Core service pages
    SERVICES = {
        "services.html", "ai-seo.html", "copywriting.html", "cro.html",
        "google-ads.html", "seo-management.html", "seo-strategy.html",
        "seo-copywriting.html", "seo-audit.html", "seo-consultation.html",
        "seo-course.html",
    }
    if rel in SERVICES:
        return (0.9, "monthly")

    # ROI calculator
    if rel == "roi-calculator.html":
        return (0.8, "monthly")

    # About / contact / vacancies
    if rel in ("about-us.html", "contact-us.html", "vacancies.html"):
        return (0.7, "monthly")

    # Glossaries / informational
    if rel in ("ra-aris-seo.html", "seo-leqsikoni.html", "startup-leqsikoni.html", "ai-leqsikoni.html"):
        return (0.7, "monthly")

    # Default
    return (0.6, "monthly")

def url_for(rel: str) -> str:
    """Convert rel path to public URL.
    - index.html → /
    - en/index.html → /en/
    - everything else → /<rel> (keep .html — matches canonical on each page
      and .htaccess redirects clean URLs back to .html)
    """
    if rel == "index.html":
        return f"{DOMAIN}/"
    if rel == "en/index.html":
        return f"{DOMAIN}/en/"
    return f"{DOMAIN}/{rel}"


def is_ka_only(rel: str) -> bool:
    """Page has no English translation (blog, dictionaries)."""
    if rel in KA_ONLY:
        return True
    return any(rel.startswith(p) for p in KA_ONLY_PREFIXES)


def is_en_path(rel: str) -> bool:
    """Page lives under /en/ subtree."""
    return rel.startswith("en/")


def ka_counterpart(rel: str) -> str:
    """Given an EN path en/foo.html, return ka counterpart 'foo.html'."""
    return rel[len("en/"):] if rel.startswith("en/") else rel


def en_counterpart(rel: str) -> str | None:
    """Given a KA path foo.html, return en/foo.html if its EN translation
    exists in the tracked file set; None if no EN counterpart."""
    return f"en/{rel}"


def has_en_translation(rel: str, all_files: set) -> bool:
    """KA page has an EN counterpart if /en/<rel> exists in tracked files."""
    if is_ka_only(rel) or is_en_path(rel):
        return False
    return f"en/{rel}" in all_files

def get_lastmod(path: Path) -> str:
    """Get last commit date for file (or file mtime as fallback)."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", str(path.relative_to(ROOT))],
            cwd=ROOT, capture_output=True, text=True
        )
        date = result.stdout.strip()
        if date:
            return date
    except Exception:
        pass
    # Fallback to mtime
    return datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d")

def sort_key(rel: str) -> tuple:
    """Order: KA pages first by category, then EN pages mirroring KA order.
    Homepage → core services → industries → blog/case indexes → details → tools → other.
    """
    # KA pages get priority bucket 0-9; EN pages get 10-19 (mirrors KA order)
    locale_offset = 10 if rel.startswith("en/") else 0
    base = rel[len("en/"):] if rel.startswith("en/") else rel

    if base == "index.html": return (0 + locale_offset, rel)
    if base.startswith("blog/"): return (8 + locale_offset, rel)
    if base.startswith("case-studies/"): return (7 + locale_offset, rel)
    if base.startswith("industries/"): return (4 + locale_offset, rel)
    if base.startswith("tools/"): return (9 + locale_offset, rel)
    if base in ("blog.html", "case-studies.html", "portfolio.html"): return (5 + locale_offset, rel)
    SERVICES = {
        "services.html", "ai-seo.html", "copywriting.html", "cro.html",
        "google-ads.html", "seo-management.html", "seo-strategy.html",
        "seo-copywriting.html", "seo-audit.html", "seo-consultation.html",
        "seo-course.html", "seo-tools.html",
    }
    if base in SERVICES: return (1 + locale_offset, rel)
    if base == "roi-calculator.html": return (2 + locale_offset, rel)
    if base in ("about-us.html", "contact-us.html", "vacancies.html"): return (3 + locale_offset, rel)
    return (6 + locale_offset, rel)

def main():
    # Get all tracked HTML files
    result = subprocess.run(
        ["git", "ls-files", "*.html"],
        cwd=ROOT, capture_output=True, text=True
    )
    all_tracked = set(f for f in result.stdout.strip().split("\n") if f)
    files = [f for f in all_tracked if f not in EXCLUDE]
    files.sort(key=sort_key)

    print(f"Building bilingual sitemap from {len(files)} pages...")

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<?xml-stylesheet type="text/xsl" href="/sitemap.xsl"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
             '        xmlns:xhtml="http://www.w3.org/1999/xhtml">']

    for rel in files:
        path = ROOT / rel
        if not path.exists():
            print(f"  ⚠ skipped (file missing): {rel}")
            continue
        url = url_for(rel)
        lastmod = get_lastmod(path)
        priority, changefreq = page_meta(rel)

        # Determine hreflang alternates
        ka_url = None
        en_url = None
        if is_en_path(rel):
            ka_rel = ka_counterpart(rel)
            if ka_rel in all_tracked:
                ka_url = url_for(ka_rel)
            en_url = url
        else:
            ka_url = url
            if has_en_translation(rel, all_tracked):
                en_url = url_for(f"en/{rel}")

        lines.append("  <url>")
        lines.append(f"    <loc>{url}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append(f"    <changefreq>{changefreq}</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")

        if ka_url and en_url:
            lines.append(f'    <xhtml:link rel="alternate" hreflang="ka" href="{ka_url}"/>')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{en_url}"/>')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{ka_url}"/>')

        lines.append("  </url>")
        flag = "🌐" if (ka_url and en_url) else ""
        print(f"  ✓ [{priority}] {url} {flag}")

    lines.append('</urlset>')
    lines.append('')

    OUT.write_text("\n".join(lines))

    # Summary
    print(f"\n✅ Wrote {OUT}")
    print(f"   Total URLs: {len(files)}")
    print(f"   Excluded: {sorted(EXCLUDE)}")
    bilingual = sum(1 for f in files if not is_en_path(f) and has_en_translation(f, all_tracked))
    print(f"   With EN translation: {bilingual} pages")

if __name__ == "__main__":
    main()
