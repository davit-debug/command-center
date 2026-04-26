# Industries Landing Pages — CHANGES

## 2026-04-26 — Construction A/B Variants (V2-V5 + Mix-A/B/C + SUPER full-stack)

Eight more A/B-test variants of `construction.html` shipped on top of V1+V6. Total 10 variants now live for testing. All `noindex,nofollow` until A/B winner picked. Canonical → `construction.html`. Anonymized references throughout.

### Files added (8)
| File | Variant | Audience | Lines |
|---|---|---|---|
| `construction-mid-market-quiz.html` | V2 Mid-Market Quiz | Mid-tier dev (1 project) | 462 |
| `construction-roi-calculator.html` | V3 ROI Calculator | Investor-led CFO buyers | 391 |
| `construction-project-architecture.html` | V4 Multi-Project Architecture | 5+ project CMOs | 452 |
| `construction-vsl-cold-traffic.html` | V5 VSL Cold Traffic | Cold paid traffic | 526 |
| `construction-pyramid-hero.html` | Mix-A Pyramid Hero | High-intent referral (brand-book minimal) | 253 |
| `construction-editorial.html` | Mix-B Editorial Story | Reading-oriented premium decision-makers | 239 |
| `construction-manifesto.html` | Mix-C Manifesto | Confident anti-portal buyers | 254 |
| `construction-full-stack.html` | SUPER Full-Stack Growth Partner | Devs wanting one agency for everything | 484 |

### V2 Mid-Market Quiz
- 4-step inline quiz: project type → # active projects → current SEO budget → primary market
- Personalized strategy card generated from answers (5 templates)
- Auto-highlighted recommended pricing tier
- WhatsApp deep-link with quiz answers pre-filled in message body
- Current purple/teal palette + glass-morphism + progress bar

### V3 ROI Calculator
- 4-slider interactive calculator: monthly portal spend (GEL 500-15k), avg apartment price ($30K-€2.5M), foreign investor share (0-80%), conversion %
- Real-time output: lead cost, 12-month portal cost, lost foreign-investor market in $, SEO break-even month
- Auto-recommended package based on inputs
- Email-gated PDF projection + Calendly final CTA
- AI Blue accent color for calculator UI

### V4 Multi-Project Architecture
- Blueprint dark + JetBrains Mono technical aesthetic
- Hero preview + full SVG architecture diagram (15 project nodes + 5 hubs + 4-language layer)
- 3-layer explainer (Brand SEO / Project SEO / Local Hubs)
- Per-project playbook (8 steps mono-style)
- Multi-project Live Dashboard mock (7 projects with bars)
- Targets developers with 5+ active projects (Next Property tier)

### V5 VSL Cold Traffic
- Full Hormozi 10-beat structure (Hook → Agitate → Enemy → Mechanism → Proof → Stack → Price → Guarantee → Urgency → CTA)
- 90s VSL placeholder (poster + play button — actual video pending)
- Same gold CTA repeated 9 times throughout
- Live "slots remaining" pills (4 taken, 2 open)
- 90-day Top 5 guarantee badge ("or next month free")
- Skip-pill appears 30s after page load
- Aggressive yellow + dark contrast, single-column flow

### Mix-A Pyramid Hero (V1+V6 mix)
- Most minimal of all variants — full-viewport hero with animated gold pyramid (FB/IG cover image inspired)
- "მზად ხარ იყო პირველი?" tagline as h1
- Single proof point (+68% / -45% / 6 months)
- 4 service icons (no descriptions — bare minimum)
- Pricing table (5 tiers compact)
- Final CTA with second pyramid
- Spotlight gradient + pyramid glow animation

### Mix-B Editorial Story (V1+V6 mix)
- Magazine-style storytelling with chapter numbering (Lora serif italic)
- Alternating navy/cream sections for visual rhythm
- Drop-cap on first essay paragraph
- Pull-quotes between chapters
- 4 chapters: The Problem / How We Think / Single Case Study / 4 Services
- KA + EN toggle ready
- Reading-oriented for premium decision-makers

### Mix-C Manifesto (V1+V6 mix)
- Bold declarative statements with massive Inter Black typography
- "We Believe / We Don't / We Promise" three-act structure
- Strike-through for what they DON'T do (red strike-color)
- Section dividers with dashed yellow pattern
- Confidence-driven anti-portal positioning
- 6 sections, all KA, no images other than logos

### SUPER Full-Stack Growth Partner
- Bundles 11 services in one offering: SEO + **AI SEO/GEO** + CRO + Google Ads + UI/UX + Copywriting + Branding + Email + Social + Analytics + Video
- Hero anchored on "stop juggling 5 agencies" pain
- "Vendor Chaos" section showing 11 separate vendors at GEL 22,200/mo
- 11-service grid with color-coded badges per service
- 4-step "How it works" timeline
- 3 pricing tiers: GROWTH (15k GEL), SCALE (25k GEL — featured), DOMINATE (45k+ GEL)
- 8-Q FAQ specific to bundling concerns
- Targets developers wanting ONE growth partner instead of vendor management

### Why these variants together?
The 10 total variants (V1-V6 + Mix-A/B/C + SUPER) cover orthogonal dimensions:
- **Audience scale**: V2 (1 project) → V1 (premium multi) → V4 (5+ projects) → SUPER (full-stack)
- **Conversion mechanic**: V6 (clarity) → V2 (quiz) → V3 (calculator) → V5 (VSL) → SUPER (consultative)
- **Visual identity**: monochrome (V6) → brand-book yellow (V1, Mix-A/B/C, SUPER) → blueprint (V4) → multi-color (SUPER)
- **CTA strategy**: 1 CTA twice (V6) → 1 CTA × 3 (V1) → multi-tier (V2, V3) → 1 CTA × 9 (V5)

A/B test pairs to consider:
- **V1 vs V6** — info-density vs subtraction (same premium audience)
- **V3 vs V5** — calculator self-discovery vs Hormozi persuasion (cold traffic test)
- **Mix-A vs Mix-B vs Mix-C** — minimal vs editorial vs manifesto (brand-book aesthetic test)
- **SUPER vs V1** — full-stack bundle vs SEO-only at premium tier (cross-sell test)

---

## 2026-04-26 — Construction A/B Variants (V1 + V6) — initial pair

Two A/B-test variants of `construction.html` shipped, targeting **large-project Georgian developers** (Chronometri / Coordinate / Central MG / Next Property tier). Both files are `noindex, nofollow` until A/B winner picked. Canonical points to original `construction.html` for both. See full strategy at `~/.claude/plans/users-imac-desktop-10xseo-main-docs-seo-abstract-seal.md`.

### Files added
| File | Variant | Audience | Lines |
|---|---|---|---|
| `construction-clarity.html` | V6 Clarity | High-intent referral / branded search buyers | 385 |
| `construction-premium-multi-project.html` | V1 Premium Multi-Project | Premium developers (Chronometri-tier) with foreign-investor audiences | 551 |

### V6 Clarity — design intent
- **Hypothesis:** sophisticated buyers from referrals don't need persuasion — they need confidence signals. Brutal subtraction filters tire-kickers, only serious developers convert.
- **Visual:** monochrome, `#020710` base, white type, single purple `#8B5CF6` accent reserved for the CTA only. Inter font (skip FiraGO Heavy on display sizes). No glass cards, no gradients.
- **Sections (7):** Single-sentence hero promise → single anonymized case study (resort developer +68%) → 4 services as plain icons → 4-step process as numbered list → all-5-tiers pricing table → single FAQ ("რატომ ჯერ კიდევ არ რანქავ?") → single CTA.
- **CTA strategy:** single CTA, repeated only twice (top + bottom). "დაგვიკავშირდი." Calendly popup. No WhatsApp above fold (footer only). No lead-magnet form. No exit-intent.
- **What's cut from current 13-section page:** Portal Problem comparison, 8-card service grid, 7-tab niche grid, transparency band, AI/GEO deep dive, 15-Q FAQ, 47-point PDF lead magnet, sticky mobile CTA, animated dashboard.

### V1 Premium Multi-Project — design intent
- **Hypothesis:** premium developers with 2-10 active projects respond to brand-book aesthetic that signals premium positioning + multi-language investor capability. CTA = single Calendly, no quizzes/calculators (these buyers want a real conversation).
- **Visual:** brand-book "მზად ხარ იყო პირველი?" palette — Yellow `#FFC000` accents on Navy `#0F172A` base, gold pyramid mark in hero corner, Dachi the Lynx font for headings, off-white "cream" section break for the SEO architecture diagram (visual contrast against all-dark monotony).
- **Sections (10):** Hero with 4-language pill dashboard mock → trust bar with hex logos + investor stats (15+ years, 600+ projects, 1000+ investors, 95% retention — anonymized) → 5 service cards (Project SEO / Brand SEO / Off-Plan / Multi-language Investor / Schema) → SEO Architecture SVG diagram (cream section) → 3 sub-niche tabs (Residential / Mixed-Use / Commercial) → 4-phase process timeline → investor-trust signal stats → testimonial (anonymized "Premium Resort Developer") → 10-Q FAQ → final CTA.
- **NEW components vs. current page:** (a) Project Portfolio Architecture SVG diagram showing brand domain + project nodes + neighborhood hubs + 4-language layer; (b) 4-language pill system (KA/EN/RU/TR) shown in hero dashboard mock and ready for hreflang wiring; (c) cream section break for diagram (#F5F1E8); (d) gold-accent FAQ component (replaces v29 purple variant).
- **Languages declared:** KA primary, EN/RU/TR placeholders in toggle (translation pending — Phase 1 dev work doesn't block on translation).

### Reference clients — anonymization
Per user decision (2026-04-26), no client is named in prose. The hex client logo bar reuses the existing public logo images (Chronometri, Coordinate, Horizon, myhome) — these are public marks already on the live site. Case study testimonial is anonymized to "Premium Resort Developer (Batumi)" / "Director" framing instead of the original "Horizon Development / გიორგი ხარაიშვილი" attribution.

### Schema preserved across variants
Both variants ship full schema: Service, Organization, BreadcrumbList. V1 also ships FAQPage schema (10 Qs, KA). V6 omits FAQPage (only 1 question — not worth schema).

### Open items not yet resolved (carry to next sprint)
- RU + TR translation copy for V1 (placeholder UI in place)
- A/B traffic split mechanism (Cloudflare or URL param)
- Promote winner to canonical `construction.html` once test concludes

---

# Healthcare Landing Page Redesign — CHANGES (prior)

## What changed and why

### SECTIONS REMOVED
| Section | Why |
|---------|-----|
| Ratings Bar (separate section) | Integrated into hero as pill badges adjacent to CTA — higher visibility |
| S8: Process (5-step timeline) | Duplicate of S8B "First 30 Days". Merged into single timeline |

### SECTIONS REWRITTEN
| Section | Change | Why |
|---------|--------|-----|
| S1: Hero | Lead with "Todua Clinic — +40% GBP ზარები 2 თვეში" instead of tagline. Dashboard → annotated traffic chart with neon callouts. Social proof pills adjacent to CTA. Secondary CTA = phone number (not Calendly duplicate). | First line = specific result → trust. Multi-CTA by intent level. |
| S3: AI Stats | Asymmetric: 70% is dominant full-width card, 52% and 77% are smaller 2-col. | Break visual monotony of 3 equal cards. Dominant stat draws eye. |
| S4: Services | 6-card grid → "Symptom → Treatment" two-column rows. Medical metaphor. | Fits vertical, scannable, unique vs competitor pages. |
| S5: Specialty Tabs | Each tab now has mini-CTA ("აუდიტი →" or case study link) and one real client/metric. Removed Pharmadepot +340% (unverifiable). | Conversion path per specialty. No unverifiable claims. |
| S9: Testimonial | Centered card → hero-sized pull quote. Larger text (text-4xl), semi-transparent bg. | High-impact social proof deserves visual weight. |
| S8B → Timeline | Merged S8 5-step process into S8B. Now 5 compact cards (Week 1 → Ongoing). | Single timeline, no duplication. |
| Pricing | Added clinic-stage headers per tier ("1 ფილიალი · ახალი კლინიკა" / "ზრდის ფაზა" / "საერთაშორისო"). Added guarantee badge. | Self-qualification by clinic stage. Risk reversal. |
| FAQ | Rewritten from 12 generic Qs to 8 focused ones (agency switching, contract, what-if-we-stop, YMYL compliance, GEO). | Objection-handling questions that clinic owners actually ask. |
| Final CTA | Changed primary CTA to "მივიღო უფასო SEO აუდიტი" (video icon). Added "ყოველგვარი ვალდებულების გარეშე" tagline. | Low-commitment CTA + risk-reversal messaging. |

### SECTIONS ADDED
| Section | What | Why |
|---------|------|-----|
| Cost of Inaction | 3 red-bordered cards: competitor AI advantage, zero-click traffic loss, rising CAC. | Fear of missing out + urgency without fake scarcity. |
| AI Visibility Check (Wedge CTA) | "Enter clinic name → get Loom video in 24h showing AI visibility". Calendly trigger. | Unique differentiator. Low-commitment lead gen. No competitor offers this. |
| Guarantee Badge | "60 დღეში პროგრესის გარეშე — ვმუშაობთ უფასოდ შედეგამდე" pill under pricing. | Risk reversal. Reduces commitment anxiety. |

### DATA FIXES
| Item | Action |
|------|--------|
| "Cost per Lead -35%" in dashboard | Removed — unverifiable |
| "Pharmadepot +340%" in pharmacy tab | Removed — unverifiable (no case study backs it) |
| Hero dashboard | Replaced with annotated traffic chart showing real growth trajectory |

### KEPT UNCHANGED
- Head (meta, schema, CSS) — no changes
- Header + mobile menu — no changes
- Hex client logos — kept (order unchanged)
- S6 Case study cards — kept (4 cards, same data)
- Footer — no changes
- Sticky mobile CTA — no changes
- Scripts (scroll reveal, count-up, Calendly) — no changes
- Color system (primary=#8B5CF6, accent=#14B8A6) — no changes

## Replication guide for other industry pages
When applying this pattern to financial-services.html, construction.html, ecommerce.html:

1. Replace hero badge with industry-specific client result
2. Replace annotated chart with relevant client's growth data
3. Adapt "Symptom → Treatment" rows to industry pain points
4. Replace specialty tabs with industry sub-verticals
5. Swap case study cards with industry-relevant clients
6. Adjust FAQ questions to industry-specific objections
7. Update AI Visibility Check copy for the vertical
8. Keep pricing structure (stage-based headers), adjust descriptions
