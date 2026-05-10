#!/usr/bin/env python3
"""Regenerate sitemap.xml from current KEEP pages in command-center/."""
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent  # command-center/
OUT = ROOT / "sitemap.xml"
DOMAIN = "https://10xseo.ge"

# Pages to EXCLUDE from sitemap (system pages, campaign landings)
EXCLUDE = {
    "404.html",          # System error page
    "lead-form.html",    # Campaign landing — intentionally not in sitemap
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
    """Convert rel path to public URL. Special case: index.html → /, seo-audit.html → seo-audit/."""
    if rel == "index.html":
        return f"{DOMAIN}/"
    if rel == "seo-audit.html":
        return f"{DOMAIN}/seo-audit/"
    return f"{DOMAIN}/{rel}"

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
    """Order: homepage → core services → industries → blog/case indexes → details → tools → other."""
    if rel == "index.html": return (0, rel)
    if rel.startswith("blog/"): return (8, rel)
    if rel.startswith("case-studies/"): return (7, rel)
    if rel.startswith("industries/"): return (4, rel)
    if rel.startswith("tools/"): return (9, rel)
    if rel in ("blog.html", "case-studies.html", "portfolio.html"): return (5, rel)
    SERVICES = {
        "services.html", "ai-seo.html", "copywriting.html", "cro.html",
        "google-ads.html", "seo-management.html", "seo-strategy.html",
        "seo-copywriting.html", "seo-audit.html", "seo-consultation.html",
        "seo-course.html", "seo-tools.html",
    }
    if rel in SERVICES: return (1, rel)
    if rel == "roi-calculator.html": return (2, rel)
    if rel in ("about-us.html", "contact-us.html", "vacancies.html"): return (3, rel)
    return (6, rel)

def main():
    # Get all tracked HTML files
    result = subprocess.run(
        ["git", "ls-files", "*.html"],
        cwd=ROOT, capture_output=True, text=True
    )
    files = [f for f in result.stdout.strip().split("\n") if f and f not in EXCLUDE]
    files.sort(key=sort_key)

    print(f"Building sitemap from {len(files)} pages...")

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']

    for rel in files:
        path = ROOT / rel
        if not path.exists():
            print(f"  ⚠ skipped (file missing): {rel}")
            continue
        url = url_for(rel)
        lastmod = get_lastmod(path)
        priority, changefreq = page_meta(rel)
        lines.append("  <url>")
        lines.append(f"    <loc>{url}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append(f"    <changefreq>{changefreq}</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")
        print(f"  ✓ [{priority}] {url}")

    lines.append('</urlset>')
    lines.append('')

    OUT.write_text("\n".join(lines))

    # Summary
    print(f"\n✅ Wrote {OUT}")
    print(f"   Total URLs: {len(files)}")
    print(f"   Excluded: {sorted(EXCLUDE)}")

if __name__ == "__main__":
    main()
