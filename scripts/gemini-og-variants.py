#!/usr/bin/env python3
"""
Use Gemini API to generate 3 OG card text variants for each of 10 KA service pages.
Outputs JSON for a picker UI.

Output structure per variant:
  - pill: small uppercase pill (1-3 words, Georgian)
  - line1: big yellow heading word (1-2 words, Georgian or English short term like "SEO")
  - line2: big white heading word (1-2 words, Georgian)
  - deck: small subtitle (5-12 words, Georgian)
"""
import json, re, sys
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path("/Users/imac/SEO/command-center")
API_KEY = Path("/Users/imac/SEO/.gemini-key").read_text().strip()
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={API_KEY}"

# Service page metadata
SERVICES = [
    {"slug":"seo-management",   "name_ka":"SEO მენეჯმენტი",        "context":"ყოველთვიური SEO სრული მომსახურება — ტექნიკური SEO, კონტენტი, ბექლინქი, AI/GEO, ანგარიში. სამიზნე: B2B/SaaS კომპანიები რომელთაც გრძელვადიანი ორგანული ზრდა სურთ."},
    {"slug":"seo-consultation", "name_ka":"SEO კონსულტაცია",       "context":"1-on-1 60-წუთიანი სტრატეგიული სესია. სრული აუდიტი + action plan + Loom video. სამიზნე: მენეჯერები ან მფლობელები, რომელთაც ერთჯერადი ექსპერტული მიმოხილვა სჭირდებათ."},
    {"slug":"seo-strategy",     "name_ka":"SEO სტრატეგია",         "context":"12-თვიანი SEO გეგმა — keyword research, keyword mapping, content plan, technical roadmap, backlink strategy. სამიზნე: კომპანიები რომელთაც აქვთ შიდა გუნდი და სჭირდებათ მკაცრი strategic direction."},
    {"slug":"seo-copywriting",  "name_ka":"SEO კოპირაიტინგი",      "context":"SEO-ოპტიმიზებული ტექსტები — landing page, blog post, product description. E-E-A-T-ით ჩარჩოს, AI-მზადებული. სამიზნე: brand, რომელსაც სჭირდება მაღალი ხარისხის ქართული კონტენტი."},
    {"slug":"copywriting",      "name_ka":"UI/UX კოპირაიტინგი",    "context":"მიკროკოპი — ღილაკები, error messages, empty states, onboarding, forms. ნუ ვკარგავთ კლიენტებს ბუნდოვანი ინტერფეისის გამო. სამიზნე: product team, SaaS, e-commerce."},
    {"slug":"cro",              "name_ka":"კონვერსიის ოპტიმიზაცია","context":"CRO — A/B test, heatmap, funnel analysis, UX research. მეტი მომხმარებელი იმავე ტრაფიკიდან. სამიზნე: ვისაც ტრაფიკი აქვს, მაგრამ კონვერსია დაბალია."},
    {"slug":"google-ads",       "name_ka":"Google Ads",             "context":"Google Ads management — Search, Display, Performance Max, Shopping. CPC ოპტიმიზაცია, conversion tracking. სამიზნე: კომპანიები რომელთაც სწრაფი შედეგი სჭირდებათ + ბრენდის ცნობადობა."},
    {"slug":"ai-seo",           "name_ka":"AI SEO / GEO / AEO",     "context":"AI search ოპტიმიზაცია — იყავი ხილული ChatGPT-ში, Perplexity-ში, Gemini-ში, AI Overviews-ში. GEO + AEO + LLM-friendly content. სამიზნე: ცარიელი early-adopter ბრენდები."},
    {"slug":"seo-course",       "name_ka":"SEO კურსი",              "context":"12-სესიური პრაქტიკული SEO კურსი. ნოლიდან advanced-მდე. Hands-on workshops, real-project work, certificate. სამიზნე: მარკეტერი, ბიზნეს-მფლობელი, ან freelancer."},
    {"slug":"seo-audit",        "name_ka":"SEO აუდიტი",             "context":"სრული SEO აუდიტი 72 საათში — Loom video, 100+ ფაქტორი. უფასო. სამიზნე: ბრენდები რომელთაც სურთ პრობლემების სწრაფი იდენტიფიკაცია მუშაობის დაწყებამდე."},
]

PROMPT_TEMPLATE = """შენ ხარ ქართული SEO სააგენტოს მთავარი კოპირაიტერი (10xSEO). შენი ამოცანაა შექმნა Open Graph (Facebook share card) ვიზუალისთვის 3 განსხვავებული ტექსტური ვარიანტი ერთი სერვისის გვერდისთვის.

ვიზუალის სტრუქტურა:
- ზედა pill (1-3 სიტყვა, uppercase) — როგორც კატეგორია/ბადჯი
- ცენტრში 2 ხაზის headline:
  - line1: 1-2 სიტყვა, ყვითელი ფერი, ხშირად მთავარი keyword (მაგ. "SEO", "AI", "CRO")
  - line2: 1-3 სიტყვა, თეთრი ფერი, კონკრეტული value (მაგ. "მენეჯმენტი", "სტრატეგია")
- ქვემოთ deck (5-12 სიტყვა) — სუბსტიტრი benefit/value props-ით

სერვისი: {name_ka}
დეტალები: {context}

დააბრუნე ზუსტად 3 განსხვავებული ვარიანტი JSON ფორმატით (No markdown wrapping, just raw JSON):
{{
  "variants": [
    {{"pill": "...", "line1": "...", "line2": "...", "deck": "..."}},
    {{"pill": "...", "line1": "...", "line2": "...", "deck": "..."}},
    {{"pill": "...", "line1": "...", "line2": "...", "deck": "..."}}
  ]
}}

წესები:
- line1 + line2 ერთად 4 სიტყვამდე ჯამში (იქნება დიდი ფონტი — 130-160px)
- line1-ში სასურველია მთავარი keyword/brand-term (მაგ. "SEO", "AI", "CRO" - ლათინური ან ქართული)
- line2 ქართულად
- deck-ი ქართულად, marketing-style, შემაჯამებელი benefit
- pill ქართულად UPPERCASE-ით (მაგ. "სერვისი", "უფასო", "1-ON-1")
- 3-ვე ვარიანტი უნდა იყოს მკვეთრად განსხვავებული tone-ით (მაგ. ერთი outcome-driven, ერთი feature-driven, ერთი emotional-driven)
- დააბრუნე მხოლოდ JSON, შესავალი ან მსჯელობა გარეშე
"""

def call_gemini(prompt):
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.9, "responseMimeType": "application/json"},
    }
    req = urllib.request.Request(
        GEMINI_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    return result["candidates"][0]["content"]["parts"][0]["text"]

def main():
    output = {}
    for svc in SERVICES:
        print(f"→ {svc['slug']:25} ", end="", flush=True)
        prompt = PROMPT_TEMPLATE.format(**svc)
        try:
            raw = call_gemini(prompt)
            data = json.loads(raw)
            output[svc["slug"]] = {"name_ka": svc["name_ka"], "variants": data["variants"]}
            print(f"✓ {len(data['variants'])} variants")
        except Exception as e:
            print(f"✗ ERROR: {e}")
            output[svc["slug"]] = {"name_ka": svc["name_ka"], "error": str(e), "variants": []}

    out_path = ROOT / "scripts" / "_gemini-og-suggestions.json"
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSaved: {out_path}")
    total = sum(len(v.get("variants", [])) for v in output.values())
    print(f"Total variants generated: {total}")

if __name__ == "__main__":
    main()
