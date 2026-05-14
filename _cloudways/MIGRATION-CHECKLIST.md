# Cloudways Migration Checklist — 10xseo.ge

**Source:** Static HTML site at `command-center/` (this repo) → currently on GitHub Pages staging
**Target:** Cloudways managed hosting → replaces existing WordPress on `10xseo.ge`
**Strategy:** Parallel test on Cloudways temp URL first → flip DNS only after green

---

## A. Files prepared (this session)

| File | Where it lives now | Where it goes on Cloudways |
|---|---|---|
| `_cloudways/.htaccess` | repo root | site root (`public_html/.htaccess`) |
| `_cloudways/robots.txt` | repo root | site root (`public_html/robots.txt`) |
| `_cloudways/cloudways-deploy.yml` | repo root | `.github/workflows/cloudways-deploy.yml` |
| `_cloudways/REDIRECT-MAP.csv` | repo root | reference only (audit doc) |

The deploy workflow auto-promotes `_cloudways/.htaccess` and `_cloudways/robots.txt` to the site root before rsync, so the staging GitHub Pages site never gets the production robots.

---

## B. Cloudways setup (manual — outside Claude's scope)

1. **Sign up & launch app**
   - Server: choose a provider/region close to GE (Vultr Frankfurt, DO Frankfurt, AWS eu-central-1)
   - Server size: 1 GB RAM is enough for a 70 MB static site (start small, scale up later)
   - Application: **PHP 8.x stack** (use this even though we have no PHP — we just need the Apache+Nginx web server)
   - Application name: `10xseo`

2. **SSH key setup** (for the deploy workflow)
   - Generate locally: `ssh-keygen -t ed25519 -f ~/.ssh/cloudways_10xseo -N ""`
   - Cloudways Console → Server → Master Credentials → SSH Public Keys → paste `.pub`
   - GitHub repo → Settings → Secrets → Actions → add 4 secrets:
     - `CLOUDWAYS_SSH_HOST` (server IP from Cloudways)
     - `CLOUDWAYS_SSH_USER` (Application's SSH user, format: `master_xxxxxxxx`)
     - `CLOUDWAYS_SSH_KEY` (the **private** key content — full file)
     - `CLOUDWAYS_REMOTE_PATH` (e.g. `/home/master/applications/abcdefgh/public_html`)

3. **First deploy via temp URL**
   - Cloudways gives every app a temp URL like `https://wordpress-XXXXXX-XXXXXX.cloudwaysapps.com`
   - Move the workflow into place: `mv _cloudways/cloudways-deploy.yml .github/workflows/`
   - Push to `main` → GitHub Actions runs rsync → site lives at the temp URL
   - In your browser, override DNS via `/etc/hosts` so `10xseo.ge` points to the new server IP — that lets you click around the new site as if it were live.

---

## C. Pre-cutover testing checklist

### On the Cloudways temp URL:
- [ ] Homepage loads, hex animation works
- [ ] All header / footer links work (no `.html` extension shown to user but correct page loads)
- [ ] `/seo-management/` 301-redirects to `/seo-management.html`
- [ ] `/case-studies/270-percent-increase/` 301-redirects to `/case-studies/270-percent-increase.html`
- [ ] `/blog/` works as `/blog.html`
- [ ] An old WP blog URL like `/2024-seo-trendebi/` 301-redirects to `/blog/2024-seo-trendebi.html`
- [ ] EN version: `/en/seo-management/` redirects to `/en/seo-management.html`
- [ ] 404 page renders the custom `404.html` (try `/this-does-not-exist`)
- [ ] HTTPS works (Cloudways auto Let's Encrypt — see step D)
- [ ] `https://www.10xseo.ge/` redirects to `https://10xseo.ge/`
- [ ] All form submissions still go to Tally / external form tool (no native forms broke)
- [ ] All YouTube embeds, Calendly, etc. third-party widgets still load
- [ ] Mobile menu works
- [ ] Sitemap loads at `/sitemap.xml` — 120 URLs visible
- [ ] `robots.txt` allows indexing (NOT the staging `Disallow: /` version)

### Performance:
- [ ] PageSpeed Insights — homepage scores ≥ 85 mobile, ≥ 95 desktop
- [ ] Largest assets (videos in `videos/why-us/`) lazy-load
- [ ] Brotli or gzip is active (DevTools → Network → check `Content-Encoding`)

### SEO:
- [ ] Run `audit/` Playwright suite against the temp URL → no regressions
- [ ] Search Console → URL Inspection on 5 representative URLs against the temp URL → all "URL is on Google" friendly markup parses

---

## D. Cutover (DNS flip) — STRICT ORDER REQUIRED

> ⚠️ **Verified via dry-run (2026-05-14):** Without step 4, requests to `10xseo.ge`
> on Cloudways IP `157.245.32.108` hit the server's **default vhost (a different WP app)**
> instead of our static site. **Step 4 MUST happen BEFORE step 6.**

**Pre-flight (24h before):**
1. **Backup current WordPress** — Cloudways or hosting provider, full backup (DB + files). Keep for ≥ 30 days.
2. **Lower DNS TTL** at registrar 24 h before cutover: set A record TTL to 300 s (5 min). This makes rollback fast if needed.
3. **Verify** the new site one more time at the temp URL.

**Day of cutover (strict order):**
4. **🔴 FIRST: Cloudways → Apps → 10xseo → Domain Management** — add `10xseo.ge` (Primary) + `www.10xseo.ge` (alias). **WITHOUT THIS, traffic goes to a default vhost.**
5. **DNS at registrar** — change `A` record for `10xseo.ge` to `157.245.32.108`. Also `A` for `www` (or CNAME www → 10xseo.ge).
6. **Wait 5–60 min** for DNS propagation. Monitor: `dig 10xseo.ge +short` (should return `157.245.32.108`).
7. **Cloudways → SSL Certificate** — generate Let's Encrypt for `10xseo.ge` AND `www.10xseo.ge`. Requires step 5 + 6 first (HTTP-01 challenge needs DNS).
8. **Verify SSL** — open `https://10xseo.ge/` in Incognito → no cert warning.
9. **Cloudways → Manage Services → Varnish → Purge** — clear stale cache from temp-URL period.
10. **After SSL works on every URL**, uncomment HSTS line in `_cloudways/.htaccess` and push.
11. Cold test: Incognito + 5 deep URLs (`/`, `/seo-management.html`, `/blog.html`, `/case-studies.html`, `/en/`).
12. **Search Console** → Sitemaps → Submit `https://10xseo.ge/sitemap.xml`.
13. URL Inspection on top 10 pages → "Request Indexing".

**Post-cutover monitoring (first 7 days):**
- Daily: Search Console → Coverage report — watch for crawl errors or 404 spikes.
- Daily: GSC → Performance — watch impressions for sudden drops on top keywords (esp. "SEO სააგენტო", "SEO სტრატეგია").
- Day 3 + 7: re-run PSI on top 10 pages.
- Week 2: review GSC "Indexed but not in sitemap" + "Crawled - currently not indexed" — may need extra 301s.

---

## E. Rollback runbook (if it goes sideways)

**Before cutover — capture these values:**
- [ ] OLD WP A record IP (run: `dig 10xseo.ge +short` BEFORE flipping DNS) → ________________
- [ ] Old WP control panel URL: ________________
- [ ] Old WP admin credentials saved in password manager: ☐

**Rollback triggers (any of these = revert):**
- Homepage returns 5xx or wrong content > 5 min after DNS propagation
- Critical redirect (e.g., `/ra-aris-seo/` — 81 clicks/mo) returns 404 or wrong destination
- SSL cert error visible in Chrome incognito (and Cloudways SSL generation fails)
- Search Console shows 20+ new 404 errors within first hour
- Forms (Tally embeds) broken → contact / leads dropping

**Rollback procedure (≤ 5 minutes end-to-end):**
1. Registrar DNS → change A record back to OLD WP IP (recorded above)
2. With TTL=300s, propagation = ~5 min globally
3. Verify: `dig 10xseo.ge +short` from your machine returns OLD IP
4. Verify: Open `https://10xseo.ge/` in incognito → WP loads
5. Notify team: rollback completed at [time]; post-mortem TBD

**Don't panic-do:**
- ✗ Don't delete the 10xseo Cloudways app — preserve it for diagnosis
- ✗ Don't delete WP files/DB — those are your fallback
- ✗ Don't disable Cloudflare/SSL — let them re-converge

**Post-rollback:**
- Cloudways app stays deployed (free — paid per-server, not per-app)
- Investigate root cause via Cloudways logs: `ssh master_qqcfjajpxj@157.245.32.108 'tail -100 ~/applications/mnxbbjxncp/logs/*.log'`
- Fix → push → temp URL test → retry cutover when ready

---

## F. After cutover (clean-up)

- [ ] Disable / pause the old GitHub Pages workflow (`pages.yml` and `deploy.yml`) — they keep building but no one's using them. Or delete them.
- [ ] Update `CNAME` in repo if it exists (it doesn't currently) — or remove from GH Pages settings.
- [ ] Delete `_cloudways/` from repo if you want, OR keep as a reference doc (recommended).
- [ ] Remove old WordPress hosting after 30 days confidence period.
- [ ] Cancel old WP hosting subscription.

---

## G-pre. GSC baseline (pulled 2026-05-13, last 90 days)

| Metric | Value |
|---|---|
| Total clicks | 585 |
| Total impressions | 17,500 |
| Average CTR | 3.3% |
| Average position | 6.8 |
| Indexed pages | 123 |
| Not indexed | 115 (5 reasons) |
| Submitted sitemaps | **0** (must submit `/sitemap.xml` post-launch) |
| Mobile CWV | latest 0/0/0 (insufficient CrUX data on individual URLs) |
| Desktop CWV | 43 good URLs, 0 issues |

**Top query → URL mappings to preserve** (verified via GSC):
- "10x georgia" / "10xgeorgia" / "10xseo" (215 clicks combined) → homepage ✓
- "seo სააგენტო" + "სეო სააგენტო" (54 clicks) → homepage (after `/seo-saagento/` redirect)
- "seo ოპტიმიზაცია" (28 clicks) → `/seo-management.html` (after `/seo-optimizacia/` redirect)
- "seo მომსახურება" (16 clicks) → `/seo-management.html` directly
- "რა არის სეო" (7 clicks) → `/ra-aris-seo.html` (top-level dual-intent)

**Indexing health issues to monitor post-migration:**
- 75 "Crawled - currently not indexed" pages grew 15× in last 3 months on WP. New static site has thinner, higher-quality content — should drop dramatically.
- 15 "Not found (404)" pages — mostly WP bot probes (wp-admin, wp-content/plugins) — will stay 404 on Cloudways. Fine.

## G. KNOWN GAPS — review before cutover

These pages exist on **WordPress** but have **no equivalent** on the new static site. The `.htaccess` ships with my best-guess 301s — confirm they're acceptable or override:

| Old WP URL | Current 301 target | Better target? |
|---|---|---|
| `/link-building/` | `/seo-management.html` | build a dedicated link-building.html? |
| `/web-development/` | `/services.html` | drop entirely (410)? |
| `/get-an-offer/` | `/contact-us.html` | keep as is — there's no dedicated offer page on CC |
| `/website-info/*` (×13 sub-pages) | `/portfolio.html` | check GSC: do any of these still get traffic? If yes, build them; if no, OK to redirect |
| `/seo-saagento/` | `/blog/seo-saagento.html` | could redirect to `/` (homepage targets the same keyword "SEO სააგენტო" 8x) |
| `/ra-aris-seo/` | `/blog/ra-aris-seo.html` | CC has BOTH a service page (`/ra-aris-seo.html`) and a blog post — the WP version was a blog post; current map preserves that semantic |
| `/copywriting/` | `/blog/copywriting.html` | WP `/copywriting/` was a blog post (not the service); confirmed |

**Recommendation:** before cutover, pull the last 90 days of GSC data for these URLs. If any have meaningful traffic (>10 clicks/mo), reconsider the redirect target.
