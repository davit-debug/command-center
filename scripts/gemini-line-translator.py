#!/usr/bin/env python3
"""Line-by-line Gemini translator for stubborn Georgian leftovers.

Unlike gemini-translate-page.py which uses str.replace (can fail on
whitespace/escape mismatches), this script:
1. Identifies each line with Georgian text
2. Sends ONE line at a time to Gemini
3. Replaces the line by index (not str.replace)

Slower but more robust for edge cases like FAQ Q&A JS objects.

Usage:
  python3 scripts/gemini-line-translator.py --page industries/financial-services.html
  python3 scripts/gemini-line-translator.py --all
"""
import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEY_PATH = "/Users/imac/SEO/.gemini-key"
MODEL = "gemini-2.5-pro"
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"

KA_RE = re.compile(r'[Ⴀ-ჿ]')


def load_key():
    with open(KEY_PATH) as f:
        return f.read().strip()


def has_georgian(line):
    stripped = re.sub(r'data-ka="[^"]*"', "", line)
    return bool(KA_RE.search(stripped))


def translate_one_line(line, key):
    """Send a single line to Gemini, return translated line."""
    prompt = f"""Translate the Georgian text in this HTML/JS line to English. Output ONLY the translated line, preserving:
- All HTML tags, classes, IDs, attributes EXACTLY
- All JavaScript syntax (object literals, quotes, commas)
- Brand names (Google, ChatGPT, 10xSEO, NerdWallet, etc.)
- HTML entities (&amp;, &copy;, etc.)
- Indentation and whitespace
- Unicode escape sequences in cat: values — convert them to plain English category names

Return as JSON: {{"translated": "<full translated line>"}}

Input line:
{line}

JSON output only:"""

    url = ENDPOINT.format(model=MODEL, key=key)
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 8000,
            "responseMimeType": "application/json",
        },
    }).encode("utf-8")

    req = urllib.request.Request(
        url, data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        print(f"  ERROR: {e}", file=sys.stderr)
        return None

    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.MULTILINE)
        result = json.loads(text)
        return result.get("translated", "")
    except Exception as e:
        print(f"  PARSE ERROR: {e}", file=sys.stderr)
        return None


def process_file(file_path, dry_run=False):
    with open(file_path, encoding="utf-8") as f:
        lines = f.readlines()

    ka_indices = [i for i, line in enumerate(lines) if has_georgian(line)]
    if not ka_indices:
        print(f"  No Georgian — skipped")
        return

    print(f"  {len(ka_indices)} lines to translate")
    key = load_key()
    translated_count = 0

    for idx in ka_indices:
        original = lines[idx]
        translation = translate_one_line(original, key)
        if translation is None:
            continue
        # Preserve the original trailing newline if present
        if original.endswith("\n") and not translation.endswith("\n"):
            translation += "\n"
        if not has_georgian(translation):
            lines[idx] = translation
            translated_count += 1
            print(f"  ✓ L{idx+1}")
        else:
            print(f"  ✗ L{idx+1} — Gemini still returned Georgian")

    print(f"  Translated: {translated_count}/{len(ka_indices)}")

    if dry_run:
        print(f"  DRY-RUN — no file written")
        return

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"  ✓ Wrote {file_path}")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--page", help="Page relative path under /en/")
    p.add_argument("--all", action="store_true", help="Process all /en/ pages")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    if args.all:
        en_root = ROOT / "en"
        for page in sorted(en_root.rglob("*.html")):
            print(f"\n=== {page.relative_to(en_root)} ===")
            process_file(page, dry_run=args.dry_run)
    elif args.page:
        full = ROOT / "en" / args.page
        print(f"\n=== {args.page} ===")
        process_file(full, dry_run=args.dry_run)
    else:
        sys.exit("Specify --page or --all")


if __name__ == "__main__":
    sys.exit(main())
