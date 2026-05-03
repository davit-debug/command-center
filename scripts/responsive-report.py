#!/usr/bin/env python3
"""
Responsive Audit — HTML dashboard generator

Reads audit/responsive/data/*.json and generates audit/responsive/report.html
with:
  - Severity-ranked issue list
  - Per-page × per-viewport grid with screenshot thumbnails
  - Issue clustering (same problem on N pages)
  - Aggregate stats

Usage:  audit/.venv/bin/python scripts/responsive-report.py
"""
import json
import html
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT = REPO_ROOT / 'audit' / 'responsive'
DATA = OUTPUT / 'data'
REPORT = OUTPUT / 'report.html'

VIEWPORTS = ['mobile-sm', 'mobile-md', 'tablet', 'laptop', 'desktop']

SEVERITY_ORDER = {'critical': 0, 'serious': 1, 'moderate': 2, 'minor': 3, None: 4}
SEVERITY_COLORS = {
    'critical': '#dc2626', 'serious': '#ea580c',
    'moderate': '#d97706', 'minor': '#65a30d', None: '#64748b'
}


def load_pages():
    pages = []
    for jf in sorted(DATA.glob('*.json')):
        with open(jf, encoding='utf-8') as f:
            pages.append(json.load(f))
    return pages


def cluster_issues(pages):
    """Group axe violations by rule ID across all pages."""
    by_rule = defaultdict(list)
    for p in pages:
        for vp_name, vp_data in p['viewports'].items():
            for v in vp_data.get('axe_violations', []) or []:
                by_rule[v['id']].append({
                    'page': p['page'],
                    'viewport': vp_name,
                    'impact': v['impact'],
                    'help': v['help'],
                    'description': v['description'],
                    'nodes': v['nodes'],
                    'sample': v.get('sample', []),
                })
    clusters = []
    for rule_id, instances in by_rule.items():
        unique_pages = sorted(set(i['page'] for i in instances))
        impact = instances[0]['impact']
        clusters.append({
            'rule_id': rule_id,
            'impact': impact,
            'help': instances[0]['help'],
            'description': instances[0]['description'],
            'instances': instances,
            'page_count': len(unique_pages),
            'pages': unique_pages,
            'total_nodes': sum(i['nodes'] for i in instances),
        })
    clusters.sort(key=lambda c: (SEVERITY_ORDER.get(c['impact'], 4), -c['page_count']))
    return clusters


def aggregate_stats(pages):
    stats = {
        'total_pages': len(pages),
        'total_viewport_runs': 0,
        'pages_with_overflow': set(),
        'pages_with_cls_issues': set(),
        'pages_with_touch_issues': set(),
        'pages_with_console_errors': set(),
        'pages_with_load_errors': [],
        'total_touch_violations': 0,
        'total_axe_violations': 0,
    }
    for p in pages:
        for vp, vd in p['viewports'].items():
            stats['total_viewport_runs'] += 1
            if vd.get('error'):
                stats['pages_with_load_errors'].append(f"{p['page']} ({vp})")
                continue
            if vd.get('has_horizontal_overflow'):
                stats['pages_with_overflow'].add(p['page'])
            if (vd.get('cls') or 0) > 0.1:
                stats['pages_with_cls_issues'].add(p['page'])
            if vd.get('touch_targets_under_44px'):
                stats['pages_with_touch_issues'].add(p['page'])
                stats['total_touch_violations'] += len(vd['touch_targets_under_44px'])
            if vd.get('console_errors') or vd.get('page_errors'):
                stats['pages_with_console_errors'].add(p['page'])
            stats['total_axe_violations'] += len(vd.get('axe_violations', []) or [])
    return stats


def generate_html(pages, clusters, stats):
    out = []
    out.append('''<!DOCTYPE html>
<html lang="ka">
<head>
<meta charset="UTF-8">
<title>Responsive Audit — 10xseo.ge</title>
<style>
:root { --bg:#020710; --card:#0f172a; --muted:#94a3b8; --text:#f8fafc;
        --accent:#8b5cf6; --good:#22c55e; --warn:#f59e0b; --bad:#ef4444; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: var(--bg); color: var(--text); font: 14px/1.5 system-ui, -apple-system, sans-serif; padding: 24px; }
h1 { font-size: 28px; margin-bottom: 4px; }
h2 { font-size: 20px; margin: 32px 0 12px; padding-bottom: 6px; border-bottom: 1px solid #1e293b; }
h3 { font-size: 16px; margin: 16px 0 8px; }
.muted { color: var(--muted); }
.row { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; }
.stat { background: var(--card); padding: 16px; border-radius: 8px; border: 1px solid #1e293b; }
.stat .v { font-size: 28px; font-weight: 700; }
.stat .l { font-size: 12px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; }
.stat.bad .v { color: var(--bad); }
.stat.warn .v { color: var(--warn); }
.stat.good .v { color: var(--good); }
.cluster { background: var(--card); border: 1px solid #1e293b; border-radius: 8px; padding: 16px; margin-bottom: 12px; }
.cluster .impact { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700; text-transform: uppercase; color: white; }
.cluster details summary { cursor: pointer; padding: 8px 0; color: var(--muted); }
.cluster .pages { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 8px; }
.cluster .pages span { background: #1e293b; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-family: ui-monospace, monospace; }
.page { background: var(--card); border: 1px solid #1e293b; border-radius: 8px; padding: 16px; margin-bottom: 16px; }
.page h3 { font-family: ui-monospace, monospace; }
.viewports { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-top: 12px; }
.vp { background: #020710; border: 1px solid #1e293b; border-radius: 6px; overflow: hidden; }
.vp .head { padding: 8px 12px; font-size: 12px; display: flex; justify-content: space-between; align-items: center; background: #0f172a; }
.vp img { width: 100%; height: auto; display: block; max-height: 600px; object-fit: cover; object-position: top; cursor: zoom-in; }
.vp.has-issues .head { background: #450a0a; }
.badges { display: flex; gap: 4px; flex-wrap: wrap; padding: 6px 12px; background: #0f172a; }
.badge { font-size: 10px; padding: 2px 6px; border-radius: 3px; }
.badge.bad { background: var(--bad); color: white; }
.badge.warn { background: var(--warn); color: black; }
.badge.good { background: var(--good); color: black; }
.badge.muted { background: #1e293b; color: var(--muted); }
code { font-family: ui-monospace, monospace; background: #1e293b; padding: 1px 4px; border-radius: 3px; font-size: 12px; }
.lightbox { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.95); z-index: 100; padding: 24px; cursor: zoom-out; }
.lightbox.active { display: flex; align-items: center; justify-content: center; }
.lightbox img { max-width: 100%; max-height: 100%; }
nav.toc { background: var(--card); padding: 12px; border-radius: 8px; margin: 16px 0; font-size: 13px; }
nav.toc a { color: var(--accent); text-decoration: none; margin-right: 16px; }
.bad-text { color: var(--bad); }
.warn-text { color: var(--warn); }
.good-text { color: var(--good); }
</style>
</head>
<body>''')

    # Header
    out.append(f'<h1>Responsive Audit — 10xseo.ge</h1>')
    out.append(f'<p class="muted">{stats["total_pages"]} pages × {len(VIEWPORTS)} viewports = {stats["total_viewport_runs"]} runs</p>')

    out.append('<nav class="toc">')
    out.append('<a href="#stats">📊 Stats</a>')
    out.append('<a href="#clusters">🔥 Issue Clusters</a>')
    out.append('<a href="#pages">📄 Per-Page</a>')
    out.append('</nav>')

    # Stats
    out.append('<h2 id="stats">📊 Aggregate Stats</h2>')
    out.append('<div class="row">')
    overflow_count = len(stats['pages_with_overflow'])
    cls_count = len(stats['pages_with_cls_issues'])
    touch_count = len(stats['pages_with_touch_issues'])
    console_count = len(stats['pages_with_console_errors'])

    out.append(f'<div class="stat {"bad" if overflow_count else "good"}"><div class="v">{overflow_count}</div><div class="l">Pages with horizontal overflow</div></div>')
    out.append(f'<div class="stat {"bad" if cls_count else "good"}"><div class="v">{cls_count}</div><div class="l">Pages with CLS &gt; 0.1</div></div>')
    out.append(f'<div class="stat {"warn" if touch_count else "good"}"><div class="v">{touch_count}</div><div class="l">Pages with small touch targets</div></div>')
    out.append(f'<div class="stat warn"><div class="v">{stats["total_touch_violations"]}</div><div class="l">Total touch &lt; 44px</div></div>')
    out.append(f'<div class="stat {"bad" if console_count else "good"}"><div class="v">{console_count}</div><div class="l">Pages with console errors</div></div>')
    out.append(f'<div class="stat warn"><div class="v">{stats["total_axe_violations"]}</div><div class="l">Total a11y violations</div></div>')
    out.append(f'<div class="stat"><div class="v">{len(clusters)}</div><div class="l">Unique a11y rules failing</div></div>')
    out.append('</div>')

    # Clusters
    out.append('<h2 id="clusters">🔥 Issue Clusters (sorted by severity & spread)</h2>')
    if not clusters:
        out.append('<p class="muted good-text">✓ No accessibility violations.</p>')
    for c in clusters:
        col = SEVERITY_COLORS.get(c['impact'], '#64748b')
        out.append(f'<div class="cluster">')
        out.append(f'<div><span class="impact" style="background:{col}">{c["impact"] or "info"}</span> ')
        out.append(f'<strong>{html.escape(c["help"])}</strong> <code>{c["rule_id"]}</code></div>')
        out.append(f'<p class="muted" style="margin-top:8px">{html.escape(c["description"])}</p>')
        out.append(f'<p style="margin-top:8px">📄 <strong>{c["page_count"]}</strong> pages affected · <strong>{c["total_nodes"]}</strong> total elements</p>')
        out.append('<div class="pages">')
        for pg in c['pages'][:20]:
            out.append(f'<span>{html.escape(pg)}</span>')
        if len(c['pages']) > 20:
            out.append(f'<span>+{len(c["pages"])-20} more</span>')
        out.append('</div>')
        # Sample
        if c['instances'][0].get('sample'):
            out.append('<details><summary>Show sample HTML</summary>')
            for s in c['instances'][0]['sample'][:2]:
                out.append(f'<pre style="background:#020710;padding:8px;margin-top:6px;border-radius:4px;overflow-x:auto;font-size:11px">{html.escape(s.get("html",""))}</pre>')
                if s.get('failureSummary'):
                    out.append(f'<p class="muted" style="font-size:11px">{html.escape(s["failureSummary"])}</p>')
            out.append('</details>')
        out.append('</div>')

    # Per-page
    out.append('<h2 id="pages">📄 Per-Page Detail</h2>')
    for p in pages:
        page_path = p['page']
        out.append(f'<div class="page">')
        out.append(f'<h3>{html.escape(page_path)}</h3>')
        out.append('<div class="viewports">')
        for vp_name in VIEWPORTS:
            vd = p['viewports'].get(vp_name, {})
            ovf = vd.get('has_horizontal_overflow', False)
            cls = vd.get('cls', 0) or 0
            touch = len(vd.get('touch_targets_under_44px', []))
            axe = len(vd.get('axe_violations', []) or [])
            err = vd.get('error')
            errors = vd.get('console_errors', [])
            page_errors = vd.get('page_errors', [])

            has_issues = ovf or cls > 0.1 or touch > 0 or err or errors or page_errors
            cls_class = 'has-issues' if has_issues else ''
            out.append(f'<div class="vp {cls_class}">')
            out.append(f'<div class="head"><span>{vp_name}</span><span class="muted">{vd.get("load_ms","-")}ms</span></div>')

            badges = []
            if ovf: badges.append('<span class="badge bad">overflow</span>')
            if cls > 0.1: badges.append(f'<span class="badge bad">CLS {cls:.2f}</span>')
            elif cls > 0.05: badges.append(f'<span class="badge warn">CLS {cls:.2f}</span>')
            if touch > 0: badges.append(f'<span class="badge warn">{touch} touch&lt;44</span>')
            if axe > 0: badges.append(f'<span class="badge warn">{axe} a11y</span>')
            if errors: badges.append(f'<span class="badge bad">{len(errors)} console</span>')
            if page_errors: badges.append(f'<span class="badge bad">{len(page_errors)} JS err</span>')
            if not badges: badges.append('<span class="badge good">clean</span>')
            out.append(f'<div class="badges">{"".join(badges)}</div>')

            if vd.get('screenshot'):
                out.append(f'<img src="{vd["screenshot"]}" loading="lazy" onclick="lb(this.src)" alt="{vp_name}">')
            elif err:
                out.append(f'<div style="padding:24px;text-align:center;color:var(--bad)">ERROR: {html.escape(err)}</div>')
            out.append('</div>')
        out.append('</div></div>')

    out.append('''
<div class="lightbox" id="lb" onclick="this.classList.remove('active')"><img id="lbimg" src=""></div>
<script>
function lb(src) {
  const el = document.getElementById('lb');
  document.getElementById('lbimg').src = src;
  el.classList.add('active');
}
</script>
</body></html>''')
    return '\n'.join(out)


def main():
    pages = load_pages()
    if not pages:
        print("No data found. Run scripts/responsive-audit.py first.")
        return 1
    clusters = cluster_issues(pages)
    stats = aggregate_stats(pages)
    html_out = generate_html(pages, clusters, stats)
    REPORT.write_text(html_out, encoding='utf-8')
    print(f"✓ Report: {REPORT.relative_to(REPO_ROOT)}")
    print(f"  Pages: {stats['total_pages']}, Issue clusters: {len(clusters)}")
    print(f"  Overflow: {len(stats['pages_with_overflow'])}, CLS: {len(stats['pages_with_cls_issues'])}, "
          f"Touch: {len(stats['pages_with_touch_issues'])}, Console: {len(stats['pages_with_console_errors'])}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
