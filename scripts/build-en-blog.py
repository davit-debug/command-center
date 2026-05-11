#!/usr/bin/env python3
"""Build /en/blog/ HTML files from a template + per-article data.

Generates EN-only blog posts (no KA counterpart) using the existing
/blog/ template structure with proper /en/blog/ depth-aware paths.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "blog" / "best-seo-agency-in-georgia.html"
OUT_DIR = ROOT / "en" / "blog"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# ARTICLE 1: What Is AEO?
# ============================================================
ARTICLE_1 = {
    "slug": "what-is-aeo",
    "title": "What Is AEO? Answer Engine Optimization Explained — 10xSEO",
    "h1": "What Is AEO? Answer Engine Optimization Explained",
    "description": "AEO (Answer Engine Optimization) makes your brand the source AI engines cite. Learn what AEO is, how it differs from SEO, and how to start optimizing for ChatGPT, Gemini, and Perplexity.",
    "image": "what-is-aeo.webp",
    "image_alt": "What Is AEO? Answer Engine Optimization explained by 10xSEO",
    "published": "2025-06-04",
    "modified": "2026-05-11",
    "reading_minutes": 9,
    "intro": [
        "Search is changing — and faster than most marketing teams realize. Instead of scanning a list of blue links, users increasingly ask a question and accept a single AI-generated answer. That answer is being assembled by Large Language Models that cite some sources and ignore the rest.",
        "<strong>Answer Engine Optimization (AEO)</strong> is the discipline of becoming the source those engines cite. It builds on classic SEO but optimizes for a new endpoint: the generated answer, not the ranked link.",
        "This guide explains what AEO is, why it matters, how it relates to SEO and GEO, and the practical steps every brand should take to remain visible as the search experience moves to AI.",
    ],
    "sections": [
        {
            "id": "what-is-aeo",
            "heading": "What Is Answer Engine Optimization?",
            "paragraphs": [
                "AEO is the practice of optimizing content so that answer engines — ChatGPT, Gemini, Perplexity, Claude, and Google AI Overviews — recognize it as a trustworthy source and quote it in their generated responses.",
                "Where traditional SEO targets a ranked position in a list of links, AEO targets <em>inclusion in a synthesized answer</em>. The mechanics are different: instead of optimizing for crawl + ranking signals, you optimize for how a language model extracts, weighs, and attributes information.",
                "A page that ranks #1 on Google can still be invisible inside ChatGPT. AEO closes that gap.",
            ],
        },
        {
            "id": "ai-changes-search-behavior",
            "heading": "How AI Is Reshaping Search Behavior",
            "paragraphs": [
                "User behavior has shifted in three measurable ways. First, average query length is growing — people are typing full questions instead of short keyword fragments. Second, click-through rates from traditional SERPs are dropping as users accept the AI-generated answer at the top. Third, conversational follow-ups (\"and what about pricing?\") have replaced new search sessions.",
                "The result is a smaller pool of clicks distributed across the sources an answer engine chose to cite. If your brand isn't in that small pool, the traffic isn't simply harder to win — it's gone.",
            ],
        },
        {
            "id": "structure-and-depth",
            "heading": "Why Structure and Depth Both Matter",
            "paragraphs": [
                "Answer engines reward two properties at once: <strong>extractable structure</strong> (clear H2/H3, short definitional sentences, lists, tables) and <strong>topical depth</strong> (enough surrounding context that the model trusts the source).",
                "Pages with only structure feel shallow and rarely get cited as primary sources. Pages with depth but no structure get skipped because the model can't cleanly extract a span of text to quote. AEO content needs both — a scannable skeleton with substantive flesh on every bone.",
            ],
            "list": {
                "type": "ul",
                "items": [
                    "<strong>Definitional opening:</strong> answer the page's main question in the first 50–80 words.",
                    "<strong>Structured headings:</strong> H2/H3 phrased as the actual questions users ask.",
                    "<strong>Concise paragraphs:</strong> 2–4 sentences each, with one main idea per paragraph.",
                    "<strong>Schema markup:</strong> Article, FAQPage, and HowTo where appropriate.",
                    "<strong>First-party data:</strong> statistics, case studies, and original examples models can't get elsewhere.",
                ],
            },
        },
        {
            "id": "voice-search",
            "heading": "Voice Search Optimization",
            "paragraphs": [
                "Voice queries are conversational. Someone speaking to Google Assistant or Siri uses full sentences, not keyword strings. AEO content written in plain English with question-based headings naturally matches voice queries.",
                "Practical tactic: review your top-performing pages and audit whether the H2/H3 are phrased as questions a real person would ask out loud. \"AEO Strategy\" is a keyword. \"How do I build an AEO strategy?\" is a voice query — and the latter is much more likely to be matched and cited.",
            ],
        },
        {
            "id": "measurement",
            "heading": "Measuring AEO Results",
            "paragraphs": [
                "Classic SEO metrics (rank, impressions, CTR) only tell part of the story under AEO. You also need to track:",
            ],
            "list": {
                "type": "ul",
                "items": [
                    "<strong>Citation share:</strong> how often your domain appears as a cited source inside ChatGPT, Perplexity, and Google AI Overviews for your target queries.",
                    "<strong>Brand prompt mentions:</strong> how often users prompt an answer engine with your brand name (a leading indicator of AI-search demand).",
                    "<strong>Referral traffic from AI engines:</strong> direct visits from ChatGPT, Perplexity, and Gemini referrer URLs.",
                    "<strong>Assisted conversions:</strong> AI-search visits often have longer paths to conversion — multi-touch attribution captures their real value.",
                ],
            },
        },
        {
            "id": "aeo-strategy",
            "heading": "Building an AEO Strategy",
            "paragraphs": [
                "An AEO strategy isn't a separate replacement for SEO — it's a parallel track. The strongest brands run both. Start with a citation audit (where are answer engines pulling your category's information today?), then prioritize the prompts where competitors dominate the citation pool but your content is materially better.",
                "From there, the work is mostly content engineering: restructure pages around the prompts you want to win, layer in original data, and make every claim explicit enough that a language model can extract it as a quotable span.",
            ],
        },
        {
            "id": "integration",
            "heading": "Integrating AEO into Your Overall SEO Plan",
            "paragraphs": [
                "AEO and SEO share the same content engine. The difference is the optimization target. A team running both well treats every new article as a dual-purpose asset: it must rank in Google's traditional SERP and be quotable inside an answer engine.",
                "In practical terms, this means a single QA workflow that checks the page against two scorecards: traditional on-page SEO (title, meta, internal linking, technical health) and AEO readiness (definitional opening, structured headings, schema markup, original data).",
            ],
        },
        {
            "id": "next-steps",
            "heading": "Practical Next Steps",
            "paragraphs": [
                "If you're new to AEO, the highest-ROI first move is auditing your existing top pages — the ones already ranking on Google — and rewriting their openings as direct, extractable answers to the main query. That single change typically lifts citation rates inside ChatGPT and Perplexity within weeks.",
                "Need help executing? <a href=\"../ai-seo.html\">10xSEO's AI SEO service</a> handles AEO + GEO end-to-end — from prompt research to content engineering to citation tracking.",
            ],
        },
    ],
    "faq": [
        ("What is the difference between SEO and AEO?",
         "SEO optimizes pages for traditional ranked search results — the goal is appearing in the top blue links. AEO optimizes for inclusion in AI-generated answers from engines like ChatGPT, Gemini, and Perplexity. The two share underlying signals (quality content, structure, authority) but the optimization target is different: a ranked link versus a cited source."),
        ("Does AEO replace SEO?",
         "No. The two work together. Most users still encounter your brand through traditional search before they ask an AI engine. SEO drives the discovery layer; AEO ensures you remain visible once that user shifts to an answer engine. Brands that drop SEO to chase AEO usually lose more traffic than they gain."),
        ("Which AI engines should I optimize for?",
         "The high-impact set today is ChatGPT, Google AI Overviews, Perplexity, and Gemini. Claude is growing fast in B2B contexts. The good news: the structural changes that win in one engine usually help in all of them, because they share underlying training and citation behaviors."),
        ("How long does AEO take to show results?",
         "Faster than traditional SEO in many cases. Re-writing the first 80 words of a page can change citation behavior within 2–4 weeks because answer engines re-crawl frequently. Building citation share for a brand new domain still takes 3–6 months, similar to ranking timelines."),
        ("Do I need schema markup for AEO?",
         "Schema markup helps but isn't strictly required. FAQPage and Article schema make it easier for parsers to extract definitional content, and HowTo schema helps with step-based queries. We recommend adding it where it fits naturally — don't force schema onto pages that don't structurally need it."),
    ],
    "related": [
        ("aeo-optimization-agency-dubai.html", "AEO Optimization Agency Dubai — modern SEO and ChatGPT optimization", "8 min"),
        ("../ai-seo.html", "AI SEO (GEO/AEO) — visibility in ChatGPT, Gemini and Perplexity", "service page"),
        ("../seo-audit.html", "Free SEO Audit — Loom video analysis in 72 hours", "service page"),
    ],
}

# ============================================================
# ARTICLE 2: AEO Optimization Agency Dubai
# ============================================================
ARTICLE_2 = {
    "slug": "aeo-optimization-agency-dubai",
    "title": "AEO Optimization Agency Dubai — ChatGPT SEO for the UAE | 10xSEO",
    "h1": "AEO Optimization Agency Dubai: ChatGPT SEO for the UAE Market",
    "description": "Looking for a top AEO Optimization Agency in Dubai? 10xSEO helps UAE brands win in AI search — ChatGPT optimization, Answer Engine SEO, and AI Overview rankings for the GCC market.",
    "image": "aeo-optimization-agency-dubai.webp",
    "image_alt": "AEO Optimization Agency Dubai — ChatGPT SEO for UAE businesses",
    "published": "2025-08-14",
    "modified": "2026-05-11",
    "reading_minutes": 8,
    "intro": [
        "The Dubai search market has changed faster than almost any other in the GCC. Voice queries in Arabic and English now share the top of the search funnel with AI engines like ChatGPT, Gemini, and Perplexity — and the rules for visibility have changed with them.",
        "An <strong>AEO Optimization Agency in Dubai</strong> isn't a luxury anymore. For UAE businesses competing across hospitality, real estate, financial services, healthcare, and e-commerce, getting cited inside AI answers is becoming as commercially important as ranking on Google itself.",
        "This guide explains what an AEO agency actually does for a Dubai-based business, how ChatGPT SEO fits into modern strategy, and what to look for when hiring one.",
    ],
    "sections": [
        {
            "id": "what-is-aeo",
            "heading": "What Is AEO Optimization?",
            "paragraphs": [
                "AEO (Answer Engine Optimization) is the practice of optimizing your content so AI-powered engines — ChatGPT, Gemini, Perplexity, Claude, and Google AI Overviews — recognize your brand as a trustworthy source and cite it in their generated answers.",
                "For Dubai businesses, AEO becomes especially valuable because the local market is a heavy adopter of AI assistants. Expats, tourists, and business travelers regularly ask ChatGPT for restaurant recommendations, real-estate research, financial services comparisons, and clinic referrals. If your brand isn't visible in those answers, you're invisible at the exact moment of intent.",
            ],
        },
        {
            "id": "why-dubai-agency",
            "heading": "Why Choose a Dubai-Focused AEO Agency?",
            "paragraphs": [
                "Three things make Dubai different from other markets:",
            ],
            "list": {
                "type": "ol",
                "items": [
                    "<strong>Bilingual demand.</strong> Real Dubai search behavior spans Arabic, English, and English transliterations of Arabic terms. AEO content has to be optimized for all three.",
                    "<strong>Regulatory compliance.</strong> DFSA (financial services), DHA (healthcare), and RERA (real estate) all impose content rules that affect what an AI engine will quote. Generic content fails compliance checks; properly scoped content gets cited.",
                    "<strong>Hyper-competitive industries.</strong> Real estate, finance, and clinics in Dubai have unusually high content saturation. AEO is one of the few channels where a new entrant can outpace established players within months.",
                ],
            },
            "paragraphs2": [
                "An agency that understands these three factors can compress months of trial-and-error into a working playbook.",
            ],
        },
        {
            "id": "chatgpt-seo",
            "heading": "ChatGPT SEO: The Next Evolution of Search Optimization",
            "paragraphs": [
                "\"ChatGPT SEO\" is shorthand for the cluster of techniques that get your brand cited inside ChatGPT (and adjacent answer engines). It's a specific application of AEO with a heavier focus on the conversational, prompt-driven workflow that ChatGPT users follow.",
                "The mechanics are simple to describe and harder to execute: identify the prompts your customers actually type into ChatGPT, audit which sources currently get cited for those prompts, and produce content that competes on quality, structure, and original data. Repeat for every commercially-relevant prompt cluster.",
            ],
            "h3": [
                {
                    "heading": "How It Works in Practice",
                    "paragraphs": [
                        "A typical engagement starts with a prompt audit. We collect the 50–200 prompts your target audience actually uses inside ChatGPT, document which sources get cited today, and score them on a competition-versus-content-quality matrix.",
                        "From there, we prioritize prompts where the citation pool is weak (easy wins) and where the prompt has high commercial intent (real revenue value). Content is then re-engineered around those prompts — definitional openings, structured headings, schema markup, and original UAE-specific data.",
                    ],
                },
            ],
        },
        {
            "id": "transformation",
            "heading": "How AEO Transforms Your SEO Strategy in Dubai",
            "paragraphs": [
                "A Dubai business that runs both SEO and AEO in parallel sees three changes within the first quarter:",
            ],
            "list": {
                "type": "ul",
                "items": [
                    "<strong>Branded prompt volume rises.</strong> More users type your brand name into ChatGPT — a leading indicator of AI-search demand.",
                    "<strong>Citation share grows.</strong> Your domain appears in a higher percentage of AI answers for your category's prompts.",
                    "<strong>Conversion quality improves.</strong> AI-search traffic tends to be late-funnel — users who ask ChatGPT have already done some research and are closer to a decision.",
                ],
            },
            "paragraphs2": [
                "None of this replaces classic SEO. It compounds on top of it.",
            ],
        },
        {
            "id": "best-practices",
            "heading": "AEO Best Practices for Modern Dubai Brands",
            "paragraphs": [
                "Across our work with UAE clients, the practices that consistently move the needle are:",
            ],
            "list": {
                "type": "ul",
                "items": [
                    "<strong>Localize at the prompt level.</strong> Generic global content rarely gets cited for Dubai-specific prompts. Add explicit UAE context (regulators, currency, neighborhoods, local compliance).",
                    "<strong>Lead with the answer.</strong> First sentence of every page = the direct answer. Everything else is supporting context.",
                    "<strong>Add first-party data.</strong> Original numbers, internal case studies, and quotes from named experts. AI engines weight unique data heavily.",
                    "<strong>Bilingual content where it matters.</strong> Arabic version of high-intent pages, properly cross-linked with hreflang.",
                    "<strong>Compliance-aware language.</strong> Avoid YMYL violations in finance and healthcare pages — they reduce citation likelihood.",
                ],
            },
        },
        {
            "id": "ready",
            "heading": "Ready to Boost Your Rankings in Dubai?",
            "paragraphs": [
                "AEO is the highest-leverage marketing channel available to Dubai brands today — and the window of low competition won't stay open much longer. Brands that invest now will own the citation real estate for years.",
                "If you'd like to see what a focused AEO + SEO engagement looks like for your business, <a href=\"../contact-us.html\">get in touch with 10xSEO</a> for a free strategy session. We'll audit your current AI-search visibility and show you exactly where the citation gaps are.",
            ],
        },
    ],
    "faq": [
        ("Do I need an AEO agency if I already have an SEO agency?",
         "Most traditional SEO agencies haven't built out an AEO practice yet. If your current agency is tracking AI citations, optimizing content for prompt-based queries, and measuring share-of-voice inside ChatGPT or Perplexity, you're set. If not, a specialized AEO agency complements — it doesn't replace — the classic SEO work."),
        ("How is AEO Optimization different from ChatGPT SEO?",
         "AEO is the broader discipline — optimizing for all answer engines (ChatGPT, Gemini, Perplexity, Claude, Google AI Overviews). ChatGPT SEO is a subset focused specifically on ChatGPT. In practice, the techniques overlap heavily, so most AEO work also improves ChatGPT visibility."),
        ("How long does AEO take to show results in Dubai?",
         "We typically see meaningful citation-share movement within 6–10 weeks. Full ROI on a competitive Dubai vertical (real estate, finance, clinics) usually takes 4–6 months. Brand-new domains take longer because answer engines weight domain authority heavily."),
        ("Does AEO work for Arabic content?",
         "Yes — and the competition is much lower in Arabic AEO than in English. AI engines now handle Arabic well, and most Dubai businesses haven't built Arabic-optimized content yet. This is one of the highest-ROI segments we see today."),
        ("What's the typical investment for AEO in the UAE?",
         "It depends on industry and number of target prompts. A focused AEO retainer with one prompt cluster and content production runs from a few thousand USD per month. A full AEO + SEO engagement for a competitive vertical is meaningfully more. We can scope a fixed-price pilot for most situations."),
        ("Can AEO help with Google AI Overviews?",
         "Yes. Google AI Overviews and ChatGPT use similar signals to select sources. The same content engineering that wins inside ChatGPT generally also wins inside AI Overviews — so a single AEO investment pays back across multiple engines."),
    ],
    "related": [
        ("what-is-aeo.html", "What Is AEO? Answer Engine Optimization explained", "9 min"),
        ("../ai-seo.html", "AI SEO (GEO/AEO) — visibility in ChatGPT, Gemini and Perplexity", "service page"),
        ("../industries/financial-services.html", "Financial Services SEO — Banks, Insurance, Accounting", "service page"),
    ],
}


def render_section(s):
    """Render a section dict to HTML."""
    out = [f'<h2 id="{s["id"]}">{s["heading"]}</h2>']
    for p in s.get("paragraphs", []):
        out.append(f'<p>{p}</p>')
    if "list" in s:
        list_tag = s["list"]["type"]
        out.append(f'<{list_tag}>')
        for it in s["list"]["items"]:
            out.append(f'  <li>{it}</li>')
        out.append(f'</{list_tag}>')
    for p in s.get("paragraphs2", []):
        out.append(f'<p>{p}</p>')
    for sub in s.get("h3", []):
        out.append(f'<h3>{sub["heading"]}</h3>')
        for p in sub.get("paragraphs", []):
            out.append(f'<p>{p}</p>')
    return "\n            ".join(out)


def render_faq(faq_pairs):
    """Render FAQ HTML + schema."""
    html_parts = ['<h2 id="faq">Frequently Asked Questions</h2>']
    for q, a in faq_pairs:
        html_parts.append(f'<h3>{q}</h3>')
        html_parts.append(f'<p>{a}</p>')
    return "\n            ".join(html_parts)


def render_toc(article):
    """Sidebar TOC."""
    items = []
    for i, s in enumerate(article["sections"], 1):
        items.append(
            f'<a href="#{s["id"]}" class="toc-link block text-sm text-body dark:text-body-dark hover:text-primary dark:hover:text-primary-light pl-3 border-l-2 border-gray-200 dark:border-gray-700 transition-colors">{i}. {s["heading"]}</a>'
        )
    items.append(
        f'<a href="#faq" class="toc-link block text-sm text-body dark:text-body-dark hover:text-primary dark:hover:text-primary-light pl-3 border-l-2 border-gray-200 dark:border-gray-700 transition-colors">{len(article["sections"])+1}. FAQ</a>'
    )
    return "\n                ".join(items)


def render_related(items):
    """Related articles grid."""
    cards = []
    for href, title, meta in items:
        cards.append(
            f'<a href="{href}" class="group bg-surface-alt dark:bg-surface-dark-alt rounded-xl p-4 border border-gray-100 dark:border-gray-800 hover:shadow-md transition-shadow">\n'
            f'  <p class="text-xs text-body/70 dark:text-body-dark/70 mb-2">{meta}</p>\n'
            f'  <p class="font-heading font-semibold text-heading dark:text-heading-dark text-sm group-hover:text-primary dark:group-hover:text-primary-light transition-colors leading-snug">{title}</p>\n'
            f'</a>'
        )
    return "\n              ".join(cards)


def render_faq_schema(faq_pairs):
    import json
    items = []
    for q, a in faq_pairs:
        items.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a}
        })
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": items,
    }, ensure_ascii=False)


def render_blog_posting_schema(article, url):
    import json
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": article["h1"],
        "description": article["description"],
        "image": f"https://10xseo.ge/images/blog/{article['image']}",
        "url": url,
        "datePublished": article["published"],
        "dateModified": article["modified"],
        "author": {"@type": "Organization", "name": "10XSEO", "url": "https://10xseo.ge"},
        "publisher": {
            "@type": "Organization",
            "name": "10XSEO",
            "url": "https://10xseo.ge",
            "logo": {"@type": "ImageObject", "url": "https://10xseo.ge/images/logo.webp"}
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "inLanguage": "en-US",
    }, ensure_ascii=False)


def build_article(article):
    slug = article["slug"]
    url = f"https://10xseo.ge/en/blog/{slug}.html"
    image_path = f"../../images/blog/{article['image']}"
    image_abs = f"https://10xseo.ge/images/blog/{article['image']}"

    # Build article body HTML
    intro_html = "\n            ".join(f'<p>{p}</p>' for p in article["intro"])

    # Split sections: first half before inline CTA, rest after
    half = max(1, len(article["sections"]) // 2)
    sections_top = "\n            ".join(render_section(s) for s in article["sections"][:half])
    sections_bottom = "\n            ".join(render_section(s) for s in article["sections"][half:])
    faq_html = render_faq(article["faq"])
    toc_html = render_toc(article)
    related_html = render_related(article["related"])

    faq_schema = render_faq_schema(article["faq"])
    blog_schema = render_blog_posting_schema(article, url)

    html = f"""<!DOCTYPE html>
<html lang="en" class="dark scroll-smooth" data-beasties-container>
<head>
  <meta charset="UTF-8">
  <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
  <meta name="robots" content="noindex, nofollow">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="preload" as="image" href="{image_path}" fetchpriority="high">
  <title>{article['title']}</title>
  <link rel="canonical" href="{url}">
  <link rel="alternate" hreflang="en" href="{url}">
  <link rel="alternate" hreflang="x-default" href="{url}">
  <meta name="description" content="{article['description']}">
  <link rel="stylesheet" href="../../assets/site.tailwind.css">
  <style>
    @font-face {{ font-family: 'Dachi the Lynx'; src: url('../../fonts/DachiTheLynx.woff2') format('woff2'); font-weight: 400; font-style: normal; font-display: swap; }}
    body {{ font-family: 'FiraGO', sans-serif; }}
    .header-scrolled {{ backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); }}
    .safe-bottom {{ padding-bottom: env(safe-area-inset-bottom, 0px); }}
    #reading-progress {{ transition: width 100ms linear; }}
    .prose h2 {{ font-family: 'Dachi the Lynx', sans-serif; font-size: 1.5rem; font-weight: 700; margin-top: 2.5rem; margin-bottom: 1rem; line-height: 1.3; }}
    .prose h3 {{ font-family: 'Dachi the Lynx', sans-serif; font-size: 1.25rem; font-weight: 600; margin-top: 2rem; margin-bottom: 0.75rem; line-height: 1.4; }}
    .prose p {{ margin-bottom: 1.5rem; line-height: 2; font-size: 1.125rem; }}
    .prose ul, .prose ol {{ margin-bottom: 1.25rem; padding-left: 1.5rem; }}
    .prose li {{ margin-bottom: 0.625rem; line-height: 2; font-size: 1.125rem; }}
    .prose ul li {{ list-style-type: disc; }}
    .prose ol li {{ list-style-type: decimal; }}
    .prose a {{ color: #8B5CF6; text-decoration: underline; }}
    .dark .prose a {{ color: #00ff88; }}
    .toc-link.active {{ color: #8B5CF6; font-weight: 600; border-left-color: #8B5CF6; }}
    .dark .toc-link.active {{ color: #A78BFA; border-left-color: #A78BFA; }}
    @keyframes aiGradient {{ 0%{{background-position:0% 50%}} 50%{{background-position:100% 50%}} 100%{{background-position:0% 50%}} }}
    .ai-cta-animate {{ background: linear-gradient(-45deg,#8B5CF6,#3B82F6,#14B8A6,#8B5CF6) !important; background-size:300% 300% !important; animation: aiGradient 4s ease infinite; box-shadow: 0 4px 25px rgba(139,92,246,.35); }}
  </style>
  <meta property="og:type" content="article">
  <meta property="og:title" content="{article['title']}">
  <meta property="og:description" content="{article['description']}">
  <meta property="og:url" content="{url}">
  <meta property="og:site_name" content="10XSEO">
  <meta property="og:locale" content="en_US">
  <meta property="og:image" content="{image_abs}">
  <meta property="og:image:alt" content="{article['image_alt']}">
  <meta property="og:image:type" content="image/webp">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{article['title']}">
  <meta name="twitter:description" content="{article['description']}">
  <meta name="twitter:image" content="{image_abs}">
  <meta name="twitter:image:alt" content="{article['image_alt']}">
  <script type="application/ld+json">{blog_schema}</script>
  <script type="application/ld+json">{faq_schema}</script>
</head>
<body class="font-body bg-surface-dark text-body-dark transition-colors duration-300">

  <!-- Reading Progress Bar -->
  <div class="fixed top-0 left-0 right-0 z-[60] h-1 bg-gray-200/50 dark:bg-gray-800/50">
    <div id="reading-progress" class="h-full ai-cta-animate w-0"></div>
  </div>

  <!-- ========== HEADER (simplified) ========== -->
  <header id="main-header" class="fixed top-0 left-0 right-0 z-50 h-16 lg:h-[72px] bg-white/80 dark:bg-surface-dark/80 header-scrolled border-b border-gray-100 dark:border-gray-800 transition-all duration-300">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 h-full flex items-center justify-between">
      <a href="../index.html" class="flex items-center shrink-0">
        <img src="../../images/logo.webp" alt="10XSEO" decoding="async" class="h-auto w-40 lg:w-44 dark:mix-blend-screen" width="600" height="125">
      </a>
      <nav class="hidden lg:flex items-center gap-1" aria-label="Main navigation">
        <a href="../index.html" class="px-3 py-2 text-sm font-medium text-heading dark:text-heading-dark hover:text-primary dark:hover:text-primary-light rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">Home</a>
        <a href="../services.html" class="px-3 py-2 text-sm font-medium text-heading dark:text-heading-dark hover:text-primary dark:hover:text-primary-light rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">Services</a>
        <a href="../ai-seo.html" class="px-3 py-2 text-sm font-medium text-heading dark:text-heading-dark hover:text-primary dark:hover:text-primary-light rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">AI SEO</a>
        <a href="../case-studies.html" class="px-3 py-2 text-sm font-medium text-heading dark:text-heading-dark hover:text-primary dark:hover:text-primary-light rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">Case Studies</a>
        <a href="../about-us.html" class="px-3 py-2 text-sm font-medium text-heading dark:text-heading-dark hover:text-primary dark:hover:text-primary-light rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">About</a>
        <a href="../contact-us.html" class="px-3 py-2 text-sm font-medium text-heading dark:text-heading-dark hover:text-primary dark:hover:text-primary-light rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">Contact</a>
      </nav>
      <div class="flex items-center gap-2">
        <a href="../../index.html" class="hidden sm:flex items-center gap-1 px-2.5 py-1.5 text-xs font-semibold rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800/50 text-heading dark:text-heading-dark transition-colors" hreflang="ka" aria-label="Switch to Georgian">
          <span class="opacity-50">KA</span><span class="opacity-50">/</span><span class="text-primary font-bold">EN</span>
        </a>
        <a href="../contact-us.html" class="hidden lg:inline-flex items-center gap-2 px-5 py-2.5 ai-cta-animate text-white text-sm font-semibold rounded-xl hover:shadow-lg hover:shadow-primary/25 transition-all duration-200">Book Consultation</a>
      </div>
    </div>
  </header>

  <main id="main-content" class="pt-16 lg:pt-[72px]">
    <!-- Hero -->
    <section class="py-12 lg:py-16 bg-gradient-to-br from-primary/5 to-accent/5 dark:from-primary/10 dark:to-accent/10">
      <div class="max-w-4xl mx-auto px-4 sm:px-6">
        <nav class="flex items-center gap-2 text-sm text-body/70 dark:text-body-dark/70 mb-6">
          <a href="../index.html" class="hover:text-primary transition-colors">Home</a>
          <span>›</span>
          <span class="text-heading dark:text-heading-dark font-medium">Blog</span>
          <span>›</span>
          <span class="text-heading dark:text-heading-dark font-medium">{article['h1'][:40]}…</span>
        </nav>
        <h1 class="font-heading text-3xl sm:text-4xl lg:text-5xl font-extrabold text-heading dark:text-heading-dark !leading-tight mb-6">{article['h1']}</h1>
        <div class="flex items-center gap-4 text-sm text-body/80 dark:text-body-dark/80">
          <span>📅 {article['published']}</span>
          <span>•</span>
          <span>⏱ {article['reading_minutes']} min read</span>
        </div>
      </div>
    </section>

    <!-- Article body + sidebar -->
    <section class="py-12 lg:py-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 grid lg:grid-cols-[1fr_280px] gap-12">
        <article>
          <img src="{image_path}" alt="{article['image_alt']}" class="w-full rounded-2xl mb-10" width="1200" height="630">

          <div class="prose text-body dark:text-body-dark">
            {intro_html}

            {sections_top}
          </div>

          <!-- Inline CTA -->
          <div class="my-10 p-6 lg:p-8 bg-gradient-to-r from-primary/5 to-accent/5 dark:from-primary/10 dark:to-accent/10 rounded-2xl border border-primary/10 dark:border-primary/20">
            <div class="flex flex-col sm:flex-row items-start sm:items-center gap-4">
              <div class="flex-1">
                <p class="font-heading font-bold text-heading dark:text-heading-dark mb-1">Wondering about your AI search visibility?</p>
                <p class="text-sm text-body dark:text-body-dark">Get a free 72-hour audit — we'll show you which AI engines are citing your competitors and where the gaps are.</p>
              </div>
              <a href="../seo-audit.html" class="inline-flex items-center gap-2 px-6 py-3 bg-primary text-white text-sm font-bold rounded-xl hover:shadow-lg hover:shadow-primary/25 transition-all whitespace-nowrap shrink-0">
                Free Audit
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"/></svg>
              </a>
            </div>
          </div>

          <div class="prose text-body dark:text-body-dark">
            {sections_bottom}

            {faq_html}
          </div>

          <!-- End CTA -->
          <div class="mt-12 p-8 lg:p-10 ai-cta-animate rounded-2xl text-center">
            <h3 class="font-heading text-2xl font-extrabold text-white mb-3">Ready to win in AI search?</h3>
            <p class="text-white/80 mb-6 max-w-lg mx-auto">Talk to 10xSEO about your AEO + SEO strategy. Free 15-minute consultation.</p>
            <a href="../contact-us.html" class="inline-flex items-center gap-2 px-8 py-4 bg-white text-primary text-lg font-bold rounded-2xl hover:shadow-xl hover:-translate-y-0.5 transition-all duration-200">
              Book Free Consultation
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"/></svg>
            </a>
          </div>

          <!-- Related Articles -->
          <div class="mt-16">
            <h3 class="font-heading text-xl font-bold text-heading dark:text-heading-dark mb-6">Related Articles</h3>
            <div class="grid sm:grid-cols-3 gap-4">
              {related_html}
            </div>
          </div>
        </article>

        <!-- Sidebar -->
        <aside class="hidden lg:block">
          <div class="sticky top-24">
            <div class="bg-surface-alt dark:bg-surface-dark-alt rounded-2xl p-5 border border-gray-100 dark:border-gray-800 mb-6">
              <p class="font-heading font-bold text-heading dark:text-heading-dark text-sm mb-4">Table of Contents</p>
              <nav class="space-y-2">
                {toc_html}
              </nav>
            </div>
            <div class="bg-gradient-to-br from-primary/5 to-accent/5 dark:from-primary/10 dark:to-accent/10 rounded-2xl p-5 border border-primary/10 dark:border-primary/20">
              <p class="font-heading font-bold text-heading dark:text-heading-dark text-sm mb-2">Free SEO Audit</p>
              <p class="text-xs text-body dark:text-body-dark mb-4">See what's missing on your site within 72 hours.</p>
              <a href="../seo-audit.html" class="block text-center px-4 py-2.5 bg-primary text-white text-sm font-bold rounded-xl hover:shadow-lg hover:shadow-primary/25 transition-all">Get Free Audit</a>
            </div>
          </div>
        </aside>
      </div>
    </section>
  </main>

  <!-- ========== FOOTER (minimal) ========== -->
  <footer class="bg-heading dark:bg-surface-dark-alt text-gray-400 py-12 lg:py-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6">
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
        <div>
          <p class="font-heading text-white font-semibold text-sm uppercase tracking-wider mb-4">Services</p>
          <ul class="space-y-2 text-sm">
            <li><a href="../seo-management.html" class="hover:text-white transition-colors">SEO Management</a></li>
            <li><a href="../seo-consultation.html" class="hover:text-white transition-colors">SEO Consultation</a></li>
            <li><a href="../ai-seo.html" class="hover:text-white transition-colors">AI SEO (GEO/AEO)</a></li>
            <li><a href="../seo-audit.html" class="hover:text-white transition-colors">Free SEO Audit</a></li>
          </ul>
        </div>
        <div>
          <p class="font-heading text-white font-semibold text-sm uppercase tracking-wider mb-4">Company</p>
          <ul class="space-y-2 text-sm">
            <li><a href="../about-us.html" class="hover:text-white transition-colors">About Us</a></li>
            <li><a href="../portfolio.html" class="hover:text-white transition-colors">Portfolio</a></li>
            <li><a href="../case-studies.html" class="hover:text-white transition-colors">Case Studies</a></li>
            <li><a href="../contact-us.html" class="hover:text-white transition-colors">Contact</a></li>
          </ul>
        </div>
        <div>
          <p class="font-heading text-white font-semibold text-sm uppercase tracking-wider mb-4">Industries</p>
          <ul class="space-y-2 text-sm">
            <li><a href="../industries/construction.html" class="hover:text-white transition-colors">Construction &amp; Real Estate</a></li>
            <li><a href="../industries/healthcare.html" class="hover:text-white transition-colors">Healthcare</a></li>
            <li><a href="../industries/financial-services.html" class="hover:text-white transition-colors">Financial Services</a></li>
            <li><a href="../industries/ecommerce.html" class="hover:text-white transition-colors">E-commerce</a></li>
          </ul>
        </div>
        <div>
          <p class="font-heading text-white font-semibold text-sm uppercase tracking-wider mb-4">Contact</p>
          <ul class="space-y-2 text-sm">
            <li><a href="tel:+995510101517" class="hover:text-white transition-colors">+995 510 10 15 17</a></li>
            <li><a href="mailto:sales@10xseo.ge" class="hover:text-white transition-colors">sales@10xseo.ge</a></li>
            <li>8 Bakhtrioni Street, Tbilisi 0194, Georgia</li>
          </ul>
        </div>
      </div>
      <div class="border-t border-white/10 pt-8 flex items-center justify-center gap-3">
        <a href="../index.html"><img src="../../images/logo-sm.webp" alt="10XSEO" loading="lazy" decoding="async" width="600" height="125" class="h-8 w-auto"></a>
        <p class="text-xs text-gray-300">Georgia's #1 SEO Agency. &copy; 2026 All rights reserved.</p>
      </div>
    </div>
  </footer>

  <!-- Reading progress JS -->
  <script>
    document.addEventListener('scroll', () => {{
      const h = document.documentElement;
      const scrolled = (h.scrollTop / (h.scrollHeight - h.clientHeight)) * 100;
      const bar = document.getElementById('reading-progress');
      if (bar) bar.style.width = scrolled + '%';
    }});
    // TOC active link
    const tocLinks = document.querySelectorAll('.toc-link');
    const obs = new IntersectionObserver((entries) => {{
      entries.forEach(e => {{
        if (e.isIntersecting) {{
          tocLinks.forEach(l => l.classList.toggle('active', l.getAttribute('href') === '#' + e.target.id));
        }}
      }});
    }}, {{ rootMargin: '-30% 0px -60% 0px' }});
    document.querySelectorAll('h2[id], h3[id]').forEach(h => obs.observe(h));
  </script>
</body>
</html>
"""

    out_path = OUT_DIR / f"{slug}.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"✓ Wrote {out_path.relative_to(ROOT)} ({len(html)} bytes)")


if __name__ == "__main__":
    build_article(ARTICLE_1)
    build_article(ARTICLE_2)
    print(f"\nDone. {len(list(OUT_DIR.glob('*.html')))} files in {OUT_DIR.relative_to(ROOT)}/")
