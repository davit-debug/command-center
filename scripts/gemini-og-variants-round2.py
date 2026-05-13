#!/usr/bin/env python3
"""
Round 2: Generate 3 ADDITIONAL Gemini variants per KA service (totaling 6 per service).
Focus: better Georgian grammar + different from round 1.
"""
import json, time
import urllib.request
from pathlib import Path

ROOT = Path("/Users/imac/SEO/command-center")
API_KEY = Path("/Users/imac/SEO/.gemini-key").read_text().strip()
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={API_KEY}"

# Load existing round 1 variants
existing = json.loads((ROOT/"scripts/_gemini-og-suggestions.json").read_text(encoding="utf-8"))

SERVICES = [
    {"slug":"seo-management",   "name_ka":"SEO მენეჯმენტი (ყოველთვიური)",   "context":"სრული SEO გუნდი თქვენი პროდუქტისთვის — ტექნიკური ოპტიმიზაცია, კონტენტი, ბექლინქი, AI/GEO ხილვადობა, ყოველთვიური ანგარიში. ფიქსირებული თვიური ფასით. B2B/SaaS-ისთვის."},
    {"slug":"seo-consultation", "name_ka":"SEO კონსულტაცია 1:1",            "context":"1-on-1 60-წუთიანი სტრატეგიული სესია გადაწყვეტილების მიმღებებთან. სრული აუდიტი + action plan + Loom video ჩანაწერი. ერთჯერადი — სანამ გრძელვადიან თანამშრომლობას დაიწყებთ."},
    {"slug":"seo-strategy",     "name_ka":"SEO სტრატეგია (12 თვის გეგმა)",  "context":"12-თვიანი დეტალური სამოქმედო გეგმა — keyword research, keyword mapping, content plan, technical roadmap, backlink strategy. გადასცემთ შენი in-house გუნდს ან აგებთ ჩვენთან ერთად."},
    {"slug":"seo-copywriting",  "name_ka":"SEO კოპირაიტინგი",               "context":"SEO-ოპტიმიზებული ქართული ტექსტები — landing pages, blog posts, product descriptions. E-E-A-T სიგნალები, AI-ერა-ში ხილვადობა, ბუნებრივი ენა."},
    {"slug":"copywriting",      "name_ka":"UI/UX კოპირაიტინგი (Premium)",   "context":"მიკროკოპი ციფრულ პროდუქტებზე — ღილაკები, error messages, empty states, onboarding, forms. ვიზიტორი მყიდველად აქცევა ბუნდოვანი ტექსტის გამოსწორებით."},
    {"slug":"cro",              "name_ka":"კონვერსიის ოპტიმიზაცია (CRO)",    "context":"A/B test, heatmap, funnel analysis, UX research. იმავე ტრაფიკიდან მეტი მომხმარებელი. ვისაც ვიზიტი აქვს, მაგრამ კონვერსია არ ხდება."},
    {"slug":"google-ads",       "name_ka":"Google Ads მენეჯმენტი",           "context":"სრული Google Ads მართვა — Search, Display, Performance Max, Shopping. CPC ოპტიმიზაცია, conversion tracking, ROI ფოკუსი. სწრაფი შედეგი + ბრენდის ცნობადობა."},
    {"slug":"ai-seo",           "name_ka":"AI SEO (GEO/AEO)",               "context":"AI ძიების ეპოქის ოპტიმიზაცია — იყავი ციტირებული ChatGPT-ში, Perplexity-ში, Gemini-ში, Google AI Overviews-ში. LLM-friendly content, schema, brand authority."},
    {"slug":"seo-course",       "name_ka":"SEO კურსი (12 პრაქტიკული სესია)","context":"ნოლიდან advanced-მდე. 12 პრაქტიკული გაკვეთილი + workshops + real-project hands-on + სერთიფიკატი. მარკეტერი, ბიზნეს-მფლობელი, freelancer-ისთვის."},
    {"slug":"seo-audit",        "name_ka":"SEO აუდიტი (72 საათში)",          "context":"სრული SEO ვიდეო-ანალიზი (Loom format) 72 საათში — 100+ ფაქტორი, technical + content + UX + backlink. უფასო. სანამ მუშაობას დაიწყებთ."},
]

PROMPT = """შენ ხარ ქართული SEO სააგენტოს მთავარი კოპირაიტერი (10xSEO). 3 ვარიანტი Open Graph (social share) card-ისთვის.

⚠ ფოკუსი: **სრულიად სწორი ქართული გრამატიკა და სტილისტიკა**. არ შეიქმნა strange grammatical constructions. ბუნებრივი ქართული.

ვიზუალური სტრუქტურა (ფიქსირებული):
- pill: 1-3 სიტყვა UPPERCASE — კატეგორია/ბადჯი (ქართულად)
- line1: 1-2 სიტყვა — **ყვითელი ფერი**, ცენტრალური თემა (შეიძლება მთავარი keyword "SEO", "AI", "CRO" ან ქართული)
- line2: 1-3 სიტყვა — **თეთრი ფერი**, value/concrete benefit (ქართულად)
- deck: 5-12 სიტყვა, ქართულად — სუბტიტრი, marketing benefit

სერვისი: {name_ka}
დეტალები: {context}

⚠ უკვე გვაქვს 3 ვარიანტი ამ სერვისზე (ქვემოთ). შენ უნდა შექმნა **სხვა 3 ვარიანტი**, რომელიც განსხვავდება მათგან tone-ით, structure-ით ან angle-ით.

გვერდი წინა ვარიანტები:
{previous}

დააბრუნე ზუსტი JSON (raw, no markdown):
{{"variants": [{{"pill":"...","line1":"...","line2":"...","deck":"..."}}, ...]}}

წესები:
- line1 + line2 ჯამში 4 სიტყვამდე (იქნება დიდი ფონტი)
- pill UPPERCASE-ით (მაგ. "სერვისი", "უფასო", "1-ON-1")
- 3 ვარიანტი მკვეთრად განსხვავებული tone (მაგ. outcome-driven, expertise-driven, urgency-driven)
- გრამატიკულად სრულიად სწორი — ნამდვილი ქართველი copywriter-ის სტილში
- ბუნებრივი ენა, არა "google-translate" სტილი
- აქცენტი value/benefit-ზე
- მხოლოდ JSON, შესავალი ან მსჯელობა გარეშე
"""

for svc in SERVICES:
    slug = svc["slug"]
    prev = existing.get(slug, {}).get("variants", [])
    prev_text = json.dumps(prev, ensure_ascii=False, indent=2)
    print(f"→ {slug:25} ", end="", flush=True)
    for attempt in range(3):
        try:
            body = {"contents":[{"parts":[{"text":PROMPT.format(name_ka=svc["name_ka"], context=svc["context"], previous=prev_text)}]}],
                    "generationConfig":{"temperature":0.95,"responseMimeType":"application/json"}}
            req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers={"Content-Type":"application/json"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read().decode())
            raw = result["candidates"][0]["content"]["parts"][0]["text"]
            new_variants = json.loads(raw)["variants"]
            # Append to existing
            all_v = prev + new_variants
            existing[slug] = {"name_ka": svc["name_ka"], "variants": all_v}
            print(f"✓ +{len(new_variants)} (total {len(all_v)})")
            break
        except Exception as e:
            err_str = str(e)[:60]
            print(f"✗ {err_str} → retry in 5s", end=" ", flush=True)
            time.sleep(5)
    else:
        print(" → FAILED")
    time.sleep(0.5)  # small gap between requests

(ROOT/"scripts/_gemini-og-suggestions.json").write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
total = sum(len(v.get("variants",[])) for v in existing.values())
print(f"\nTotal variants: {total} (target 60: 10 svc × 6)")
