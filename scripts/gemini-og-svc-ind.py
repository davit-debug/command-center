#!/usr/bin/env python3
"""Generate 6 Gemini variants for remaining 4 services + 4 industries (48 total)."""
import json, time, urllib.request
from pathlib import Path

ROOT = Path("/Users/imac/SEO/command-center")
API_KEY = Path("/Users/imac/SEO/.gemini-key").read_text().strip()
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={API_KEY}"

PAGES = [
    # Services not picked yet
    {"slug":"seo-consultation",  "kind":"service", "name_ka":"SEO კონსულტაცია 1:1",  "context":"1-on-1 60-წუთიანი სტრატეგიული სესია გადაწყვეტილების მიმღებებთან. სრული აუდიტი + action plan + Loom ჩანაწერი. ერთჯერადი წვდომა, სანამ გრძელვადიან თანამშრომლობას დაიწყებთ."},
    {"slug":"seo-copywriting",   "kind":"service", "name_ka":"SEO კოპირაიტინგი",      "context":"SEO-ოპტიმიზებული ქართული ტექსტები — landing pages, blog posts, product descriptions. E-E-A-T სიგნალები, AI-ერა-ში ხილვადობა, ბუნებრივი ენა. ჩვენი ექსპერტი copywriter-ები."},
    {"slug":"copywriting",       "kind":"service", "name_ka":"UI/UX კოპირაიტინგი",    "context":"მიკროკოპი ციფრულ პროდუქტებზე — ღილაკები, error messages, empty states, onboarding, forms. ვიზიტორი მყიდველად აქცევა ბუნდოვანი ტექსტის გამოსწორებით. SaaS-ისთვის, e-commerce-ისთვის."},
    {"slug":"seo-audit",         "kind":"service", "name_ka":"SEO აუდიტი (უფასო)",    "context":"სრული SEO ვიდეო-ანალიზი (Loom format) 72 საათში. 100+ ფაქტორი — technical + content + UX + backlink. უფასო — სანამ მუშაობას დაიწყებთ. სწრაფი პრობლემების იდენტიფიკაცია."},

    # Industries
    {"slug":"construction",      "kind":"industry","name_ka":"SEO დეველოპერებისთვის (Real Estate)", "context":"SEO სამშენებლო კომპანიებისთვის და დეველოპერებისთვის. სამიზნე keyword-ები: ბინა გასაყიდად, კოტეჯი, საცხოვრებელი კომპლექსი. ფოკუსი: ბიუჯეტიანი მყიდველი + ინვესტორი."},
    {"slug":"ecommerce",         "kind":"industry","name_ka":"SEO E-commerce ბიზნესისთვის",       "context":"SEO online მაღაზიებისთვის — Shopify, WooCommerce, Magento. პროდუქტის გვერდები, კატეგორიის გვერდები, schema markup, product feed. ფოკუსი: გაყიდვების ზრდა + traffic მაღაზიაში."},
    {"slug":"healthcare",        "kind":"industry","name_ka":"SEO სამედიცინო კლინიკებისთვის",      "context":"SEO სამედიცინო ბიზნესისთვის — კლინიკები, ექიმები, სტომატოლოგია, კოსმეტოლოგია. YMYL ნიში — E-E-A-T სიგნალები კრიტიკულია. ფოკუსი: ლოკალური ძიება + AI პასუხები."},
    {"slug":"financial-services","kind":"industry","name_ka":"SEO ფინანსური სერვისებისთვის",      "context":"SEO ბანკები, საინვესტიციო კომპანიები, ბროკერები, fintech. YMYL ნიში — ავტორიტეტი + სანდოობა აუცილებელია. რეგულაციური სიფრთხილე. ფოკუსი: B2B და B2C ნდობის შექმნა."},
]

PROMPT = """შენ ხარ ქართული SEO სააგენტოს მთავარი კოპირაიტერი (10xSEO). 6 ვარიანტი Open Graph (social share) card-ისთვის.

⚠ ფოკუსი: **სრულიად სწორი ქართული გრამატიკა და სტილისტიკა**. ბუნებრივი ენა, არა Google-translate.

ვიზუალური სტრუქტურა:
- pill: 1-3 სიტყვა UPPERCASE — კატეგორია/ბადჯი
- line1: 1-2 სიტყვა — **ყვითელი ფერი**, ცენტრალური თემა (შეიძლება keyword "SEO", "AI" ან ქართული)
- line2: 1-3 სიტყვა — **თეთრი ფერი**, value/concrete benefit (ქართულად)
- deck: 5-12 სიტყვა, ქართულად — სუბტიტრი marketing benefit-ით

გვერდი: {name_ka}
დეტალები: {context}

დააბრუნე ზუსტი JSON (raw, no markdown):
{{"variants": [
  {{"pill":"...","line1":"...","line2":"...","deck":"..."}},
  {{"pill":"...","line1":"...","line2":"...","deck":"..."}},
  {{"pill":"...","line1":"...","line2":"...","deck":"..."}},
  {{"pill":"...","line1":"...","line2":"...","deck":"..."}},
  {{"pill":"...","line1":"...","line2":"...","deck":"..."}},
  {{"pill":"...","line1":"...","line2":"...","deck":"..."}}
]}}

წესები:
- line1 + line2 ჯამში 4 სიტყვამდე (იქნება დიდი ფონტი)
- pill ქართულად UPPERCASE-ით
- 6 ვარიანტი მკვეთრად განსხვავებული tone-ით (outcome-driven, expertise-driven, urgency-driven, emotional, ROI-focused, contrarian)
- გრამატიკულად სრულიად სწორი — ნამდვილი ქართველი copywriter-ის სტილში
- მხოლოდ JSON, შესავალი ან მსჯელობა გარეშე
"""

output = {}
for p in PAGES:
    print(f"→ {p['kind']:9} · {p['slug']:22} ", end="", flush=True)
    for attempt in range(5):
        try:
            body = {"contents":[{"parts":[{"text":PROMPT.format(name_ka=p["name_ka"], context=p["context"])}]}],
                    "generationConfig":{"temperature":0.95,"responseMimeType":"application/json"}}
            req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers={"Content-Type":"application/json"})
            with urllib.request.urlopen(req, timeout=90) as resp:
                raw = json.loads(resp.read().decode())["candidates"][0]["content"]["parts"][0]["text"]
            variants = json.loads(raw)["variants"]
            output[p["slug"]] = {"kind":p["kind"], "name_ka":p["name_ka"], "variants":variants}
            print(f"✓ {len(variants)} variants")
            break
        except Exception as e:
            print(f"✗ {str(e)[:40]} → wait 6s", end=" ", flush=True)
            time.sleep(6)
    else:
        print(" → FAILED")
        output[p["slug"]] = {"kind":p["kind"], "name_ka":p["name_ka"], "error":"timeout", "variants":[]}
    time.sleep(0.5)

out_path = ROOT / "scripts" / "_gemini-og-svc-ind.json"
out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
total = sum(len(v.get("variants",[])) for v in output.values())
print(f"\nSaved: {out_path}")
print(f"Total: {total}/48 variants")
