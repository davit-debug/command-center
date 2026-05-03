#!/usr/bin/env python3
"""
Apply V29 Gold Glassmorphism FAQ template + see-more button to all pages.

Detects existing FAQ structure per-page (5 known variants), extracts Q/A
data, and rewrites the FAQ <section> with the homepage style.

Variants handled:
  1. v29-items (existing V29 - just wrap with see-more)
  2. fq1-list  (JS data array driver)
  3. faq-item  (inline HTML buttons)
  4. fq1-card  (inline HTML, offer.html)
  5. pfaq-item (inline HTML, offer-premium*.html)
  6. <details> (offer-deal-room.html)
"""
import re
import sys
import os
from pathlib import Path

ROOT = Path(__file__).parent.parent

# ============================================================
# V29 TEMPLATE — single source of truth
# ============================================================

V29_CSS = """    /* FAQ v29 Gold Glassmorphism (homepage parity) */
    .v29-tab { padding: 8px 18px; border-radius: 8px; font-size: 13px; font-weight: 700; cursor: pointer; transition: all 0.3s; border: none; text-transform: uppercase; letter-spacing: 0.5px; }
    .v29-tab:hover { opacity: 0.85; }
    .v29-tab.v29-active { box-shadow: 0 0 16px rgba(0,0,0,0.3); }
    .v29-tab[data-cat="all"] { background: rgba(20,184,166,0.15); color: #2DD4BF; }
    .v29-tab[data-cat="general"] { background: rgba(236,72,153,0.15); color: #F472B6; }
    .v29-tab[data-cat="price"] { background: rgba(245,158,11,0.15); color: #FBBF24; }
    .v29-tab[data-cat="results"] { background: rgba(59,130,246,0.15); color: #60A5FA; }
    .v29-card { border-radius: 16px; overflow: hidden; background: rgba(255,255,255,0.035); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.08); transition: all 0.35s; position: relative; }
    .v29-card::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 3px; border-radius: 14px 0 0 14px; opacity: 0; transition: opacity 0.3s; background: #D4A017; }
    .v29-card[data-cat="ზოგადი"]::before { background: #EC4899; }
    .v29-card[data-cat="შედეგები"]::before { background: #3B82F6; }
    .v29-card[data-cat="ფასი"]::before { background: #F59E0B; }
    .v29-card:hover { border-color: rgba(212,160,23,0.25); }
    .v29-card[data-cat="ზოგადი"]:hover { border-color: rgba(236,72,153,0.25); }
    .v29-card[data-cat="შედეგები"]:hover { border-color: rgba(59,130,246,0.25); }
    .v29-card[data-cat="ფასი"]:hover { border-color: rgba(245,158,11,0.25); }
    .v29-card:hover::before { opacity: 0.5; }
    .v29-card.v29-open { border-color: rgba(212,160,23,0.35); background: rgba(212,160,23,0.04); box-shadow: 0 0 30px rgba(212,160,23,0.06); }
    .v29-card[data-cat="ზოგადი"].v29-open { border-color: rgba(236,72,153,0.35); background: rgba(236,72,153,0.04); box-shadow: 0 0 30px rgba(236,72,153,0.06); }
    .v29-card[data-cat="შედეგები"].v29-open { border-color: rgba(59,130,246,0.35); background: rgba(59,130,246,0.04); box-shadow: 0 0 30px rgba(59,130,246,0.06); }
    .v29-card[data-cat="ფასი"].v29-open { border-color: rgba(245,158,11,0.35); background: rgba(245,158,11,0.04); box-shadow: 0 0 30px rgba(245,158,11,0.06); }
    .v29-card.v29-open::before { opacity: 1; }
    .v29-card.v29-hidden { display: none; }
    .v29-cq { display: flex; align-items: center; padding: 18px 22px; cursor: pointer; gap: 16px; }
    .v29-cq .v29-badge { width: 38px; height: 38px; border-radius: 10px; background: rgba(212,160,23,0.1); display: flex; align-items: center; justify-content: center; flex-shrink: 0; transition: all 0.3s; }
    .v29-open .v29-badge { background: rgba(212,160,23,0.2); box-shadow: 0 0 12px rgba(212,160,23,0.15); }
    .v29-cq .v29-badge svg { width: 16px; height: 16px; stroke: #D4A017; transition: transform 0.3s; }
    .v29-open .v29-badge svg { transform: rotate(180deg); stroke: #EAB308; }
    .v29-cq .v29-txt { flex: 1; font-weight: 600; color: #F1F5F9; font-size: 17px; line-height: 1.4; }
    .v29-cat { font-size: 10px; font-weight: 700; padding: 3px 8px; border-radius: 6px; text-transform: uppercase; letter-spacing: 0.5px; flex-shrink: 0; }
    .v29-cat[data-key="general"] { color: #F472B6; background: rgba(236,72,153,0.15); }
    .v29-cat[data-key="price"] { color: #FBBF24; background: rgba(245,158,11,0.15); }
    .v29-cat[data-key="results"] { color: #60A5FA; background: rgba(59,130,246,0.15); }
    .v29-ca { max-height: 0; overflow: hidden; transition: max-height 0.45s cubic-bezier(0.4,0,0.2,1), padding 0.3s; padding: 0 22px 0 76px; }
    .v29-open .v29-ca { max-height: 500px; padding: 0 22px 18px 76px; }
    .v29-ca p { color: #CBD5E1; font-size: 15px; line-height: 1.8; }
    .v29-card.v29-extra-hidden { display: none; }
    .v29-more-wrap { text-align: center; margin-top: 24px; }
    .v29-more-wrap.v29-hidden { display: none; }
    .v29-more-btn { background: linear-gradient(135deg, rgba(139,92,246,0.15), rgba(124,58,237,0.1)); border: 1px solid rgba(139,92,246,0.3); color: #C4B5FD; padding: 14px 32px; border-radius: 12px; font-weight: 700; font-size: 14px; cursor: pointer; transition: all 0.3s; display: inline-flex; align-items: center; gap: 10px; font-family: inherit; }
    .v29-more-btn:hover { background: linear-gradient(135deg, rgba(139,92,246,0.25), rgba(124,58,237,0.15)); border-color: rgba(139,92,246,0.5); transform: translateY(-2px); box-shadow: 0 8px 24px rgba(139,92,246,0.15); }
    .v29-more-btn svg { width: 14px; height: 14px; transition: transform 0.3s; }
    .v29-more-btn.v29-expanded svg { transform: rotate(180deg); }"""


def build_section(title_html, faq_data, has_categories=False):
    """Build the full V29 FAQ <section> block.

    title_html: the inner HTML for the <h2> heading (can include <span>).
    faq_data:   list of dicts {q, a, cat?}
    has_categories: whether to render category tabs
    """
    cat_html = '<div class="flex flex-wrap justify-center gap-2 mb-8" id="v29-tabs"></div>\n      ' if has_categories else ''
    js_data = ',\n          '.join(
        '{ q: ' + repr(item['q']).replace("'", '"') + ', a: ' + repr(item['a']).replace("'", '"') +
        (', cat: ' + repr(item.get('cat', '')).replace("'", '"') if has_categories else '') + ' }'
        for item in faq_data
    )

    cat_tabs_js = '''var faqCategories = [
          {name:"ყველა", key:"all"}, {name:"ზოგადი", key:"general"}, {name:"ფასი", key:"price"}, {name:"შედეგები", key:"results"}
        ];
        var tabs=document.getElementById('v29-tabs'), activeCat='ყველა';
        faqCategories.forEach(function(item){
          var cat=item.name, t=document.createElement('button');
          t.className='v29-tab'+(cat==='ყველა'?' v29-active':'');
          t.setAttribute('data-cat', item.key);
          t.textContent=cat;
          t.onclick=function(){ activeCat=cat; tabs.querySelectorAll('.v29-tab').forEach(function(b){b.classList.remove('v29-active');}); t.classList.add('v29-active'); filter(); };
          tabs.appendChild(t);
        });
        var catKeyMap={"ზოგადი":"general","ფასი":"price","შედეგები":"results"};''' if has_categories else "var activeCat='ყველა'; var catKeyMap={};"

    cat_filter_js = "el.getAttribute('data-cat')===activeCat" if has_categories else "true"
    cat_render = "var ck=catKeyMap[faq.cat]||'';" if has_categories else "var ck='';"
    cat_html_render = "+'<span class=\"v29-cat\" data-key=\"'+ck+'\">'+(faq.cat||'')+'</span>'" if has_categories else "+''"
    cat_attr = "d.setAttribute('data-cat',faq.cat||'');" if has_categories else ""

    return f'''  <!-- ========== FAQ — V29 Gold Glassmorphism ========== -->
  <section id="faq" class="relative py-16 lg:py-24 overflow-hidden bg-white dark:bg-surface-dark">
    <div class="absolute inset-0 dark:block hidden" style="background: radial-gradient(ellipse at 30% 20%, rgba(139,92,246,0.04) 0%, transparent 50%), radial-gradient(ellipse at 70% 80%, rgba(124,58,237,0.03) 0%, transparent 50%);"></div>
    <div class="max-w-3xl mx-auto px-4 sm:px-6 relative z-10">
      <div class="text-center mb-8">
        <p class="text-sm font-semibold uppercase tracking-wider mb-3" style="color:#D4A017">FAQ</p>
        <h2 class="font-heading text-[24px] sm:text-[30px] lg:text-[36px] font-bold text-heading dark:text-heading-dark leading-[1.3]">{title_html}</h2>
      </div>
      {cat_html}<div class="space-y-3" id="v29-items"></div>
      <div class="v29-more-wrap" id="v29-more-wrap">
        <button class="v29-more-btn" id="v29-more-btn" type="button">
          <span id="v29-more-txt">დანარჩენი კითხვების ნახვა</span>
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7"/></svg>
        </button>
      </div>
    </div>
    <script>
      (function(){{
        var faqData = [
          {js_data}
        ];
        var list=document.getElementById('v29-items');
        var moreBtn=document.getElementById('v29-more-btn'), moreWrap=document.getElementById('v29-more-wrap'), moreTxt=document.getElementById('v29-more-txt');
        var INITIAL=6, expanded=false;
        {cat_tabs_js}
        faqData.forEach(function(faq){{
          var d=document.createElement('div'); {cat_render}
          d.className='v29-card'; {cat_attr}
          d.innerHTML='<div class="v29-cq"><div class="v29-badge"><svg fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg></div><span class="v29-txt">'+faq.q+'</span>'{cat_html_render}+'</div><div class="v29-ca"><p>'+faq.a+'</p></div>';
          d.querySelector('.v29-cq').onclick=function(){{ var o=d.classList.contains('v29-open'); list.querySelectorAll('.v29-card').forEach(function(el){{el.classList.remove('v29-open');}}); if(!o) d.classList.add('v29-open'); }};
          list.appendChild(d);
        }});
        function filter(){{
          var matchedCount=0;
          list.querySelectorAll('.v29-card').forEach(function(el){{
            el.classList.remove('v29-open');
            el.classList.remove('v29-extra-hidden');
            var match = activeCat==='ყველა' || {cat_filter_js};
            if(match){{ el.classList.remove('v29-hidden'); matchedCount++; if(!expanded && matchedCount>INITIAL) el.classList.add('v29-extra-hidden'); }}
            else {{ el.classList.add('v29-hidden'); }}
          }});
          var remainder = matchedCount - INITIAL;
          if(remainder>0){{ moreWrap.classList.remove('v29-hidden'); moreTxt.textContent = expanded ? 'ნაკლების ჩვენება' : ('დანარჩენი ' + remainder + ' კითხვის ნახვა'); }}
          else {{ moreWrap.classList.add('v29-hidden'); }}
        }}
        moreBtn.addEventListener('click', function(){{ expanded=!expanded; moreBtn.classList.toggle('v29-expanded', expanded); filter(); }});
        filter();
      }})();
    </script>
  </section>'''


# ============================================================
# Per-variant data extractors
# ============================================================

JS_DATA_RE = re.compile(
    r'var\s+(?:data|faqData)\s*=\s*\[(.*?)\];',
    re.DOTALL,
)
JS_ITEM_RE = re.compile(
    r'\{\s*q\s*:\s*"((?:[^"\\]|\\.)*)"\s*,\s*a\s*:\s*"((?:[^"\\]|\\.)*)"(?:\s*,\s*cat\s*:\s*"((?:[^"\\]|\\.)*)")?'
    r'(?:\s*,\s*video\s*:\s*(?:true|false))?\s*\}',
)


def extract_from_js_array(html):
    """Variant: fq1-list / v29-items driven by JS data array."""
    m = JS_DATA_RE.search(html)
    if not m:
        return None
    items = []
    has_cat = False
    for m2 in JS_ITEM_RE.finditer(m.group(1)):
        q, a, cat = m2.group(1), m2.group(2), m2.group(3)
        # Unescape
        q = q.replace('\\"', '"').replace("\\'", "'")
        a = a.replace('\\"', '"').replace("\\'", "'")
        item = {'q': q, 'a': a}
        if cat:
            item['cat'] = cat
            has_cat = True
        items.append(item)
    return items, has_cat


def _strip_tags(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()


def extract_from_faq_item(html):
    """Variant: <div class="faq-item">...<span>Q</span>...<p|div>A</p|div></div>"""
    items = []
    # Walk each faq-item div individually, extract Q (first <span>) + A (first <p> OR first <div class="faq-answer"> inner)
    item_re = re.compile(r'<div class="faq-item[^"]*"[^>]*>(.*?)(?=<div class="faq-item|</div>\s*</div>\s*</section|</div>\s*</section)', re.DOTALL)
    span_re = re.compile(r'<span[^>]*>([^<]+)</span>')
    p_re    = re.compile(r'<p[^>]*>(.*?)</p>', re.DOTALL)
    ans_re  = re.compile(r'<div class="faq-answer"[^>]*>(.*?)</div>\s*</div>', re.DOTALL)

    # Simpler approach: split by `<div class="faq-item`
    parts = re.split(r'<div class="faq-item', html)
    for part in parts[1:]:
        sm = span_re.search(part)
        if not sm:
            continue
        q = sm.group(1).strip()
        # Try <p> first, fallback to faq-answer wrapper
        am = p_re.search(part)
        if am:
            a = _strip_tags(am.group(1))
        else:
            am2 = ans_re.search(part)
            if not am2:
                continue
            a = _strip_tags(am2.group(1))
        if q and a:
            items.append({'q': q, 'a': a})
    return items, False


def extract_from_fq1_card(html):
    """Variant: <div class="fq1-card">...<span class="fq1-txt">Q</span>...<div class="fq1-a"><p>A</p></div>"""
    items = []
    parts = re.split(r'<div class="fq1-card"', html)
    txt_re = re.compile(r'class="fq1-txt"[^>]*>([^<]+)<')
    ans_re = re.compile(r'class="fq1-a[^"]*"[^>]*>(.*?)</div>', re.DOTALL)
    for part in parts[1:]:
        tm = txt_re.search(part)
        am = ans_re.search(part)
        if tm and am:
            items.append({'q': tm.group(1).strip(), 'a': _strip_tags(am.group(1))})
    return items, False


def extract_from_pfaq(html):
    """Variant: pfaq-item OR fq-card.

    pfaq:  <div class="pfaq-item">...<div class="pfaq-txt">Q</div>...<div class="pfaq-a">A</div>
    fq:    <div class="fq-card">...<div class="fq-txt">Q</div>...<div class="fq-a">A</div>
    """
    items = []
    # Try pfaq-item first, then fq-card
    for class_prefix in ('pfaq', 'fq'):
        cls = class_prefix + '-item' if class_prefix == 'pfaq' else class_prefix + '-card'
        parts = re.split(r'<div class="' + re.escape(cls) + r'"', html)
        if len(parts) < 2:
            continue
        txt_re = re.compile(r'class="' + class_prefix + r'-txt"[^>]*>([^<]+)<')
        ans_re = re.compile(r'class="' + class_prefix + r'-a[^"]*"[^>]*>(.*?)</div>', re.DOTALL)
        for part in parts[1:]:
            tm = txt_re.search(part)
            am = ans_re.search(part)
            if tm and am:
                items.append({'q': tm.group(1).strip(), 'a': _strip_tags(am.group(1))})
        if items:
            return items, False
    return items, False


def extract_from_details(html):
    """Variant: <details><summary>Q</summary>A</details>"""
    items = []
    pattern = re.compile(
        r'<details[^>]*>\s*<summary[^>]*>(.*?)</summary>(.*?)</details>',
        re.DOTALL,
    )
    for m in pattern.finditer(html):
        q = re.sub(r'<[^>]+>', ' ', m.group(1)).strip()
        q = re.sub(r'\s+', ' ', q)
        a = re.sub(r'<[^>]+>', ' ', m.group(2)).strip()
        a = re.sub(r'\s+', ' ', a)
        items.append({'q': q, 'a': a})
    return items, False


# ============================================================
# Section locator + replacer
# ============================================================

def find_faq_section(html):
    """Find the <section ...> ... </section> bounds containing 'ხშირად დასმული'.

    Tries (1) <h2>/<h1> tag containing the text, (2) <section id="faq">.
    """
    # Try heading first — match across embedded tags by stopping at </h1|2>
    heading_re = re.compile(r'<h[12][^>]*>[^<]*ხშირად დასმული.*?</h[12]>', re.DOTALL)
    h_match = heading_re.search(html)
    if h_match:
        h_pos = h_match.start()
    else:
        # Fallback: <section id="faq" ...>
        sec_re = re.compile(r'<section[^>]*id="faq"[^>]*>')
        m = sec_re.search(html)
        if not m:
            return None
        # Use the section open as anchor; find its matching close
        h_pos = m.end()

    # Walk backwards to find enclosing <section ...>
    open_re = re.compile(r'<section[^>]*>')
    last_open = None
    for m in open_re.finditer(html, 0, h_pos + 1):
        last_open = m
    if not last_open:
        return None

    # Now find matching </section> after h_pos with nesting tracking
    depth = 1
    pos = last_open.end()
    while pos < len(html):
        next_open = html.find('<section', pos)
        next_close = html.find('</section>', pos)
        if next_close == -1:
            return None
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + len('<section')
        else:
            depth -= 1
            if depth == 0:
                return (last_open.start(), next_close + len('</section>'))
            pos = next_close + len('</section>')
    return None


def find_h2_inner(html, start, end):
    """Extract the inner HTML of the <h2> within the section."""
    section = html[start:end]
    m = re.search(r'<h2[^>]*>(.*?)</h2>', section, re.DOTALL)
    if not m:
        return 'ხშირად დასმული კითხვები'
    return m.group(1).strip()


# ============================================================
# Pipeline
# ============================================================

EXTRACTORS = [
    ('v29-items + JS', extract_from_js_array, lambda h: 'id="v29-items"' in h or 'id="fq1-list"' in h or 'id="faq-container"' in h),
    ('fq1-card HTML', extract_from_fq1_card,  lambda h: 'class="fq1-card"' in h),
    ('pfaq/fq-card',  extract_from_pfaq,      lambda h: 'class="pfaq-item"' in h or 'class="fq-card"' in h),
    ('faq-item HTML', extract_from_faq_item,  lambda h: 'class="faq-item' in h),
    ('<details>',     extract_from_details,   lambda h: '<details' in h and '<summary' in h),
]


def patch_file(path: Path, dry_run=False):
    text = path.read_text(encoding='utf-8')

    bounds = find_faq_section(text)
    if not bounds:
        return ('NO_FAQ', None, None)
    start, end = bounds
    section = text[start:end]

    # Detect variant + extract
    variant_name = None
    items = None
    for name, fn, detect in EXTRACTORS:
        if detect(section):
            result = fn(section)
            if result and result[0]:
                items, _ = result
                variant_name = name
                break

    if not items:
        return ('EXTRACT_FAILED', section[:200], None)

    # Force categories OFF on non-homepage pages to keep visual unity
    # (homepage uses 4 fixed categories; other pages have varying schemas)
    items_no_cat = [{'q': it['q'], 'a': it['a']} for it in items]
    title = find_h2_inner(text, start, end)
    new_section = build_section(title, items_no_cat, has_categories=False)

    # Expand bounds to swallow leftover banner comments immediately before/after
    expand_start = start
    while expand_start > 0:
        # Look for HTML comment block on its own line preceding the section
        prev_line_end = text.rfind('\n', 0, expand_start - 1)
        if prev_line_end == -1:
            break
        line_start = text.rfind('\n', 0, prev_line_end - 1) + 1
        line = text[line_start:prev_line_end].strip()
        if line.startswith('<!--') and line.endswith('-->'):
            expand_start = line_start
        else:
            break

    expand_end = end
    while expand_end < len(text):
        next_nl = text.find('\n', expand_end)
        if next_nl == -1:
            break
        line = text[expand_end:next_nl].strip()
        if not line:
            expand_end = next_nl + 1
        else:
            break

    new_text = text[:expand_start] + new_section + text[expand_end:]

    # Strip pre-existing v29-* CSS blocks (clean rebuild) — match CSS rules only
    new_text = re.sub(
        r'\n\s*/\* FAQ v29[^\n]*\*/\n(\s*\.v29-[^\n]*\n)+',
        '\n',
        new_text,
    )

    # Inject fresh V29 CSS into the first <style> block (idempotent).
    # Check for CSS RULE (.v29-card { ...) not the string 'v29-card' which
    # appears in JS regardless. Look for selectors followed by `{`.
    has_css = bool(re.search(r'\.v29-card\s*\{', new_text))
    if not has_css:
        m = re.search(r'(<style[^>]*>)', new_text)
        if m:
            insert = m.end()
            new_text = new_text[:insert] + '\n' + V29_CSS + '\n' + new_text[insert:]

    if dry_run:
        return ('OK_DRY', variant_name, len(items))

    path.write_text(new_text, encoding='utf-8')
    return ('OK', variant_name, len(items))


# ============================================================
# Main
# ============================================================

TARGETS = [
    # Production service pages
    'seo-audit.html',
    'seo-management.html',
    'seo-consultation.html',
    'seo-course.html',
    'seo-copywriting.html',
    'copywriting.html',
    'cro.html',
    'google-ads.html',
    'ai-seo.html',
    'keyword-research.html',
    'roi-calculator.html',
    # Offer pages (production)
    'offer.html',
    'offer-premium.html',
    'offer-premium-convert.html',
    'offer-premium-brand.html',
    # Skipped intentionally:
    #   index.html (already done manually)
    #   seo-management-v2/v3/v4 (alternate terminal designs)
    #   offer-v2..v9 (alternate designs)
    #   offer-deal-room.html (deal room <details> blocks ≠ FAQ)
    #   faq.html (prototype gallery v1-v13)
]


def main():
    dry = '--dry' in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith('--')]
    targets = only if only else TARGETS

    print(f"{'DRY RUN' if dry else 'APPLY'} mode\n")
    for name in targets:
        path = ROOT / name
        if not path.exists():
            print(f"  SKIP   {name} (not found)")
            continue
        try:
            status, info, count = patch_file(path, dry_run=dry)
            print(f"  {status:14s} {name:38s} {info or ''}  ({count} Qs)" if count else f"  {status:14s} {name:38s} {info or ''}")
        except Exception as e:
            print(f"  ERROR          {name:38s} {e}")


if __name__ == '__main__':
    main()
