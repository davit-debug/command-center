# 🚀 10xseo.ge Cutover — 10-Point Testing Plan

> **Strategy:** Subdomain (`new.10xseo.ge`) ALREADY VALIDATED ✅ — 90/91 automated tests pass.
> This plan is for the **production cutover** (DNS flip 10xseo.ge → Cloudways).

**Status at plan creation:**
- ✅ Cloudways app `10xseo` deployed (157.245.32.108, app folder `mnxbbjxncp`)
- ✅ DNS `new.10xseo.ge` → Cloudflare → Cloudways tested and working
- ✅ SSL Let's Encrypt installed for `new.10xseo.ge` (valid until Aug 12, 2026)
- ✅ ~100 redirect rules verified on `new.10xseo.ge`
- ⏳ Pending: 10xseo.ge DNS A record (currently → WordPress)

---

## 📐 STRUCTURE

```
PHASE 1 (T-24h):     Pre-flight prep              — points 1-2
PHASE 2 (T-0):        Cutover                      — points 3-4
PHASE 3 (T+5 min):    Immediate verification       — points 5-7
PHASE 4 (T+1h):       Stability check              — points 8-9
PHASE 5 (T+24h/72h):  Search Console monitoring    — point 10
```

---

## ☝️ POINT 1 — Pre-Flight Capture (T-24h, 5 min)

**Goal:** Capture rollback values BEFORE making any changes.

```bash
# Run these on your terminal:
echo "OLD WP IP (rollback target):"
dig 10xseo.ge +short
# Save this number! → ________________

echo "OLD WP TTL (verify current):"
dig 10xseo.ge | grep -A1 'ANSWER SECTION' | tail -1

echo "Current robots.txt (verify WP version):"
curl -s https://10xseo.ge/robots.txt | head -10
```

**Save to safe place:**
- Old WP IP: `____________________`
- Old WP host control panel URL: `____________________`
- WP admin credentials: ☐ in password manager
- Cloudways server IP: `157.245.32.108` (already known)
- Cloudways app folder: `mnxbbjxncp`

**Fail trigger:** Can't reach WP admin or backup → DELAY cutover.

---

## ✌️ POINT 2 — DNS TTL + WordPress Backup (T-24h, 30 min)

**Goal:** Make rollback fast + preserve WP data.

### 2a. Lower TTL at registrar (24h before flip)
- Login to your registrar (where 10xseo.ge is registered)
- DNS settings → A record for 10xseo.ge
- Change **TTL: 300 seconds** (5 min)
- Wait 24 hours for global propagation of low TTL

### 2b. WordPress backup
- Login to current WP hosting control panel
- Take **full backup**: Database + files
- Download backup file locally → store in `~/Backups/10xseo-pre-cutover-YYYY-MM-DD.zip`
- Verify backup file > 0 bytes ✓

**Fail trigger:** Backup fails → DELAY cutover, fix backup first.

---

## 👌 POINT 3 — Add 10xseo.ge to Cloudways Domain Mgmt (T-0, 2 min)

**🔴 CRITICAL — this MUST happen BEFORE DNS flip.**

Verified via dry-run: without this step, requests to `10xseo.ge` hit a **default WP vhost** on the shared Cloudways server (NOT our site).

```
Cloudways → Apps → 10xseo → Domain Management → + Add Domain:
   Domain: 10xseo.ge
   Save

   Domain: www.10xseo.ge
   Save

   (do NOT set Primary yet)
```

**Verify (Domain List should show):**
- `phpstack-1272771-6417221.cloudwaysapps.com` (Primary)
- `new.10xseo.ge` (Alias) — already there
- `10xseo.ge` (Alias) — NEW
- `www.10xseo.ge` (Alias) — NEW

**Fail trigger:** Add fails → STOP, troubleshoot before DNS.

---

## 🖖 POINT 4 — DNS Flip at Registrar (T-0, 2 min)

```
Registrar → DNS → A record for 10xseo.ge:
   Old value:  [WP IP from Point 1]
   New value:  157.245.32.108
   TTL:        300 (still low from Point 2)
   Save

Add or update A record for www.10xseo.ge:
   Value:      157.245.32.108
   (or CNAME www → 10xseo.ge if registrar prefers)
```

**Watch DNS propagation:**
```bash
# Re-run every 30 seconds for 5-15 minutes:
dig @8.8.8.8 10xseo.ge +short
dig @1.1.1.1 10xseo.ge +short
# When BOTH return 157.245.32.108 → continue to Point 5
```

**Fail trigger:** DNS doesn't propagate after 30 min → check registrar.

---

## 🤚 POINT 5 — SSL Generation (T+~5 min, 1-2 min)

**Only run after DNS propagates** (HTTP-01 challenge needs DNS).

```
Cloudways → 10xseo app → SSL Certificate:
   Let's Encrypt tab
   Add Domain → 10xseo.ge
   Add Domain → www.10xseo.ge
   Save Changes
```

⏱ 30-60 sec for Let's Encrypt to validate + install.

**Verify:**
```bash
echo | openssl s_client -connect 10xseo.ge:443 -servername 10xseo.ge 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates | head -5
# subject= should contain: CN=10xseo.ge
# issuer= should contain: Let's Encrypt
```

**Fail trigger:** SSL gen fails → DNS not yet propagated globally. Wait 5 more min, retry.

---

## 🤞 POINT 6 — Smoke Test Top 10 URLs (T+~7 min, 2 min)

```bash
# Quick smoke test — run on terminal:
BASE="https://10xseo.ge"
PASS=0; FAIL=0
for url in "/" "/ra-aris-seo/" "/seo-management/" "/seo-saagento/" \
           "/best-seo-agency-in-georgia/" "/blog/" "/case-studies/" \
           "/about-us/" "/contact-us/" "/en/"; do
  code=$(curl -sIo /dev/null -w "%{http_code}" --max-time 8 "$BASE$url")
  case "$code" in
    200|301|302) echo "✓ $code $url"; PASS=$((PASS+1)) ;;
    *)           echo "✗ $code $url"; FAIL=$((FAIL+1)) ;;
  esac
done
echo "RESULT: $PASS / $((PASS+FAIL))"
```

**Pass criteria:** 10/10 return 200 or 301. Any 4xx/5xx = investigate before continuing.

**Fail trigger:** Any 500 / 502 / 503 / 5xx → **ROLLBACK** (see Point 11 below).

---

## ✋ POINT 7 — Full Verify-Cutover Script (T+~10 min, 2 min)

```bash
cd /Users/imac/SEO/command-center
bash _cloudways/verify-cutover.sh https://10xseo.ge
```

**Expected:** 30+ PASS, 0 FAIL.

Tests covered:
- DNS propagation across 3 resolvers
- HTTPS + canonical host
- robots.txt sanity
- Top 15 redirects (GSC-validated)
- Backlink-bearing URLs preservation
- Sitemap + 404
- Top 20 URLs — no 5xx
- Cache + compression + security headers
- Mixed content scan

**Fail trigger:** Any FAIL in robots, sitemap, top URLs, or mixed content → fix or rollback.

---

## 🖐 POINT 8 — Manual Browser Test (T+~15 min, 15 min)

**Open in Chrome Incognito** (no cache):

| Test | URL | Expected |
|---|---|---|
| Homepage | `https://10xseo.ge/` | Hex animation runs, "AI ეპოქის SEO სააგენტო" hero |
| Logo links home | Click logo from any page | → `https://10xseo.ge/` |
| Mobile menu | Resize to 375px → click ☰ | Menu opens, nav items work |
| Header nav | Click each top-level link | All resolve, no 404 |
| Footer | Email `davit@10xseo.ge` clickable? | mailto: opens |
| Critical redirect | `/ra-aris-seo/` typed in URL bar | 301 → dual-intent page |
| Top GSC keyword | `/seo-saagento/` | 301 → blog post |
| Old case study slug | `/case-studies/seo-krizisidan-top-3mde/` | 301 → seo-crisis-management |
| 410 Gone visual | `/web-development/` | Browser shows error (NOT 404) |
| Custom 404 | `/random-xyz/` | Branded 404 page |
| Tally form | Open `/contact-us.html` → submit test | Form submits, no broken iframe |
| YouTube | Open `/ai-seo.html` → scroll to video | Video iframe loads |
| Calendly | Open page with Calendly | Calendar renders, no "event not found" |
| EN switcher | Click EN flag from homepage | → `/en/` |
| HSTS NOT YET on | DevTools → Network → check headers | NO `Strict-Transport-Security` (still commented) |

**Fail trigger:** Any major visual/UX issue → diagnose. Forms broken = blocker.

---

## ✊ POINT 9 — PageSpeed Insights (T+~30 min, 5 min)

```
Open: https://pagespeed.web.dev/

Test 1: https://10xseo.ge/ (homepage)
   Mobile target: ≥ 80
   Desktop target: ≥ 90

Test 2: https://10xseo.ge/seo-management.html (top service)
   Mobile target: ≥ 75
   Desktop target: ≥ 85

Test 3: https://10xseo.ge/blog.html
   Mobile target: ≥ 80
   Desktop target: ≥ 90
```

**Compare with GitHub Pages staging scores** (you saved these pre-launch).

**Fail trigger:** Significant regression (>10 points lower) → investigate Cloudways perf settings.

---

## 🤙 POINT 10 — Search Console + Post-Launch Tasks (T+~45 min)

### 10a. Submit new sitemap
```
Google Search Console → Sitemaps → Add new sitemap:
   https://10xseo.ge/sitemap.xml
```

### 10b. URL Inspection — Request indexing on top 10
- Open URL Inspection tool in GSC
- Test these 10 URLs one by one → "Request Indexing":
  - https://10xseo.ge/
  - https://10xseo.ge/seo-management.html
  - https://10xseo.ge/ra-aris-seo.html ← top traffic
  - https://10xseo.ge/blog.html
  - https://10xseo.ge/case-studies.html
  - https://10xseo.ge/blog/best-seo-agency-in-georgia.html
  - https://10xseo.ge/blog/seo-saagento.html
  - https://10xseo.ge/seo-audit.html
  - https://10xseo.ge/about-us.html
  - https://10xseo.ge/contact-us.html

### 10c. Enable HSTS (only after SSL confirmed working)
```bash
# In _cloudways/.htaccess, uncomment the HSTS line:
# Find this:
#    # Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
# Change to:
#    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"

cd /Users/imac/SEO/command-center
# Edit _cloudways/.htaccess (Cursor/VS Code or vim)
git add _cloudways/.htaccess
git commit -m "Enable HSTS after SSL confirmed working on 10xseo.ge"
git push
# Auto-deploys in ~30 sec
```

### 10d. Cloudways Varnish purge (clean slate post-cutover)
```
Cloudways → Server Management → Manage Services → Varnish → Purge
```

### 10e. Monitor for 72 hours:
- **Day 1, 8 AM:** GSC → Coverage → any new 404s?
- **Day 1, 8 PM:** GSC → Performance → impressions on top keywords stable?
- **Day 2:** Re-run `verify-cutover.sh` → still all PASS?
- **Day 3:** GSC → "Crawled - currently not indexed" — should be dropping from 75
- **Day 7:** GSC → review "Indexed but not in sitemap" — add any to sitemap

**Fail trigger:** Impressions drop > 30% on top keywords by Day 3 → investigate (likely indexing lag, not fundamental issue).

---

## 🆘 ROLLBACK Procedure (≤ 5 minutes)

**Triggers (any one):**
- Homepage returns 5xx after 5 min stable
- Critical redirect breaks (`/ra-aris-seo/` returns 404)
- SSL fails AND can't be fixed within 30 min
- 20+ new 404s in GSC within 1 hour
- Forms broken → leads dropping

**Steps:**
1. Registrar → DNS → A record for 10xseo.ge:
   - Change back to **OLD WP IP** (from Point 1)
2. Verify rollback: `dig 10xseo.ge +short` returns OLD IP
3. Wait 5 min for propagation
4. Verify: `curl -sI https://10xseo.ge/` shows WP again
5. Notify team: "Rollback complete at HH:MM. Investigation TBD."

**Don't:**
- ✗ Delete Cloudways app — preserve for diagnosis
- ✗ Delete WP files — they're your fallback
- ✗ Force disable SSL

---

## 📊 Success Criteria — All Must Pass

| # | Check | Pass = |
|---|---|---|
| 1 | DNS propagated globally | 3 resolvers return 157.245.32.108 |
| 2 | SSL valid | `curl https://10xseo.ge/` no -k needed |
| 3 | Homepage loads | 200 OK + hex animation |
| 4 | Top 10 redirects | 10/10 return 301 to correct .html |
| 5 | verify-cutover.sh | 30+ PASS, 0 FAIL |
| 6 | Manual browser | All flows OK incl. forms |
| 7 | PSI mobile | ≥ 80 on homepage |
| 8 | GSC sitemap | Submitted, processed within 24h |
| 9 | 24h monitor | < 5 new 404s |
| 10 | 72h monitor | Impressions stable ±10% |

---

## 📞 Emergency Contacts (fill in)

| Role | Contact |
|---|---|
| Domain registrar support | _____________________ |
| Cloudways support (chat) | https://platform.cloudways.com/ → chat |
| Cloudflare support | https://dash.cloudflare.com/ → Help |
| Old WP hosting support | _____________________ |
| You (mobile) | +995 510 10 15 17 |

---

## 🎯 Recommended Cutover Window

- **Day:** Tuesday-Thursday (avoid Friday — weekend support thin)
- **Time:** **10:00 AM Tbilisi** (UTC+4) — low traffic, fresh team
- **Duration:** Block 2 hours uninterrupted
- **Pre-flight (Point 1-2):** Day before, ~6 PM
- **Cutover (Point 3-7):** ~15 minutes
- **Post-launch (Point 8-10a):** ~45 minutes
- **Monitoring (Point 10b-e):** ongoing, light touches
