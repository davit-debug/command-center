#!/usr/bin/env python3
"""Extend translation-review.md with 5-version variants for 9 service +
4 industry pages. Same format as the priority pages section so the
dashboard generator handles it without changes.
"""
from pathlib import Path

REVIEW_PATH = Path("/Users/imac/SEO/translation-review.md")

# Each page: list of (fragment_label, [v1, v2, v3, v4, v5])
# v can be string or (text, meta) tuple
PAGES = [
    # === SEO MANAGEMENT (Done-For-You retainer) ===
    ("/en/seo-management.html", "Monthly SEO Management (Done-For-You)", [
        ("Title", [
            ("Monthly SEO Management Services | 10xSEO Tbilisi, Georgia", "58 chars · current applied"),
            ("Done-For-You SEO Management for Georgia & Tbilisi | 10xSEO", "58 chars · DFY angle"),
            ("SEO Management Service in Georgia | 10xSEO Monthly Retainer", "59 chars · retainer framing"),
            ("Full-Stack SEO Management — Rank #1 on Google & AI | 10xSEO", "59 chars · outcome-led"),
            ("Hire 10xSEO — Monthly SEO Management for Ambitious Brands", "57 chars · action verb"),
        ]),
        ("Meta description", [
            ("Done-for-you monthly SEO management. 10xSEO takes full ownership: technical SEO, content, link building, AI search optimization. Top SEO agency in Georgia.", "157 chars · current"),
            ("Outsource your SEO to 10xSEO. Monthly retainer covers technical SEO, content, link building, and AI search optimization for Tbilisi & global brands.", "149 chars · action-led"),
            ("Georgia's #1 SEO agency runs monthly SEO management for ambitious brands. Full Done-For-You package — technical, content, links, AI search. Free consult.", "156 chars · authority"),
            ("Stop juggling SEO yourself. 10xSEO's monthly management package handles everything: technical, content, links, AEO/GEO. Live dashboard + 10-min SLA.", "151 chars · pain-point"),
            ("Monthly SEO management from Tbilisi's leading agency. Done-For-You SEO with weekly reports, AI search optimization, and a guaranteed 10-min response SLA.", "156 chars · feature stack"),
        ]),
        ("H1", [
            ("Monthly SEO Management — Rank #1 on Google and AI", "current"),
            ("Done-For-You SEO Management / for Ambitious Brands", "DFY framing"),
            ("Full-Stack SEO Management / from Georgia's #1 Agency", "geo + scope"),
            ("Hire the SEO Team / That Ranks Brands #1", "trust-led"),
            ("Monthly SEO Management / Built for Compound Growth", "outcome-led"),
        ]),
        ("Hero subheading", [
            ("10xSEO's monthly SEO management is a Done-For-You service that includes technical optimization, content creation, building digital authority, and ensuring visibility on AI platforms (ChatGPT, Gemini, Perplexity).", "current — comprehensive"),
            ("One team, full SEO ownership. We handle technical fixes, content production, link building, and AEO/GEO optimization so you can focus on your business.", "value-first"),
            ("Monthly retainer for businesses that want results, not status reports. Live dashboard, weekly reviews, and a guaranteed 10-minute response window during business hours.", "service-feature"),
            ("Stop coordinating five vendors. 10xSEO's monthly SEO management consolidates technical, content, link building, and AI search into one accountable team.", "consolidation angle"),
            ("The done-for-you SEO retainer Tbilisi brands hire when they're ready to dominate Google + ChatGPT. Live reporting, white-hat methods, real ROI.", "Tbilisi + outcomes"),
        ]),
    ]),

    # === SEO CONSULTATION (1:1 calls) ===
    ("/en/seo-consultation.html", "SEO Consultation (1:1 Expert Sessions)", [
        ("Title", [
            ("SEO Consultation 1:1 — Expert Strategy Sessions | 10xSEO", "56 chars · current"),
            ("Book a 1:1 SEO Consultation in Tbilisi | 10xSEO", "47 chars · geo + book"),
            ("SEO Expert Consultation Call — 14 Years Experience | 10xSEO", "60 chars · authority"),
            ("Talk to an SEO Expert | 10xSEO Consultation in Georgia", "54 chars · action-led"),
            ("SEO Consultation with Davit Tsilosani | 10xSEO Tbilisi", "54 chars · founder personal"),
        ]),
        ("Meta description", [
            ("Get 1:1 SEO consultation from a 14-year veteran. Solve technical SEO challenges, get clear answers, and a custom action plan. Book a session with 10xSEO.", "157 chars · current"),
            ("Book a 1-hour SEO consultation with the founder of Georgia's #1 SEO agency. Specific answers to your specific problems. Written summary + video recording.", "157 chars · deliverables"),
            ("Stuck on SEO? Talk 1:1 with a 14-year veteran. Get a clear action plan, written summary, and recording in a single 60-minute session. Book now.", "146 chars · pain-point"),
            ("Expert SEO consultation for businesses in Tbilisi and worldwide. Strategy review, audit feedback, or a focused problem-solving session — 60 minutes, real expertise.", "163 chars · borderline"),
            ("One hour with a senior SEO strategist who has shipped 50+ projects. Bring your problem; leave with a concrete plan. 10xSEO consultation, Tbilisi-based.", "153 chars · concrete promise"),
        ]),
        ("H1", [
            ("One-on-One SEO Session with an Expert", "current"),
            ("1:1 SEO Consultation / with a 14-Year Veteran", "experience hook"),
            ("Talk to an SEO Expert / Get a Custom Action Plan", "outcome-led"),
            ("Book a Session / with Georgia's #1 SEO Strategist", "authority"),
            ("SEO Consultation Call / Specific Answers, Same Day", "promise"),
        ]),
        ("Hero subheading", [
            ("Book a 60-minute call with the founder of 10xSEO. Bring your problem — leave with a written summary, video recording, and a concrete next-step plan.", "concrete deliverables"),
            ("Sometimes you don't need a full SEO retainer — you need one hour with the right expert. Strategy review, audit feedback, or a single focused problem.", "scope clarity"),
            ("Direct 1:1 access to Davit Tsilosani — 14 years of SEO, 50+ projects shipped. Includes recording + written summary you can share with your team.", "founder + deliverables"),
            ("60 minutes, video recorded, with a written follow-up. The fastest way to get specific SEO answers without committing to a multi-month engagement.", "no-commitment"),
            ("Pick the format that fits: pre-built session (₾250+VAT) or scoped strategy session (priced by complexity). All sessions include recording + written summary.", "pricing transparency"),
        ]),
    ]),

    # === SEO STRATEGY ===
    ("/en/seo-strategy.html", "SEO Strategy (Roadmap)", [
        ("Title", [
            ("SEO Strategy — Results-Driven Action Plan | 10xSEO Tbilisi", "59 chars · current"),
            ("SEO Strategy & Roadmap for Tbilisi & Global Brands | 10xSEO", "59 chars · international"),
            ("Custom SEO Strategy + Roadmap | 10xSEO Georgia", "47 chars · concise"),
            ("Professional SEO Strategy in Georgia | 12-Month Roadmap", "55 chars · timeline"),
            ("Get an SEO Roadmap from Tbilisi's #1 Agency | 10xSEO", "53 chars · action-led"),
        ]),
        ("Meta description", [
            ("Get a complete SEO strategy for your project: in-depth analysis, competitor research, market study, and step-by-step optimization roadmap from 10xSEO.", "153 chars · current"),
            ("Custom SEO strategy for your business: keyword research, competitor analysis, technical audit, content plan, and a 12-month roadmap. Tbilisi-based 10xSEO.", "158 chars · deliverables"),
            ("Stop guessing what your SEO needs. 10xSEO delivers a professional SEO strategy + roadmap based on real keyword data, competitor analysis, and your goals.", "157 chars · pain-point"),
            ("Georgia's #1 SEO agency builds custom SEO roadmaps for ambitious brands. Audit, keyword research, prioritization, content plan, and 6/12-month milestones.", "157 chars · authority"),
            ("Your SEO strategy is the difference between random work and predictable growth. 10xSEO maps the next 6–12 months with milestones, KPIs, and ownership.", "154 chars · positioning"),
        ]),
        ("H1", [
            ("SEO Strategy - A Growth Roadmap for Your Business", "current"),
            ("Custom SEO Strategy / Built Around Your Goals", "personalized"),
            ("Your SEO Roadmap / from Audit to #1", "journey-led"),
            ("SEO Strategy / 12 Months of Predictable Growth", "timeline"),
            ("Stop Guessing — Get a Plan / Built on Real SEO Data", "pain-point"),
        ]),
        ("Hero subheading", [
            ("Get a complete action plan : comprehensive analysis, market research, and a step-by-step optimization plan.", "current"),
            ("A custom SEO strategy based on your goals, your market, and your competitors. Keyword research, technical audit, content plan, and prioritized 12-month roadmap.", "deliverables"),
            ("Random SEO work produces random results. We build the strategy first — audit, keyword research, competitor analysis, prioritization — so every hour of execution compounds.", "philosophy"),
            ("12 months of SEO mapped out with milestones, owners, and KPIs. Delivered as a working document your team can execute against, not a static PDF.", "execution-friendly"),
            ("From keyword discovery to a phased rollout plan, your SEO strategy maps the entire path from where you are to #1 on Google + AI search.", "scope"),
        ]),
    ]),

    # === SEO COPYWRITING ===
    ("/en/seo-copywriting.html", "SEO Copywriting", [
        ("Title", [
            ("SEO Copywriting — Content That Ranks & Sells | 10xSEO", "53 chars · current"),
            ("SEO Copywriting Service Tbilisi & Georgia | 10xSEO", "50 chars · geo"),
            ("SEO Content Writing — Ranks on Google + Converts | 10xSEO", "57 chars · dual benefit"),
            ("Hire SEO Copywriters in Georgia | 10xSEO Content Team", "53 chars · action-led"),
            ("Premium SEO Copywriting for Ambitious Brands | 10xSEO", "53 chars · premium framing"),
        ]),
        ("Meta description", [
            ("SEO copywriting for business: homepages, blogs, articles, press releases. Content that ranks on Google's first page and converts visitors into customers.", "157 chars · current"),
            ("Professional SEO copywriting in Georgian and English. Homepage content, service pages, blog articles, and press releases that rank and sell. Free quote.", "155 chars · bilingual"),
            ("10xSEO writes the SEO content top Tbilisi businesses use to win on Google. Homepages, blogs, service pages, press releases — built for ranking and conversion.", "159 chars · authority"),
            ("Need content that ranks AND converts? 10xSEO's SEO copywriters specialize in technical SEO + persuasive writing for Tbilisi and international brands.", "151 chars · differentiator"),
            ("From homepage to blog to product descriptions — SEO copywriting by 10xSEO. Researched, optimized, and rewritten until every page earns its keyword.", "150 chars · craft-focused"),
        ]),
        ("H1", [
            ("SEO Copywriting — Content That Gets You / Found on Google", "current pattern"),
            ("SEO Copy / That Ranks and Sells", "concise"),
            ("Premium SEO Copywriting / for Ambitious Brands", "premium positioning"),
            ("Content That Wins on Google / Built by 10xSEO Writers", "outcome-led"),
            ("SEO Copywriting / Bilingual, Strategic, Conversion-First", "scope"),
        ]),
        ("Hero subheading", [
            ("Content that works for both the algorithms and your sales growth.", "current short"),
            ("Every piece is researched, structured for SEO, and written to convert. Homepage copy, service pages, blogs, press releases — all built around your keywords and your audience.", "scope + craft"),
            ("From keyword research to final draft, 10xSEO's SEO copywriters produce content that ranks on Google's first page and reads like a real human wrote it — because one did.", "differentiator"),
            ("Premium SEO copywriting for Tbilisi and international brands. We don't churn out content — we write the few pieces your business actually needs to rank and convert.", "premium + selective"),
            ("Bilingual SEO copy: Georgian and English. Every piece optimized for the platform it lives on (Google, ChatGPT, social), with one round of revisions included.", "bilingual + process"),
        ]),
    ]),

    # === COPYWRITING (UI/UX premium) ===
    ("/en/copywriting.html", "UI/UX Copywriting (Premium)", [
        ("Title", [
            ("UI/UX Copywriting — Words That Drive User Behavior | 10xSEO", "61 chars · current"),
            ("Premium UI/UX Copywriting Service | 10xSEO Tbilisi", "50 chars · geo"),
            ("Product Copywriting & Microcopy in Georgia | 10xSEO", "51 chars · scope"),
            ("Conversion Copywriting for Tbilisi Brands | 10xSEO", "50 chars · outcome-led"),
            ("UI/UX Copy That Converts | 10xSEO Georgia", "41 chars · concise"),
        ]),
        ("Meta description", [
            ("Stop losing customers to unclear UI. 10xSEO's UI/UX copywriting turns visitors into buyers with words that guide every click and reduce friction.", "151 chars · current"),
            ("Premium UI/UX copywriting service. Buttons, error messages, onboarding flows, microcopy — every word engineered to reduce friction and drive conversions.", "157 chars · scope"),
            ("Bad UI copy costs you customers. 10xSEO's UI/UX copywriters audit and rewrite your interface so visitors actually finish what they came to do.", "146 chars · pain-point"),
            ("UI/UX copywriting for SaaS, e-commerce, and digital products. Built by writers who understand product, conversion, and brand voice. 14 years experience.", "157 chars · authority"),
            ("Premium interface copy for Tbilisi and global brands. Onboarding flows, error states, button copy, empty states — words that make products feel intuitive.", "157 chars · benefit"),
        ]),
        ("H1", [
            ("Copy That Drives User Action", "current"),
            ("UI/UX Copy / Built to Convert", "outcome"),
            ("Premium UI/UX Copywriting / for Digital Products", "premium + scope"),
            ("Words That Make Products / Feel Intuitive", "benefit"),
            ("Every Button, Every Flow / Engineered to Convert", "comprehensive"),
        ]),
        ("Hero subheading", [
            ("Your website speaks to clients through its text. We ensure this language is simple, consistent, polished, and precisely answers the questions your potential customers have.", "current"),
            ("From the first button label to the last error message, every word in your product is a chance to convert or lose a customer. We make sure it's always the first.", "stakes-focused"),
            ("Premium UI/UX copywriting for SaaS, e-commerce, and digital products. Onboarding flows, microcopy, empty states — engineered to reduce friction at every click.", "scope"),
            ("Most products fail at the words, not the design. 10xSEO's UI/UX copywriters audit your interface and rewrite the moments that cost you customers.", "pain + solution"),
            ("Bilingual product copywriting (English + Georgian) for ambitious teams. We turn your product into a story your users actually finish.", "bilingual + outcome"),
        ]),
    ]),

    # === CRO ===
    ("/en/cro.html", "Conversion Rate Optimization (CRO)", [
        ("Title", [
            ("Conversion Rate Optimization (CRO) — More Results, Same Traffic | 10xSEO", "75 chars · current, too long"),
            ("CRO Service in Georgia | More Sales, Same Traffic | 10xSEO", "58 chars · concise"),
            ("Conversion Rate Optimization (CRO) | 10xSEO Tbilisi", "51 chars · geo"),
            ("CRO Agency for Tbilisi & Global Brands | 10xSEO", "47 chars · international"),
            ("Increase Conversions Without Increasing Ad Spend | 10xSEO CRO", "60 chars · outcome-led"),
        ]),
        ("Meta description", [
            ("CRO services from 10xSEO: improve conversion rates with data analysis & A/B testing. Turn visits into real sales without increasing your ad spend.", "150 chars · current"),
            ("Conversion rate optimization for Tbilisi & international brands. A/B testing, UX audits, form optimization, landing page rewrites — more sales from same traffic.", "163 chars · borderline"),
            ("Your ad spend is fine — your funnel is leaking. 10xSEO's CRO audits, tests, and rewrites pages so more of your existing visitors actually convert.", "147 chars · pain-point"),
            ("Stop scaling ads on a broken funnel. 10xSEO's CRO service tests headlines, forms, layouts, and CTAs to lift conversion rates by 15–60% within 90 days.", "152 chars · specific outcome"),
            ("CRO done right: A/B tests rooted in heatmaps, user interviews, and revenue data — not vanity tests. 10xSEO lifts conversion rates for Tbilisi brands.", "150 chars · craft"),
        ]),
        ("H1", [
            ("Conversion Rate Optimization (CRO) — Increase Sales with Your Existing Traffic", "current"),
            ("More Sales / from the Traffic You Already Have", "outcome-led"),
            ("Stop Scaling Ads on a Leaky Funnel / Fix Conversions First", "pain-led"),
            ("CRO Service / for Ambitious Brands", "premium + scope"),
            ("Conversion Rate Optimization / Backed by Data, Not Opinion", "differentiator"),
        ]),
        ("Hero subheading", [
            ("Your traffic is fine. Your conversion rate isn't. 10xSEO audits your funnel, runs structured A/B tests, and rewrites the pages that quietly cost you sales.", "current improved"),
            ("Why double your ad spend when you can double your conversion rate first? CRO finds the friction killing your funnel and removes it, test by test.", "pain-led"),
            ("CRO rooted in heatmaps, user interviews, and revenue data — not opinions. Most clients see 15–60% conversion lift within 90 days.", "data + outcome"),
            ("From landing pages to checkout flows, we audit every step of your funnel and rebuild the pages costing you the most revenue first.", "scope"),
            ("CRO for Tbilisi and international brands serious about compounding ROI. Same ad spend, better funnel — usually 15–60% more conversions in 90 days.", "geo + outcome"),
        ]),
    ]),

    # === GOOGLE ADS ===
    ("/en/google-ads.html", "Google Ads Management", [
        ("Title", [
            ("Google Ads Management — Targeted Campaigns That Convert | 10xSEO", "65 chars · current"),
            ("Google Ads Agency in Tbilisi & Georgia | 10xSEO", "47 chars · geo concise"),
            ("PPC Management for Tbilisi & Global Brands | 10xSEO", "51 chars · international"),
            ("Google Ads That Pay Back — 10xSEO PPC Service Georgia", "53 chars · outcome"),
            ("ROI-Focused Google Ads Management | 10xSEO Tbilisi", "50 chars · ROI focus"),
        ]),
        ("Meta description", [
            ("Google Ads management for Tbilisi & international brands. Maximize ROI from search ads, display, and shopping campaigns with 10xSEO's precision targeting.", "157 chars · current"),
            ("Stop wasting Google Ads budget. 10xSEO manages search, shopping, display, and YouTube campaigns built around ROI — not impressions or vanity clicks.", "150 chars · pain-led"),
            ("Done-for-you Google Ads management. Search, Shopping, PMax, Display, YouTube — every campaign engineered for measurable revenue, not status reports.", "152 chars · scope"),
            ("Hire a Google Ads agency that obsesses over ROAS. 10xSEO manages campaigns for Tbilisi and global brands across Search, Shopping, PMax, and Display.", "150 chars · authority"),
            ("Google Ads campaigns that actually pay back. 10xSEO handles keyword research, ad copy, landing page handoff, and weekly bid optimization for Tbilisi brands.", "159 chars · process"),
        ]),
        ("H1", [
            ("Google Ads Management — Paid Advertising That Pays Off", "current"),
            ("Google Ads Management / Engineered for ROI", "ROI focus"),
            ("PPC That Pays Back / 10xSEO Google Ads Service", "outcome"),
            ("Stop Wasting Google Ads Budget / Hire 10xSEO", "pain-led"),
            ("Search, Shopping, PMax, Display / All in One Team", "scope"),
        ]),
        ("Hero subheading", [
            ("Profitable Google Ads campaigns for Tbilisi and international brands. Search, Shopping, PMax, Display, YouTube — every campaign engineered around revenue, not vanity metrics.", "outcome + scope"),
            ("Most agencies optimize for clicks. 10xSEO optimizes for ROAS. Weekly bid adjustments, keyword pruning, ad copy testing, and landing page feedback in one service.", "differentiator"),
            ("From keyword research to ad copy to landing page handoff, we manage Google Ads end-to-end. You see results in your CRM — not just a dashboard.", "scope + outcome"),
            ("Done-for-you Google Ads management for ambitious brands. Search, Shopping, PMax, Display, YouTube — managed by specialists who care about your revenue.", "premium positioning"),
            ("Google Ads campaigns built around your unit economics. We forecast CPL, target ROAS, and rebuild bidding around the metrics that actually move your business.", "data-led"),
        ]),
    ]),

    # === SEO AUDIT ===
    ("/en/seo-audit.html", "Free SEO Audit", [
        ("Title", [
            ("Free SEO Audit — Loom Video Analysis in 72 Hours | 10xSEO", "57 chars · current"),
            ("Free 10-Minute SEO Audit Delivered in 72 Hours | 10xSEO", "55 chars · time-bound"),
            ("Free SEO Audit for Tbilisi & Global Brands | 10xSEO", "51 chars · geo"),
            ("Personal Video SEO Audit | 10xSEO Free in 72 Hours", "50 chars · personal"),
            ("Get a Free SEO Audit from Georgia's #1 Agency | 10xSEO", "54 chars · authority"),
        ]),
        ("Meta description", [
            ("Free SEO audit: 10-minute Loom video where our expert reviews your site's issues, analyzes competitors, and shows real growth potential. Delivered in 72 hours.", "162 chars · current borderline"),
            ("Get a free SEO audit from 10xSEO. Personal 10-min Loom video, competitor analysis, and concrete next steps. Delivered within 72 hours — no sales pitch.", "152 chars · no-sales"),
            ("Tbilisi's #1 SEO agency reviews your site for free. 10-minute Loom video with specific issues, competitor gaps, and growth opportunities. 72-hour turnaround.", "159 chars · authority"),
            ("Stop guessing what's wrong with your SEO. Get a free personal video audit from a 14-year veteran. Concrete issues, real recommendations. 72-hour delivery.", "157 chars · pain-led"),
            ("Free SEO audit for ambitious brands. We record a 10-minute Loom walking through your site's issues, competitor gaps, and biggest growth levers. No catch.", "157 chars · no-strings"),
        ]),
        ("H1", [
            ("Free SEO Audit: Get a Personal Video Analysis in 72 Hours", "current"),
            ("Free SEO Audit / Personal Loom Video in 72 Hours", "concise"),
            ("Get a Free SEO Audit / from a 14-Year Veteran", "expertise"),
            ("10-Minute Loom Video / Specific to Your Site, in 72 Hours", "specific"),
            ("Your Site, Reviewed for Free / by Georgia's #1 SEO Agency", "authority"),
        ]),
        ("Hero subheading", [
            ("Our expert will record a video review for you, providing a step-by-step analysis of your site's issues, competitor strategies, and real growth opportunities for your brand.", "current"),
            ("No automated PDF, no canned recommendations. A real 10-minute Loom video where a senior SEO walks through your site, your competitors, and the specific wins on the table.", "differentiator"),
            ("We've recorded 500+ audits. Here's the format: 10 minutes, your screen + ours, specific issues with timestamps, and a written summary you can share internally.", "social proof + format"),
            ("Free, fast, and specific. The same audit format we use for paying clients — adapted to your stack and your competitive landscape. Delivered in 72 hours.", "same-quality"),
            ("Most audits are sales pitches in disguise. This one isn't. Submit your URL, we record a personalized Loom, you implement (or hire us — your call).", "no-pitch"),
        ]),
    ]),

    # === SEO COURSE ===
    ("/en/seo-course.html", "SEO Course (Training)", [
        ("Title", [
            ("SEO Course — 12 Hands-On Sessions With Davit Tsilosani | 10xSEO", "63 chars · current"),
            ("Practical SEO Course in Georgia | 12 Sessions with Davit | 10xSEO", "65 chars · geo"),
            ("Learn SEO from Georgia's #1 Practitioner | 10xSEO Course", "56 chars · authority"),
            ("SEO Training Program (12 Sessions) — Tbilisi | 10xSEO", "53 chars · concise"),
            ("In-Person SEO Course Tbilisi + Internship at 10xSEO", "51 chars · internship hook"),
        ]),
        ("Meta description", [
            ("SEO course by Davit Tsilosani — 12 hands-on sessions, real-world examples, and an internship opportunity at 10xSEO. Learn from Georgia's leading practitioner.", "159 chars · current"),
            ("12-session SEO training program with Davit Tsilosani. Real case studies, live Ahrefs access, certification, and an internship opportunity at 10xSEO.", "151 chars · deliverables"),
            ("Practical SEO course taught by Georgia's #1 SEO practitioner. 12 intensive sessions, 8–12 students per cohort, real client examples, internship path.", "152 chars · cohort"),
            ("Stop watching SEO tutorials on YouTube. Learn from someone who's shipped 50+ projects. 12 hands-on sessions, real cases, certificate, internship opportunity.", "159 chars · pain-led"),
            ("Tbilisi's most-cited SEO practitioner teaches a 12-week course. Hands-on, project-based, with real Ahrefs/SEMrush access and a path to interning at 10xSEO.", "159 chars · tools + path"),
        ]),
        ("H1", [
            ("SEO Course: 12 Intensive Workshops", "current"),
            ("Learn SEO from Georgia's #1 / Practitioner", "authority"),
            ("12-Week SEO Course / Hands-On + Internship Path", "scope + outcome"),
            ("Practical SEO Training / Built by 10xSEO", "branded"),
            ("Master SEO in 12 Sessions / with Davit Tsilosani", "founder-led"),
        ]),
        ("Hero subheading", [
            ("Here, you will learn to use the tools that market leaders use to dominate the top positions.", "current"),
            ("Twelve intensive sessions covering technical SEO, content, link building, AI search, and analytics — taught by someone who ships SEO every day, not just teaches it.", "scope + practitioner"),
            ("Small cohort (8–12 students), real client examples, live Ahrefs and SEMrush access, certification at the end, and an internship opportunity at 10xSEO for top students.", "complete value-stack"),
            ("Most SEO courses are 95% theory. This one's 80% practice. You'll work on real audits, run real keyword research, and ship real content during the program.", "differentiator"),
            ("The SEO training program Tbilisi's top marketers send their teams to. Hands-on, project-based, taught by Davit Tsilosani — and unlocks an internship at 10xSEO.", "social proof + path"),
        ]),
    ]),

    # === INDUSTRY: CONSTRUCTION ===
    ("/en/industries/construction.html", "Industry: Construction & Real Estate", [
        ("Title", [
            ("Construction & Real Estate SEO — Scale Your Sales | 10xSEO", "59 chars · current"),
            ("Real Estate Developer SEO in Tbilisi & Dubai | 10xSEO", "53 chars · geo"),
            ("SEO for Property Developers — From Tbilisi to Dubai | 10xSEO", "60 chars · international"),
            ("Construction SEO Agency in Georgia | 10xSEO", "44 chars · concise"),
            ("Real Estate SEO + Google Ads That Sell Units | 10xSEO", "53 chars · outcome"),
        ]),
        ("Meta description", [
            ("SEO, AI search & ads for property developers: a unified model focused on direct project sales growth. Specialized SEO for construction in Georgia.", "148 chars · current"),
            ("Real estate SEO for Tbilisi, Dubai, and emerging markets. Unit-level conversion focus — every campaign mapped to actual sales, not vanity traffic.", "147 chars · outcome"),
            ("Property developers in Georgia and Dubai hire 10xSEO when ranking on Google + AI search means more units sold. Specialized in real estate funnels.", "147 chars · social proof"),
            ("Stop wasting marketing on developer-buyer mismatch. 10xSEO's real estate SEO targets the exact searches your future buyers make — and turns them into tours.", "159 chars · pain-led"),
            ("Real estate SEO + Google Ads + AI search visibility, managed by a team that understands developer funnels. Tbilisi, Dubai, and international markets.", "151 chars · scope"),
        ]),
        ("H1", [
            ("Your Real Estate Development Company / With Complete Digital Support", "current"),
            ("Real Estate SEO / That Sells Units, Not Clicks", "outcome-led"),
            ("From Tbilisi to Dubai / Real Estate SEO That Converts", "geo + outcome"),
            ("Construction SEO / Built for Developer Funnels", "specific funnel"),
            ("Sell More Units / with Real Estate SEO from 10xSEO", "outcome"),
        ]),
        ("Hero subheading", [
            ("From SEO to Google Ads: Five services to grow your project's sales. One team, unified accountability, and maximum visibility.", "current"),
            ("Property developer marketing under one roof: SEO, Google Ads, AEO, CRO, and copywriting — all built around the searches your buyers actually make.", "scope"),
            ("Real estate buyers in Tbilisi and Dubai start on Google and finish in ChatGPT. 10xSEO makes sure your project shows up in both — and converts.", "geo + AI"),
            ("Stop paying for clicks that never tour. 10xSEO's real estate marketing targets the specific neighborhood, price tier, and unit type your buyer is searching for.", "specificity"),
            ("Five services, one accountable team. Tbilisi, Dubai, and select international markets — 12+ years of real estate marketing experience baked into every campaign.", "expertise"),
        ]),
    ]),

    # === INDUSTRY: HEALTHCARE ===
    ("/en/industries/healthcare.html", "Industry: Healthcare & Clinics", [
        ("Title", [
            ("Healthcare SEO — SEO Services for Clinics & Medical Brands | 10xSEO", "68 chars · current, too long"),
            ("Medical SEO + AEO for Clinics in Georgia | 10xSEO", "49 chars · scope"),
            ("Healthcare SEO Agency Tbilisi — Clinics, Hospitals | 10xSEO", "59 chars · authority"),
            ("Clinic SEO + Google Ads That Book Appointments | 10xSEO", "55 chars · outcome"),
            ("E-E-A-T Compliant Healthcare SEO in Georgia | 10xSEO", "52 chars · YMYL signal"),
        ]),
        ("Meta description", [
            ("SEO & AEO strategies for clinics. Strengthen your Google rankings, attract patients, and rank in AI search answers. Healthcare SEO experts at 10xSEO.", "151 chars · current"),
            ("Healthcare SEO for clinics, hospitals, and medical specialists. E-E-A-T compliant content, ChatGPT visibility, and conversion-focused appointment funnels.", "157 chars · compliance"),
            ("Tbilisi clinics that rank #1 hire 10xSEO. Specialized healthcare SEO with E-E-A-T-compliant content, patient-intent keywords, and AI search optimization.", "157 chars · authority"),
            ("Stop competing on price — compete on visibility. 10xSEO's healthcare SEO ranks your clinic where patients actually search: Google, Maps, and ChatGPT.", "153 chars · pain + scope"),
            ("Healthcare SEO with regulatory awareness. We build E-E-A-T signals, optimize for medical search queries, and engineer appointment-booking funnels.", "146 chars · craft"),
        ]),
        ("H1", [
            ("SEO and AI Strategies / Make Your Medical Service the #1 Choice for Patients", "current"),
            ("Healthcare SEO / Built for Clinics That Want to Rank", "scope"),
            ("Rank #1 Where Patients Search / Healthcare SEO from 10xSEO", "outcome"),
            ("E-E-A-T Compliant Healthcare SEO / from Tbilisi's #1 Agency", "compliance"),
            ("More Patient Appointments / Same Marketing Budget", "outcome-led"),
        ]),
        ("Hero subheading", [
            ("Healthcare SEO done right means E-E-A-T-compliant content, medical-query keyword research, and conversion paths that respect both Google's YMYL rules and your patient's trust.", "differentiator"),
            ("Patients search Google, Maps, and ChatGPT before they book. 10xSEO makes sure your clinic shows up first on every platform that matters.", "outcome + scope"),
            ("Specialized SEO for clinics and medical brands in Tbilisi and beyond. E-E-A-T signals, expert-reviewed content, and patient-intent keyword targeting.", "expertise"),
            ("From a single clinic to multi-location hospital groups, 10xSEO scales healthcare SEO with the regulatory awareness and patient-conversion focus your industry demands.", "scale + scope"),
            ("Most agencies treat healthcare like e-commerce. 10xSEO doesn't. We build the trust signals Google requires for YMYL pages — without sacrificing conversion.", "differentiator + craft"),
        ]),
    ]),

    # === INDUSTRY: FINANCIAL SERVICES ===
    ("/en/industries/financial-services.html", "Industry: Financial Services", [
        ("Title", [
            ("Financial Services SEO — Banks, Insurance, Accounting | 10xSEO", "63 chars · current"),
            ("Financial SEO Agency in Georgia + Dubai | 10xSEO", "48 chars · geo"),
            ("Bank & Fintech SEO in Tbilisi | 10xSEO", "39 chars · concise"),
            ("YMYL-Compliant Financial Services SEO | 10xSEO Georgia", "54 chars · compliance"),
            ("Financial SEO + AEO for Banks & Fintech | 10xSEO", "48 chars · outcome"),
        ]),
        ("Meta description", [
            ("How do you attract clients in finance? SEO for banks, insurance & accounting: high-quality content + technical optimization that builds trust and rankings.", "155 chars · current"),
            ("Financial services SEO for banks, insurance, fintech, and accounting firms. YMYL-compliant content, AEO visibility, and conversion-focused product pages.", "157 chars · scope"),
            ("Banks and fintech firms in Tbilisi and Dubai hire 10xSEO when compliance matters as much as ranking. Specialized financial SEO with YMYL awareness.", "147 chars · social proof"),
            ("Financial SEO done by people who understand DFSA, NBG, and compliance reviews. We rank banks, insurance brands, and fintech without crossing any lines.", "152 chars · expertise"),
            ("Stop letting compliance freeze your marketing. 10xSEO's financial SEO ships content that ranks, passes legal review, and converts qualified leads.", "147 chars · pain-led"),
        ]),
        ("H1", [
            ("Financial SEO Services", "current"),
            ("Financial Services SEO / Compliant, Ranking, Converting", "triad"),
            ("YMYL-Compliant Financial SEO / from Georgia's #1 Agency", "compliance"),
            ("Bank & Fintech SEO / That Ranks Without Compliance Risk", "specific"),
            ("Financial Marketing That Converts / Without Crossing Compliance Lines", "differentiator"),
        ]),
        ("Hero subheading", [
            ("Delivered with industry expertise, regulatory compliance, and measurable results.", "current"),
            ("Banks, insurance, fintech, accounting — financial services SEO that respects E-E-A-T and YMYL while still ranking and converting. Tbilisi-based, global reach.", "scope + compliance"),
            ("Compliance shouldn't kill your marketing. 10xSEO's financial SEO ships content that ranks on Google, gets cited in ChatGPT, and passes legal review on first pass.", "pain + craft"),
            ("Six sub-niches covered: banking, insurance, fintech, accounting, wealth management, crypto. Each with its own YMYL playbook and conversion approach.", "scope detail"),
            ("From DFSA compliance in Dubai to NBG awareness in Georgia, we build financial SEO content that ranks, converts, and survives legal review every time.", "regulatory-specific"),
        ]),
    ]),

    # === INDUSTRY: E-COMMERCE ===
    ("/en/industries/ecommerce.html", "Industry: E-commerce", [
        ("Title", [
            ("E-commerce SEO Services — Grow Online Sales | 10xSEO", "53 chars · current"),
            ("Shopify & WooCommerce SEO in Georgia | 10xSEO", "45 chars · platform"),
            ("E-commerce SEO Agency Tbilisi & International | 10xSEO", "54 chars · geo"),
            ("Online Store SEO + Product Page Optimization | 10xSEO", "54 chars · scope"),
            ("E-commerce SEO Built for Compound Revenue | 10xSEO", "50 chars · outcome"),
        ]),
        ("Meta description", [
            ("E-commerce SEO: take your products to international markets via search engines. Full technical support for online stores and organic growth strategy.", "151 chars · current"),
            ("Shopify, WooCommerce, Magento — e-commerce SEO from Tbilisi's #1 agency. Product page optimization, category SEO, technical fixes, and international expansion.", "159 chars · platform"),
            ("Online stores that scale hire 10xSEO. Product schema, category SEO, technical Core Web Vitals, AEO visibility, and organic growth playbooks for any platform.", "157 chars · authority"),
            ("Stop burning Google Ads budget on traffic that doesn't repeat. 10xSEO's e-commerce SEO builds the organic engine your CFO will thank you for.", "143 chars · pain-led"),
            ("E-commerce SEO for Shopify, WooCommerce, and Magento stores. Technical, content, links, and AI search visibility — engineered for repeatable revenue growth.", "156 chars · scope"),
        ]),
        ("H1", [
            ("E-commerce SEO - Your Products on the First Page of Google", "current"),
            ("E-commerce SEO / Built for Repeatable Revenue", "outcome"),
            ("Shopify, WooCommerce, Magento / All Optimized by 10xSEO", "platform-led"),
            ("Online Store SEO / from Tbilisi's #1 Agency", "geo + authority"),
            ("Scale Organic Revenue / E-commerce SEO from 10xSEO", "outcome-led"),
        ]),
        ("Hero subheading", [
            ("Shopify, WooCommerce, Magento - Experience in global markets: Georgia, USA, UK, United Arab Emirates", "current"),
            ("Product schema, category hierarchies, Core Web Vitals, AEO visibility — every layer of e-commerce SEO handled by a single accountable team.", "scope"),
            ("Stop relying entirely on paid ads. 10xSEO builds the organic engine that compounds — product page SEO, category optimization, content marketing, AI search.", "pain + scope"),
            ("E-commerce SEO across Shopify, WooCommerce, and Magento. We've shipped projects from Tbilisi to the US, UK, and UAE — each with its own technical playbook.", "platform + global"),
            ("Most e-commerce SEO is product page tweaks. Ours covers category architecture, internal linking, schema, Core Web Vitals, and AEO visibility — end to end.", "differentiator"),
        ]),
    ]),
]


def render_markdown(pages):
    """Generate markdown sections matching translation-review.md format."""
    out = []
    for idx, (page_path, label, fragments) in enumerate(pages, start=6):  # start=6 because priority pages are 1-5
        out.append("---")
        out.append("")
        out.append(f"# {idx}. {page_path} — PENDING")
        out.append("")
        out.append(f"**Page:** {label}")
        out.append("")
        for frag_label, options in fragments:
            out.append(f"## {frag_label}")
            out.append("")
            for i, opt in enumerate(options, start=1):
                if isinstance(opt, tuple):
                    text, meta = opt
                else:
                    text, meta = opt, ""
                meta_str = f" ({meta})" if meta else ""
                out.append(f"- [ ] V{i}: `{text}`{meta_str}")
            out.append("")
    return "\n".join(out)


def main():
    current = REVIEW_PATH.read_text(encoding="utf-8")

    # Remove any old "Other pages" placeholder section if present
    if "# 6. Other pages" in current:
        current = current.split("# 6. Other pages")[0].rstrip() + "\n\n"

    new_section = render_markdown(PAGES)
    final = current.rstrip() + "\n\n" + new_section + "\n"
    REVIEW_PATH.write_text(final, encoding="utf-8")
    print(f"✓ Wrote {REVIEW_PATH} (+{len(PAGES)} pages, "
          f"{sum(len(p[2]) for p in PAGES)} fragments, "
          f"{sum(len(o) for p in PAGES for _, o in p[2])} options)")


if __name__ == "__main__":
    main()
