#!/usr/bin/env python3
"""Apply Gemini grammar/translation fixes from JSON review files.

SAFE MODE: only applies fixes when:
  - severity is Critical OR (High + confidence=High)
  - `current` substring is unique in target file (no ambiguity)
  - `current` substring not in user-confirmed brand terms (e.g., ქოფირაითერი)
  - non-empty current AND fix

For ka files: targets /command-center/<page>
For en files: targets /command-center/en/<page>

Outputs: report of what's applied + what's deferred (review list).
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIT = ROOT / "audit" / "prelaunch-2026-05-12"

# User-confirmed brand terms — DO NOT auto-replace
BRAND_TERMS = {
    "ქოფირაითერი",
    "ქოფირაითინგი",
    "ქოფირაითერმა",
    "ქოფირაითერისთვის",
    "ქოფირაითერი:",
    "ქოფირაითერი.",
}


def is_brand_term(s: str) -> bool:
    s = s.strip()
    for bt in BRAND_TERMS:
        if bt in s:
            return True
    return False


def process_lang(lang: str, dry_run: bool) -> dict:
    pattern = f"1{1 if lang == 'ka' else 2}_{lang}_*.json"
    summary = {"applied": [], "deferred": [], "skipped": [], "ambiguous": []}

    for f in sorted(AUDIT.glob(pattern)):
        stem = f.stem.replace(f"1{1 if lang == 'ka' else 2}_{lang}_", "")
        # Page mapping: ka files map to root, en files map to en/
        page_rel = (f"en/{stem}.html") if lang == "en" else f"{stem}.html"
        target = ROOT / page_rel
        if not target.exists():
            print(f"  ✗ {page_rel}: file not found")
            continue
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        results = data.get("result", [])
        if not results:
            continue

        html = target.read_text(encoding="utf-8")
        original = html
        applied_here = []
        for issue in results:
            sev = issue.get("severity", "")
            conf = issue.get("confidence", "")
            current = (issue.get("current") or "").strip()
            fix = (issue.get("fix") or "").strip()
            if not current or not fix or current == fix:
                continue
            if is_brand_term(current) or is_brand_term(fix):
                summary["skipped"].append(f"{page_rel}: brand term: {current}")
                continue
            # Apply only Critical (always) or High+High-confidence
            if sev == "Critical" or (sev == "High" and conf == "High"):
                count = html.count(current)
                if count == 0:
                    summary["deferred"].append(f"{page_rel}: not found in file: {current[:60]}")
                    continue
                if count > 1:
                    summary["ambiguous"].append(f"{page_rel}: {count}x in file: {current[:60]}")
                    continue
                # Apply
                html = html.replace(current, fix, 1)
                applied_here.append(f"L{issue.get('line', '?')}: {current[:40]} → {fix[:40]}")
                summary["applied"].append(f"{page_rel}: {current[:60]} → {fix[:60]}")
            else:
                summary["deferred"].append(f"{page_rel} [{sev}/{conf}]: {current[:60]}")

        if html != original:
            print(f"  ✓ {page_rel}: {len(applied_here)} fixes")
            for a in applied_here:
                print(f"    - {a}")
            if not dry_run:
                target.write_text(html, encoding="utf-8")
    return summary


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--lang", choices=["ka", "en"], required=True)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()
    if not (args.dry_run or args.apply):
        sys.exit("Specify --dry-run or --apply")

    print(f"=== Applying Gemini {args.lang} fixes ({'DRY-RUN' if args.dry_run else 'APPLY'}) ===")
    print(f"Skipping brand terms: {sorted(BRAND_TERMS)[:3]}…")
    print()
    summary = process_lang(args.lang, args.dry_run)
    print()
    print("--- Summary ---")
    print(f"  Applied: {len(summary['applied'])}")
    print(f"  Deferred (Med/Low or not High-confidence): {len(summary['deferred'])}")
    print(f"  Skipped (brand terms): {len(summary['skipped'])}")
    print(f"  Ambiguous (>1 match in file): {len(summary['ambiguous'])}")

    # Write deferred report
    report = AUDIT / f"1{1 if args.lang == 'ka' else 2}_{args.lang}_deferred_review.md"
    lines = [f"# Stage 1{1 if args.lang == 'ka' else 2}: {args.lang.upper()} Issues — Deferred for Manual Review", ""]
    lines.append("**Generated**: 2026-05-12 (auto-fix pass)")
    lines.append("")
    if summary["applied"]:
        lines.append(f"## Auto-Applied ({len(summary['applied'])})")
        for a in summary["applied"]:
            lines.append(f"- {a}")
        lines.append("")
    if summary["skipped"]:
        lines.append(f"## Skipped (brand terms, kept user spelling) ({len(summary['skipped'])})")
        for a in summary["skipped"]:
            lines.append(f"- {a}")
        lines.append("")
    if summary["ambiguous"]:
        lines.append(f"## Ambiguous (substring appears 2+ times — needs disambiguation) ({len(summary['ambiguous'])})")
        for a in summary["ambiguous"]:
            lines.append(f"- {a}")
        lines.append("")
    if summary["deferred"]:
        lines.append(f"## Deferred to manual review (Medium/Low severity OR confidence != High) ({len(summary['deferred'])})")
        for a in summary["deferred"]:
            lines.append(f"- {a}")
        lines.append("")
    report.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Wrote {report}")


if __name__ == "__main__":
    main()
