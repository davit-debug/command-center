#!/usr/bin/env python3
"""Render SVG → PNG via Playwright headless browser.

Used to convert the branded blog card SVGs into raster PNGs for use as
og:image (social previews can't display SVG).
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
BLOG_DIR = ROOT / "images" / "blog"

SVG_FILES = [
    "what-is-aeo-card.svg",
    "aeo-optimization-agency-dubai-card.svg",
]

WIDTH = 1200
HEIGHT = 630


def render(svg_path: Path, png_path: Path):
    svg_content = svg_path.read_text()
    # Wrap SVG in minimal HTML so playwright can screenshot at exact dimensions
    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
body{{margin:0;padding:0;overflow:hidden;width:{WIDTH}px;height:{HEIGHT}px}}
svg{{display:block;width:{WIDTH}px;height:{HEIGHT}px}}
</style></head><body>{svg_content}</body></html>"""

    tmp_html = svg_path.parent / f"_{svg_path.stem}.html"
    tmp_html.write_text(html, encoding="utf-8")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT})
            page.goto(f"file://{tmp_html}")
            page.wait_for_load_state("networkidle")
            page.screenshot(path=str(png_path), omit_background=False, clip={"x": 0, "y": 0, "width": WIDTH, "height": HEIGHT})
            browser.close()
        print(f"✓ Rendered {png_path.relative_to(ROOT)} ({png_path.stat().st_size} bytes)")
    finally:
        if tmp_html.exists():
            tmp_html.unlink()


def main():
    for svg_name in SVG_FILES:
        svg_path = BLOG_DIR / svg_name
        if not svg_path.exists():
            print(f"✗ Missing: {svg_path}")
            continue
        png_path = svg_path.with_suffix(".png")
        render(svg_path, png_path)


if __name__ == "__main__":
    main()
