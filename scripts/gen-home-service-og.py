#!/usr/bin/env python3
"""
Generate OG variants for:
  - Homepage (10 variants: V1, A, B, C, D, E, F, I, L, M)
  - 10 service pages (5 variants each: V1, B, D, I, M)

Output paths:
  og-previews/per-home/v{X}/home.jpg
  og-previews/per-service/v{X}/{service_og}.jpg

Reuses templates from gen-case-og-images.py + gen-case-og-variants-DH.py + gen-case-og-variants-IM.py
"""
import importlib.util
import subprocess
from pathlib import Path
from PIL import Image

ROOT = Path("/Users/imac/SEO/command-center")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Load all template strings from prior scripts
def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# Templates from earlier scripts
prev_DH = load_module("dh", ROOT / "scripts" / "gen-case-og-variants-DH.py")
prev_IM = load_module("im", ROOT / "scripts" / "gen-case-og-variants-IM.py")

# Read V1 (case OG) template from gen-case-og-images.py
v1_mod = load_module("v1", ROOT / "scripts" / "gen-case-og-images.py")
TPL_V1 = v1_mod.TEMPLATE  # V1 Big Number Hero

# Read A/B/C from gen-case-og-variants.py
abc_mod = load_module("abc", ROOT / "scripts" / "gen-case-og-variants.py")
TPL_A = abc_mod.TPL_A
TPL_B = abc_mod.TPL_B
TPL_C = abc_mod.TPL_C

TPL_D = prev_DH.TPL_D
TPL_E = prev_DH.TPL_E
TPL_F = prev_DH.TPL_F
TPL_G = prev_DH.TPL_G
TPL_H = prev_DH.TPL_H
TPL_I = prev_IM.TPL_I
TPL_J = prev_IM.TPL_J
TPL_K = prev_IM.TPL_K
TPL_L = prev_IM.TPL_L
TPL_M = prev_IM.TPL_M

ALL_TPLS = {
    "V1": TPL_V1, "vA": TPL_A, "vB": TPL_B, "vC": TPL_C, "vD": TPL_D,
    "vE": TPL_E, "vF": TPL_F, "vG": TPL_G, "vH": TPL_H,
    "vI": TPL_I, "vJ": TPL_J, "vK": TPL_K, "vL": TPL_L, "vM": TPL_M,
}

# ============== HOMEPAGE DATA ==============
HOME = {
    "slug": "index", "og": "home",
    "industry": "ყველა ინდუსტრია",
    "metric": "+247%", "metric_size": 280,
    "tf": "8 ქეისი", "year": "2026",
    "kicker": "საშუალო ზრდა · 8 ქეის სტადი",
    "title": "საქართველოს #1 SEO სააგენტო.",
    "bottom": "8× ROI · 30 დღე პირველ შედეგამდე · GSC + GA4 ვერიფიცირებული",
    "chapter": "★",
}

HOME_VARIANTS = ["V1", "vA", "vB", "vC", "vD", "vE", "vF", "vI", "vL", "vM"]

# ============== SERVICES DATA ==============
SERVICES = [
    {"slug":"seo-management","og":"service-seo-mgmt","industry":"SEO Management","metric":"+247%","metric_size":280,"tf":"6+ თვე","year":"2026","kicker":"ყოველთვიური მენეჯმენტი","title":"სრული SEO გუნდი.","bottom":"კონტენტი + ბექლინქი + ტექნ. SEO + AI/GEO + ანგარიში","chapter":"★"},
    {"slug":"seo-consultation","og":"service-consultation","industry":"კონსულტაცია","metric":"60წთ","metric_size":260,"tf":"1 სესია","year":"2026","kicker":"სტრატეგიული ერთ-ერთზე","title":"60 წუთი — სტრატეგია.","bottom":"Loom ჩანაწერი + წერილობითი action plan","chapter":"★"},
    {"slug":"seo-strategy","og":"service-seo-strategy","industry":"SEO სტრატეგია","metric":"12 თვე","metric_size":260,"tf":"4-6 კვირა","year":"2026","kicker":"გრძელვადიანი გეგმა","title":"12-თვიანი SEO Roadmap.","bottom":"კონკურენტული ანალიზი + keyword strategy + content plan","chapter":"★"},
    {"slug":"seo-copywriting","og":"service-seo-copy","industry":"SEO Copywriting","metric":"+180%","metric_size":280,"tf":"4 კვირა","year":"2026","kicker":"კონტენტი, რომელიც ქმედებამდე მიდის","title":"ტექსტი, რომელიც ყიდის.","bottom":"Long-form SEO content · E-E-A-T · structured data","chapter":"★"},
    {"slug":"copywriting","og":"service-copywriting","industry":"UI/UX Copy","metric":"+35%","metric_size":280,"tf":"2-4 კვირა","year":"2026","kicker":"მიკროკოპი, რომელიც აკონვერტებს","title":"UI/UX-ის ხმა.","bottom":"Onboarding · forms · empty states · error messages","chapter":"★"},
    {"slug":"cro","og":"service-cro","industry":"CRO","metric":"+45%","metric_size":280,"tf":"3 თვე","year":"2026","kicker":"კონვერსიის ოპტიმიზაცია","title":"მეტი მომხმარებელი — იმავე ტრაფიკიდან.","bottom":"A/B test · heatmap · funnel analysis · UX research","chapter":"★"},
    {"slug":"google-ads","og":"service-google-ads","industry":"Google Ads","metric":"-40%","metric_size":280,"tf":"30 დღე","year":"2026","kicker":"CPC ოპტიმიზაცია","title":"Google Ads, რომელიც ფულს ზოგავს.","bottom":"Search · Display · Performance Max · Shopping","chapter":"★"},
    {"slug":"ai-seo","og":"service-ai-seo","industry":"AI SEO / GEO","metric":"AI ↑","metric_size":260,"tf":"3-6 თვე","year":"2026","kicker":"იყავი იქ, სადაც პასუხებს ეძებენ","title":"ChatGPT-ში, Perplexity-ში, AI Overviews-ში.","bottom":"GEO + AEO + LLM visibility + AI Crawler ოპტიმიზაცია","chapter":"★"},
    {"slug":"seo-course","og":"service-seo-course","industry":"SEO Course","metric":"12 კვ.","metric_size":260,"tf":"3 თვე","year":"2026","kicker":"12 პრაქტიკული გაკვეთილი","title":"ისწავლე SEO ნულიდან.","bottom":"Theory + workshops + real-project hands-on + სერთიფიკატი","chapter":"★"},
    {"slug":"seo-audit","og":"service-seo-audit","industry":"SEO აუდიტი","metric":"უფასო","metric_size":280,"tf":"24 სთ","year":"2026","kicker":"სრული Loom ვიდეო-ანალიზი","title":"შენი საიტი — სრულად შემოწმებული.","bottom":"100+ ფაქტორი · technical · content · backlink · UX","chapter":"★"},
]

SERVICE_VARIANTS = ["V1", "vB", "vD", "vI", "vM"]

# Common derived helpers
ISSUE_MAP_COUNT = {}
def derive_data(c, idx=0):
    d = dict(c)
    # V1 template uses `badge` instead of `industry`
    d["badge"] = f"{c.get('industry','')} · {c.get('tf','')}".strip(" ·") if c.get("industry") else c.get("badge", "")
    d["title_short"] = c.get("title", "")[:24]
    d["title_pop"] = c.get("title", "")[:24]
    d["kicker_short_pop"] = c.get("kicker", "")[:22]
    d["kicker_short"] = c.get("kicker", "")[:30]
    d["issue"] = f"{idx+1:03}"
    # Iso/pop scaled metric sizes
    msz = c.get("metric_size", 280)
    d["metric_size_iso"] = int(msz * 0.55)
    d["metric_size_pop"] = int(msz * 0.62)
    # Growth-short
    m = c.get("metric", "")
    if "%" in m: d["growth_short"] = m.replace("+","").replace("%","%")
    elif "×" in m or "x" in m: d["growth_short"] = m + "x"
    elif "TOP" in m: d["growth_short"] = "TOP"
    elif "+" in m: d["growth_short"] = m.replace(",","")[:6]
    else: d["growth_short"] = m[:6]
    return d

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

def gen_one(tpl_key, page_data, kind, page_idx=0):
    """Generate one variant for one page."""
    tpl = ALL_TPLS[tpl_key]
    out_html_dir = ROOT / f"og-per-{kind}" / tpl_key
    out_png_dir = ROOT / "og-previews" / f"per-{kind}" / tpl_key
    out_html_dir.mkdir(parents=True, exist_ok=True)
    out_png_dir.mkdir(parents=True, exist_ok=True)

    data = derive_data(page_data, page_idx)
    try:
        html = tpl.format(**data)
    except KeyError as e:
        print(f"  ✗ {tpl_key}/{page_data['slug']}: missing key {e}")
        return None
    html_path = out_html_dir / f"{page_data['slug']}.html"
    html_path.write_text(html, encoding="utf-8")
    raw = out_html_dir / f"_raw_{page_data['slug']}.png"
    screenshot(html_path, raw)
    final = out_png_dir / f"{page_data['og']}.jpg"
    crop_to_og(raw, final)
    raw.unlink()
    return final

def main():
    # Homepage — 10 variants
    print("=" * 70)
    print(f"HOMEPAGE — {len(HOME_VARIANTS)} variants")
    print("=" * 70)
    for tpl in HOME_VARIANTS:
        result = gen_one(tpl, HOME, "home", 0)
        if result:
            print(f"  ✓ {tpl} · home → {result.relative_to(ROOT)}")

    # Services — 5 variants each × 10 services
    print()
    print("=" * 70)
    print(f"SERVICES — {len(SERVICES)} services × {len(SERVICE_VARIANTS)} variants = {len(SERVICES)*len(SERVICE_VARIANTS)} total")
    print("=" * 70)
    for i, svc in enumerate(SERVICES):
        for tpl in SERVICE_VARIANTS:
            result = gen_one(tpl, svc, "service", i)
            if result:
                print(f"  ✓ {tpl} · {svc['slug']:25} → {result.name}")

if __name__ == "__main__":
    main()
