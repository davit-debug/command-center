# 10xSEO Offer System

Private client-specific offer pages. All pages are `noindex, nofollow` — not public.

## Offer Page Variants

### Standard Variants (V1-V9)
Static HTML pages using purple/teal/gold design system.

| File | Type | Best For |
|------|------|----------|
| `offer-v2.html` | Grand Slam Hormozi | General prospects |
| `offer-v2-diagnostic.html?client=slug` | Personalized Audit | Post-audit prospects |
| `offer-v3-story.html` | Story-Led (Todua case) | Healthcare prospects |
| `offer-v4-compare.html` | 4-Way Comparison | Skeptics comparing options |
| `offer-v5-calculator.html` | ROI Calculator | Data-driven buyers |
| `offer-v6-educational.html` | Educational (90-day plan) | First-time SEO buyers |
| `offer-v7-recommendation.html` | Single Recommendation | Warm leads |
| `offer-v8-sprint.html` | 30-Day Sprint | Quick-start budget buyers |
| `offer-v9-hybrid.html?client=slug` | Hybrid (21 sections) | High-value prospects |

### Premium Variants (Deal Room / Video / Vertical)
Terminal/grid aesthetic (`#00ff88` neon green). Targeting Dubai/UAE expansion + premium Georgian clients.

| File | Type | Best For |
|------|------|----------|
| `offer-deal-room.html?client=slug` | Deal Room + MAP | Dubai enterprise, multi-stakeholder |
| `offer-video.html?client=slug` | Video-First VSL | Founder-led sales, trust building |
| `offer-vertical.html?client=slug` | Dubai Vertical Deep-Dive | Regulated verticals (Healthcare/DHA) |

## Decision Tree: Which Variant to Use

```
Is the prospect in Dubai/UAE?
  YES → Is it a regulated industry (healthcare, finance, real estate)?
    YES → offer-vertical.html
    NO  → offer-deal-room.html
  NO  → Is this a warm lead from a call?
    YES → Do you have a video recording?
      YES → offer-video.html
      NO  → offer-v7-recommendation.html or offer-v9-hybrid.html
    NO  → Is the prospect data-driven?
      YES → offer-v5-calculator.html or offer-v2-diagnostic.html
      NO  → offer-v2.html (Grand Slam)
```

## Adding a New Client

### Standard Variants (30 min workflow)
1. Open `offer/clients.json`
2. Copy the `demo` entry, rename to client slug (e.g., `acme-corp`)
3. Fill in: company name, domain, contact info, audit findings
4. Use Ahrefs to extract: DR, organic keywords, traffic, competitors
5. Test: `localhost:8080/offer-v9-hybrid.html?client=acme-corp`

### Premium Variants (45 min workflow)
1. Open `offer/clients-premium.json`
2. Copy the closest example client (e.g., `temu-example` for ecommerce)
3. Fill in all fields:
   - Identity: company name, domain, industry, geo targets, languages
   - Current KPIs: traffic, leads, MRR, conversion rate
   - Audit findings: 10-20 items with severity, issue, impact, fix, effort
   - Quick wins: 3-5 items
   - Competitor gap: 2-3 competitors with Ahrefs data
   - Opportunity model: 3 scenarios (conservative/base/aggressive)
   - Team assigned
   - Variant-specific data (dealRoom/video/vertical)
4. Test: `localhost:8080/offer-deal-room.html?client=your-slug`

## Data Files

| File | Purpose |
|------|---------|
| `offer/clients.json` | Standard variant client data (2 entries: demo, todua-clinic) |
| `offer/clients-premium.json` | Premium variant client data (3 entries) |
| `offer/pricing.json` | 5-tier pricing, bonuses, extras, case studies |
| `offer/shared.css` | Standard variant shared styles |
| `offer/shared.js` | Standard variant shared JS |
| `offer/premium-shared.css` | Premium variant shared styles (terminal aesthetic) |
| `offer/premium-shared.js` | Premium variant shared JS (analytics, MAP, scroll-spy) |

## Pricing Tiers (source of truth: `offer/pricing.json`)

| Tier | GEL | AED |
|------|-----|-----|
| SEO Start | 1,450 | ~1,950 |
| SEO Base | 2,500 | ~3,350 |
| SEO Growth | 3,550 | ~4,750 |
| Premium | 6,500 | ~8,700 |
| Market Leader | 12,500 | ~16,700 |

## Analytics (Future)

`offer/premium-shared.js` has a stub analytics interface ready for PostHog or Plausible:

- `trackSectionView` — which sections prospects read
- `trackCTAClick` — which CTAs get clicked
- `trackPricingInteraction` — tier views and selections
- `trackShareAction` — stakeholder forwarding
- `trackVideoProgress` — video watch completion
- `trackMAPStepToggle` — MAP engagement
- `trackExportPDF` — PDF exports

Currently logs to console. Replace with real tracking when ready.

## Local Development

```bash
cd command-center
python3 -m http.server 8080
# Open: localhost:8080/offer-deal-room.html?client=temu-example
```
