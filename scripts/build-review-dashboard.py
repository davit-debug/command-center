#!/usr/bin/env python3
"""Parse translation-review.md → generate interactive HTML picker dashboard.

Output: /Users/imac/SEO/translation-dashboard.html — single self-contained file
with localStorage persistence and JSON export of selections.
"""
import json
import re
from pathlib import Path

REVIEW_MD = Path("/Users/imac/SEO/translation-review.md")
OUTPUT = Path("/Users/imac/SEO/translation-dashboard.html")


def parse_review(md_text: str) -> dict:
    """Parse review file into structured data."""
    pages = []
    current_page = None
    current_fragment = None

    page_re = re.compile(r'^# \d+\.\s+(.+?)(?:\s+—\s+(.+))?$')
    # Looser fragment regex — accept any non-special char in label
    fragment_re = re.compile(r'^## ([^—\n]+?)(?:\s+—\s+(.+))?$')
    option_re = re.compile(r'^\s*-\s+\[([ x])\]\s+(\*\*)?(V\d+|Custom[^:]*?):\s*`?(.+?)`?(?:\s+\((\d+\s*chars[^)]*)\))?(?:\s*\*\*)?(?:\s+←\s+(APPLIED))?$')

    # Helper to clean trailing backticks/asterisks artifacts from parsed text
    def clean(s):
        s = s.strip()
        # Strip trailing `**, **, `, ** patterns
        s = re.sub(r'`?\*\*$', '', s).strip()
        s = s.rstrip('`').strip()
        return s

    for line in md_text.split('\n'):
        # Match page header (skip "Other pages — Not in this review")
        m = page_re.match(line)
        if m and '/en/' in m.group(1):
            title = m.group(1).strip()
            status = m.group(2).strip() if m.group(2) else ''
            current_page = {
                'title': title,
                'status': status,
                'fragments': []
            }
            pages.append(current_page)
            current_fragment = None
            continue

        # Match fragment header
        m = fragment_re.match(line)
        if m and current_page:
            label = m.group(1).strip()
            status = m.group(2).strip() if m.group(2) else ''
            if label.lower().startswith('how to use'):
                continue
            current_fragment = {
                'label': label,
                'status': status,
                'options': []
            }
            current_page['fragments'].append(current_fragment)
            continue

        # Match option
        m = option_re.match(line)
        if m and current_fragment:
            checked = m.group(1) == 'x'
            version = m.group(3).strip()
            text = clean(m.group(4))
            meta = m.group(5).strip() if m.group(5) else ''
            applied = m.group(6) == 'APPLIED'
            current_fragment['options'].append({
                'version': version,
                'text': text,
                'meta': meta,
                'checked': checked,
                'applied': applied,
            })

    return {'pages': pages}


def build_html(data: dict) -> str:
    pages_json = json.dumps(data, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
<meta charset="UTF-8">
<title>10xSEO Translation Picker Dashboard</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root {{
  --bg: #0a0a14;
  --surface: #12121f;
  --surface-2: #1a1a2e;
  --border: #2a2a3e;
  --primary: #8B5CF6;
  --primary-hover: #A78BFA;
  --accent: #14B8A6;
  --gold: #D4A017;
  --success: #22c55e;
  --text: #e2e8f0;
  --text-dim: #94a3b8;
  --text-faint: #64748b;
}}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; background: var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, "Inter", "FiraGO", sans-serif; line-height: 1.5; }}

.layout {{ display: grid; grid-template-columns: 260px 1fr; min-height: 100vh; }}

aside {{
  background: var(--surface);
  border-right: 1px solid var(--border);
  padding: 24px 16px;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
}}
aside .brand {{ font-weight: 900; font-size: 18px; margin-bottom: 4px; }}
aside .brand span {{ color: var(--gold); }}
aside .sub {{ font-size: 12px; color: var(--text-dim); margin-bottom: 24px; }}
aside .nav-item {{
  display: block; padding: 10px 12px; border-radius: 8px;
  text-decoration: none; color: var(--text-dim); font-size: 14px; margin-bottom: 4px;
  cursor: pointer; transition: all 0.15s;
}}
aside .nav-item:hover {{ background: var(--surface-2); color: var(--text); }}
aside .nav-item.active {{ background: var(--primary); color: white; }}
aside .nav-item .status {{
  display: inline-block; margin-left: 6px; padding: 2px 6px; border-radius: 999px;
  font-size: 10px; font-weight: 700;
}}
aside .nav-item .status.done {{ background: var(--success); color: white; }}
aside .nav-item .status.pending {{ background: var(--gold); color: black; }}
aside .nav-item .status.partial {{ background: var(--accent); color: white; }}

main {{ padding: 32px 40px; max-width: 1100px; }}
h1.title {{ font-size: 28px; font-weight: 900; margin: 0 0 4px; }}
.subtitle {{ color: var(--text-dim); margin-bottom: 32px; font-size: 14px; }}

.page-block {{ display: none; }}
.page-block.active {{ display: block; }}

.fragment {{
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 20px;
}}
.fragment-header {{ display: flex; align-items: baseline; justify-content: space-between; margin-bottom: 16px; }}
.fragment-label {{ font-size: 14px; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 1px; }}
.fragment-status {{ font-size: 11px; color: var(--text-dim); }}

.options {{ display: flex; flex-direction: column; gap: 10px; }}
.option {{
  border: 1.5px solid var(--border);
  border-radius: 10px;
  padding: 12px 16px;
  cursor: pointer;
  transition: all 0.15s;
  background: var(--surface-2);
  position: relative;
}}
.option:hover {{ border-color: var(--primary); background: rgba(139, 92, 246, 0.05); }}
.option.selected {{ border-color: var(--primary); background: rgba(139, 92, 246, 0.12); box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.3); }}
.option.applied {{ border-color: var(--success); }}
.option.applied::after {{
  content: "✓ APPLIED";
  position: absolute; top: 8px; right: 12px;
  font-size: 10px; font-weight: 700;
  background: var(--success); color: white;
  padding: 2px 8px; border-radius: 999px;
}}
.option-version {{ font-size: 12px; font-weight: 700; color: var(--primary-hover); margin-bottom: 4px; }}
.option-text {{ font-size: 14px; color: var(--text); line-height: 1.5; }}
.option-meta {{ font-size: 11px; color: var(--text-faint); margin-top: 4px; }}

.custom-input {{
  width: 100%;
  background: var(--surface-2);
  border: 1.5px solid var(--border);
  border-radius: 10px;
  padding: 12px 16px;
  color: var(--text);
  font-family: inherit;
  font-size: 14px;
  resize: vertical;
  min-height: 60px;
}}
.custom-input:focus {{ outline: none; border-color: var(--primary); }}

footer.actions {{
  position: fixed;
  bottom: 0; left: 260px; right: 0;
  background: var(--surface);
  border-top: 1px solid var(--border);
  padding: 16px 40px;
  display: flex; align-items: center; justify-content: space-between;
  z-index: 100;
}}
.stats {{ color: var(--text-dim); font-size: 13px; }}
.stats strong {{ color: var(--text); }}
.btn {{
  background: var(--primary); color: white;
  border: none; border-radius: 8px;
  padding: 10px 20px; font-weight: 700; cursor: pointer;
  font-size: 14px; transition: all 0.15s;
}}
.btn:hover {{ background: var(--primary-hover); }}
.btn.secondary {{ background: var(--surface-2); border: 1px solid var(--border); }}
.btn.secondary:hover {{ background: var(--surface); color: var(--text); }}

#modal {{
  display: none;
  position: fixed; inset: 0;
  background: rgba(0, 0, 0, 0.8);
  z-index: 200;
  align-items: center; justify-content: center;
}}
#modal.open {{ display: flex; }}
.modal-content {{
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 32px;
  max-width: 720px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}}
.modal-content h2 {{ margin-top: 0; }}
.modal-content pre {{
  background: var(--bg);
  border-radius: 8px;
  padding: 16px;
  overflow-x: auto;
  font-size: 12px;
  color: var(--accent);
  user-select: all;
}}
.modal-actions {{ display: flex; gap: 12px; justify-content: flex-end; margin-top: 20px; }}

main {{ padding-bottom: 100px; }}
</style>
</head>
<body>
<div class="layout">
  <aside>
    <div class="brand">10x<span>SEO</span></div>
    <div class="sub">Translation Picker</div>
    <div id="nav"></div>
  </aside>

  <main>
    <h1 class="title">Translation Variant Picker</h1>
    <p class="subtitle">Click a card to select. Choices auto-save to your browser. Click "Export Selections" when done.</p>
    <div id="content"></div>
  </main>
</div>

<footer class="actions">
  <div class="stats">
    <strong id="picked-count">0</strong> / <strong id="total-count">0</strong> picked
    · <strong id="page-count">5</strong> pages
  </div>
  <div style="display:flex; gap:12px;">
    <button class="btn secondary" onclick="resetAll()">Reset All</button>
    <button class="btn" onclick="showExport()">Export Selections</button>
  </div>
</footer>

<div id="modal">
  <div class="modal-content">
    <h2>Your Selections</h2>
    <p style="color: var(--text-dim);">Copy the JSON below and send to Claude:<br>
    <em style="font-size:13px">"გადმოაკოპირე ფაილიდან გადაწყვეტილებები: [paste JSON]"</em></p>
    <pre id="export-json"></pre>
    <div class="modal-actions">
      <button class="btn secondary" onclick="closeModal()">Close</button>
      <button class="btn" onclick="copyJson()">Copy to Clipboard</button>
    </div>
  </div>
</div>

<script>
const DATA = {pages_json};
const STORAGE_KEY = "10xseo-translation-picks-v1";
const CURRENT_PAGE_KEY = "10xseo-current-page-v1";

// Load persisted selections + active page
let picks = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{{}}");
let currentPageIdx = parseInt(localStorage.getItem(CURRENT_PAGE_KEY) || "0");
if (isNaN(currentPageIdx) || currentPageIdx < 0 || currentPageIdx >= DATA.pages.length) currentPageIdx = 0;

function savePicks() {{
  localStorage.setItem(STORAGE_KEY, JSON.stringify(picks));
  updateStats();
}}

function pageId(page) {{
  return page.title.replace(/[^a-z0-9]/gi, '-').toLowerCase();
}}

function fragmentId(pageIdx, fragIdx) {{
  return `p${{pageIdx}}f${{fragIdx}}`;
}}

function renderNav() {{
  const nav = document.getElementById('nav');
  nav.innerHTML = DATA.pages.map((p, i) => {{
    const pickedInPage = p.fragments.filter((f, fi) => picks[fragmentId(i, fi)] !== undefined).length;
    const total = p.fragments.length;
    let statusClass = 'pending';
    let statusTxt = `${{pickedInPage}}/${{total}}`;
    if (pickedInPage === total) statusClass = 'done';
    else if (pickedInPage > 0) statusClass = 'partial';
    if (p.status && p.status.includes('APPLIED')) {{ statusClass = 'done'; statusTxt = '✓'; }}
    return `<div class="nav-item ${{i===currentPageIdx?'active':''}}" data-page="${{i}}" onclick="showPage(${{i}})">${{p.title.replace('/en/','').replace('.html','')}} <span class="status ${{statusClass}}">${{statusTxt}}</span></div>`;
  }}).join('');
}}

function renderPage(pageIdx) {{
  currentPageIdx = pageIdx;
  localStorage.setItem(CURRENT_PAGE_KEY, String(pageIdx));
  const page = DATA.pages[pageIdx];
  const content = document.getElementById('content');
  content.innerHTML = `<div class="page-block active" id="${{pageId(page)}}">
    <h2 style="margin-top:0;">${{page.title}} ${{page.status ? `<span style="font-size:13px; color:var(--text-dim); font-weight:400;">— ${{page.status}}</span>` : ''}}</h2>
    ${{page.fragments.map((frag, fi) => renderFragment(pageIdx, fi, frag)).join('')}}
  </div>`;
  // Highlight nav
  document.querySelectorAll('.nav-item').forEach((el, i) => el.classList.toggle('active', i === pageIdx));
  // Scroll main to top after page switch
  window.scrollTo({{top: 0, behavior: 'smooth'}});
}}

function renderFragment(pageIdx, fragIdx, frag) {{
  const fid = fragmentId(pageIdx, fragIdx);
  const currentPick = picks[fid];
  return `<div class="fragment">
    <div class="fragment-header">
      <div class="fragment-label">${{frag.label}}</div>
      <div class="fragment-status">${{frag.status || ''}}</div>
    </div>
    <div class="options">
      ${{frag.options.map((opt, oi) => `
        <div class="option ${{currentPick === oi ? 'selected' : ''}} ${{opt.applied ? 'applied' : ''}}" onclick="pick('${{fid}}', ${{oi}})">
          <div class="option-version">${{opt.version}}${{opt.meta ? ' · ' + opt.meta : ''}}</div>
          <div class="option-text">${{escapeHtml(opt.text)}}</div>
        </div>
      `).join('')}}
      <div style="margin-top:8px;">
        <label style="font-size:11px; color:var(--text-dim); display:block; margin-bottom:6px;">Or write your own custom version:</label>
        <textarea class="custom-input" id="custom-${{fid}}" placeholder="Custom version..." onchange="pickCustom('${{fid}}', this.value)">${{currentPick && currentPick.custom ? escapeHtml(currentPick.custom) : ''}}</textarea>
      </div>
    </div>
  </div>`;
}}

function escapeHtml(s) {{
  return String(s).replace(/[&<>"']/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}})[c]);
}}

function showPage(idx) {{
  renderPage(idx);
}}

function pick(fid, optIdx) {{
  picks[fid] = optIdx;
  // Clear custom textarea if any
  const ta = document.getElementById(`custom-${{fid}}`);
  if (ta) ta.value = '';
  // Preserve scroll position across re-render
  const scrollY = window.scrollY;
  savePicks();
  rerenderCurrentPage();
  window.scrollTo(0, scrollY);
}}

function pickCustom(fid, value) {{
  if (!value.trim()) {{
    delete picks[fid];
  }} else {{
    picks[fid] = {{ custom: value.trim() }};
  }}
  const scrollY = window.scrollY;
  savePicks();
  rerenderCurrentPage();
  window.scrollTo(0, scrollY);
}}

function rerenderCurrentPage() {{
  const page = DATA.pages[currentPageIdx];
  const content = document.getElementById('content');
  content.innerHTML = `<div class="page-block active" id="${{pageId(page)}}">
    <h2 style="margin-top:0;">${{page.title}} ${{page.status ? `<span style="font-size:13px; color:var(--text-dim); font-weight:400;">— ${{page.status}}</span>` : ''}}</h2>
    ${{page.fragments.map((frag, fi) => renderFragment(currentPageIdx, fi, frag)).join('')}}
  </div>`;
}}

function updateStats() {{
  const total = DATA.pages.reduce((sum, p) => sum + p.fragments.length, 0);
  const picked = Object.keys(picks).length;
  document.getElementById('total-count').textContent = total;
  document.getElementById('picked-count').textContent = picked;
  document.getElementById('page-count').textContent = DATA.pages.length;
  renderNav();
}}

function resetAll() {{
  if (!confirm('Reset all selections?')) return;
  picks = {{}};
  localStorage.removeItem(STORAGE_KEY);
  updateStats();
  showPage(0);
}}

function showExport() {{
  const out = {{}};
  DATA.pages.forEach((p, i) => {{
    const pageKey = p.title.match(/\\/en\\/[\\w-]+\\.html/)?.[0] || p.title;
    out[pageKey] = {{}};
    p.fragments.forEach((f, fi) => {{
      const fid = fragmentId(i, fi);
      const pick = picks[fid];
      if (pick === undefined) return;
      if (typeof pick === 'object' && pick.custom) {{
        out[pageKey][f.label] = {{ custom: pick.custom }};
      }} else {{
        const opt = f.options[pick];
        out[pageKey][f.label] = {{ version: opt.version, text: opt.text }};
      }}
    }});
  }});
  document.getElementById('export-json').textContent = JSON.stringify(out, null, 2);
  document.getElementById('modal').classList.add('open');
}}

function closeModal() {{ document.getElementById('modal').classList.remove('open'); }}

function copyJson() {{
  const txt = document.getElementById('export-json').textContent;
  navigator.clipboard.writeText(txt).then(() => {{
    const btn = event.target;
    const orig = btn.textContent;
    btn.textContent = '✓ Copied';
    setTimeout(() => btn.textContent = orig, 1500);
  }});
}}

// Init — restore last page user was on
renderNav();
showPage(currentPageIdx);
updateStats();
</script>
</body>
</html>"""


def main():
    md = REVIEW_MD.read_text(encoding="utf-8")
    data = parse_review(md)
    total_options = sum(
        len(f["options"])
        for p in data["pages"]
        for f in p["fragments"]
    )
    print(f"Parsed: {len(data['pages'])} pages, "
          f"{sum(len(p['fragments']) for p in data['pages'])} fragments, "
          f"{total_options} options")
    html = build_html(data)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"✓ Wrote {OUTPUT} ({len(html)} bytes)")


if __name__ == "__main__":
    main()
