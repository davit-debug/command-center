#!/usr/bin/env bash
# =============================================================================
# verify-cutover.sh — Phase 1 post-cutover verification for 10xseo.ge
# Run immediately after DNS flip. Aim: catch catastrophes in < 2 minutes.
#
# Usage:   bash _cloudways/verify-cutover.sh
#          bash _cloudways/verify-cutover.sh https://temp.cloudwaysapps.com   # test temp URL pre-cutover
# =============================================================================

set -u

BASE_URL="${1:-https://10xseo.ge}"
EXPECTED_HOST="$(echo "$BASE_URL" | sed -E 's|https?://||; s|/.*||')"

# Colors
RED=$'\033[31m'; GREEN=$'\033[32m'; YELLOW=$'\033[33m'; BOLD=$'\033[1m'; NC=$'\033[0m'

PASS=0
FAIL=0
WARN=0

pass() { echo "${GREEN}✓ PASS${NC}  $1"; PASS=$((PASS+1)); }
fail() { echo "${RED}✗ FAIL${NC}  $1"; FAIL=$((FAIL+1)); }
warn() { echo "${YELLOW}! WARN${NC}  $1"; WARN=$((WARN+1)); }
info() { echo "${BOLD}»${NC} $1"; }
hr()   { echo "${BOLD}────────────────────────────────────────────────────────────────${NC}"; }

# Tiny helper: hit URL, return "STATUS_CODE|LOCATION_HEADER"
hit() {
  curl -sk -o /dev/null -w "%{http_code}|%{redirect_url}" --max-time 10 "$1"
}

# Tiny helper: full curl headers
headers() {
  curl -skI --max-time 10 "$1"
}

echo
echo "${BOLD}10xseo.ge cutover verification — $(date '+%Y-%m-%d %H:%M:%S')${NC}"
echo "Target: $BASE_URL"
hr

# -----------------------------------------------------------------------------
# 1. DNS propagation
# -----------------------------------------------------------------------------
info "1. DNS propagation"
if [ "$EXPECTED_HOST" = "10xseo.ge" ]; then
  GOOG=$(dig +short +time=3 "$EXPECTED_HOST" @8.8.8.8 | head -1)
  CFLR=$(dig +short +time=3 "$EXPECTED_HOST" @1.1.1.1 | head -1)
  ODNS=$(dig +short +time=3 "$EXPECTED_HOST" @208.67.222.222 | head -1)
  echo "   Google 8.8.8.8     → ${GOOG:-no answer}"
  echo "   Cloudflare 1.1.1.1 → ${CFLR:-no answer}"
  echo "   OpenDNS            → ${ODNS:-no answer}"
  if [ -n "$GOOG" ] && [ "$GOOG" = "$CFLR" ] && [ "$CFLR" = "$ODNS" ]; then
    pass "DNS converged across all 3 resolvers ($GOOG)"
  elif [ -n "$GOOG" ] && [ -n "$CFLR" ] && [ -n "$ODNS" ]; then
    warn "DNS resolves but values differ — propagation in progress"
  else
    fail "DNS not resolving on at least one resolver"
  fi
else
  warn "Skipping DNS check (testing temp URL: $EXPECTED_HOST)"
fi

# -----------------------------------------------------------------------------
# 2. HTTPS + canonical host (only meaningful on real domain)
# -----------------------------------------------------------------------------
hr
info "2. HTTPS + canonical host"
if [ "$EXPECTED_HOST" = "10xseo.ge" ]; then
  HTTP_RES=$(hit "http://10xseo.ge/")
  HTTP_CODE="${HTTP_RES%%|*}"
  HTTP_LOC="${HTTP_RES##*|}"
  if [ "$HTTP_CODE" = "301" ] && echo "$HTTP_LOC" | grep -q "^https://"; then
    pass "http://10xseo.ge/ → 301 to $HTTP_LOC"
  else
    fail "http://10xseo.ge/ returned $HTTP_CODE (expected 301 to https)"
  fi

  WWW_RES=$(hit "https://www.10xseo.ge/")
  WWW_CODE="${WWW_RES%%|*}"
  WWW_LOC="${WWW_RES##*|}"
  if [ "$WWW_CODE" = "301" ] && echo "$WWW_LOC" | grep -q "^https://10xseo.ge/"; then
    pass "https://www.10xseo.ge/ → 301 to apex"
  elif [ "$WWW_CODE" = "000" ]; then
    fail "https://www.10xseo.ge/ — TLS handshake failed (SSL not issued for www)"
  else
    fail "https://www.10xseo.ge/ returned $WWW_CODE → $WWW_LOC (expected 301 to apex)"
  fi
fi

APEX_RES=$(hit "$BASE_URL/")
APEX_CODE="${APEX_RES%%|*}"
if [ "$APEX_CODE" = "200" ]; then
  pass "$BASE_URL/ → 200"
elif [ "$APEX_CODE" = "000" ]; then
  fail "$BASE_URL/ — TLS / connection error"
else
  fail "$BASE_URL/ returned $APEX_CODE (expected 200)"
fi

# -----------------------------------------------------------------------------
# 3. robots.txt — indexing allowed?
# -----------------------------------------------------------------------------
hr
info "3. robots.txt sanity"
ROBOTS=$(curl -sk --max-time 10 "$BASE_URL/robots.txt")
if echo "$ROBOTS" | grep -qiE '^Disallow:\s*/\s*$'; then
  fail "robots.txt has 'Disallow: /' — STAGING ROBOTS DEPLOYED, FIX IMMEDIATELY"
elif echo "$ROBOTS" | grep -qiE '^Allow:\s*/'; then
  pass "robots.txt allows indexing"
else
  warn "robots.txt found but no explicit Allow — review manually"
fi
if echo "$ROBOTS" | grep -qi "Sitemap:"; then
  pass "robots.txt references sitemap"
else
  warn "robots.txt has no Sitemap: line"
fi

# -----------------------------------------------------------------------------
# 4. Top-traffic 301 redirects (from GSC baseline)
# -----------------------------------------------------------------------------
hr
info "4. Top-traffic WP→CC 301 redirects (from 90d GSC baseline)"

# Format: "OLD_PATH|EXPECTED_NEW_PATH|GSC_CLICKS|NOTE"
REDIRECTS=(
  "/ra-aris-seo/|/ra-aris-seo.html|81|top traffic source"
  "/seo-management/|/seo-management.html|30|main service"
  "/best-seo-agency-in-georgia/|/blog/best-seo-agency-in-georgia.html|8|"
  "/local-seo/|/blog/local-seo.html|4|"
  "/link-building/|/seo-management.html|3|no equivalent"
  "/seo-saagento/|/blog/seo-saagento.html|2|blog (user confirmed 2026-05-13)"
  "/cifruli-marketingi/|/blog/cifruli-marketingi.html|2|"
  "/contact-us/|/contact-us.html|2|"
  "/blog/|/blog.html|2|"
  "/ra-aris-aeo/|/blog/ra-aris-aeo.html|2|"
  "/copywriting/|/blog/copywriting.html|0|blog (user confirmed 2026-05-13)"
  "/seo-audit/|/seo-audit.html|0|"
  "/about-us/|/about-us.html|0|"
  "/portfolio/|/portfolio.html|0|"
  "/case-studies/|/case-studies.html|0|"
)

for entry in "${REDIRECTS[@]}"; do
  IFS='|' read -r OLD NEW CLICKS NOTE <<< "$entry"
  RES=$(hit "$BASE_URL$OLD")
  CODE="${RES%%|*}"
  LOC="${RES##*|}"
  EXPECTED_LOC_PATH="${LOC#"$BASE_URL"}"
  EXPECTED_LOC_PATH="${EXPECTED_LOC_PATH#https://10xseo.ge}"

  LABEL="$OLD → $NEW"
  [ -n "$NOTE" ] && LABEL="$LABEL  (${CLICKS}c, $NOTE)"
  [ -z "$NOTE" ] && [ "$CLICKS" != "0" ] && LABEL="$LABEL  (${CLICKS}c)"

  if [ "$CODE" = "301" ] && [ "$EXPECTED_LOC_PATH" = "$NEW" ]; then
    pass "$LABEL"
  elif [ "$CODE" = "301" ]; then
    fail "$LABEL  → got 301 to $EXPECTED_LOC_PATH (expected $NEW)"
  elif [ "$CODE" = "200" ]; then
    fail "$LABEL  → got 200 (no redirect — broken)"
  else
    fail "$LABEL  → got HTTP $CODE"
  fi
done

# -----------------------------------------------------------------------------
# 5. Backlink-bearing URLs (Ahrefs data)
# -----------------------------------------------------------------------------
hr
info "5. Backlink-bearing URLs (preserve link equity)"

BACKLINKS=(
  "/seo-optimizacia/|/ra-aris-seo.html|3 referring domains (matches WP chain)"
  "/ufaso-seo-auditi/|/seo-audit.html|1 referring domain"
)

for entry in "${BACKLINKS[@]}"; do
  IFS='|' read -r OLD NEW NOTE <<< "$entry"
  RES=$(hit "$BASE_URL$OLD")
  CODE="${RES%%|*}"
  LOC="${RES##*|}"
  EXPECTED_LOC_PATH="${LOC#"$BASE_URL"}"
  EXPECTED_LOC_PATH="${EXPECTED_LOC_PATH#https://10xseo.ge}"
  if [ "$CODE" = "301" ] && [ "$EXPECTED_LOC_PATH" = "$NEW" ]; then
    pass "$OLD → $NEW  ($NOTE)"
  else
    fail "$OLD → expected 301 to $NEW; got $CODE → $EXPECTED_LOC_PATH  ($NOTE)"
  fi
done

# -----------------------------------------------------------------------------
# 6. Sitemap + custom 404
# -----------------------------------------------------------------------------
hr
info "6. Sitemap + 404 handling"
SM_RES=$(hit "$BASE_URL/sitemap.xml")
SM_CODE="${SM_RES%%|*}"
if [ "$SM_CODE" = "200" ]; then
  SM_URLS=$(curl -sk --max-time 10 "$BASE_URL/sitemap.xml" | grep -c "<loc>")
  pass "sitemap.xml → 200, $SM_URLS URLs"
else
  fail "sitemap.xml → $SM_CODE"
fi

NF_CODE=$(curl -sko /dev/null -w "%{http_code}" --max-time 10 "$BASE_URL/this-url-should-never-exist-xyz123")
if [ "$NF_CODE" = "404" ]; then
  pass "/this-url-should-never-exist-xyz123 → 404 (proper status code)"
else
  fail "Non-existent URL returned $NF_CODE (expected 404 — soft 404 hurts SEO)"
fi

# Custom 404 page rendered?
NF_BODY=$(curl -sk --max-time 10 "$BASE_URL/this-url-should-never-exist-xyz123")
if echo "$NF_BODY" | grep -qiE '404|not found|ვერ მოიძებნა|გვერდი ვერ'; then
  pass "Custom 404 page renders content"
else
  warn "404 response body doesn't look like our custom 404.html"
fi

# -----------------------------------------------------------------------------
# 7. No 5xx on top URLs
# -----------------------------------------------------------------------------
hr
info "7. Top 20 URLs — no 5xx"

TOP_URLS=(
  ""
  "seo-management.html" "seo-audit.html" "ai-seo.html" "cro.html"
  "copywriting.html" "google-ads.html" "ra-aris-seo.html"
  "blog.html" "case-studies.html" "portfolio.html"
  "about-us.html" "contact-us.html" "services.html" "seo-tools.html"
  "en/" "en/seo-management.html" "en/contact-us.html" "en/blog.html"
)

# bash 3.2 compatible (macOS default): use plain vars instead of associative array
SC_2xx=0; SC_3xx=0; SC_4xx=0; SC_5xx=0
HAS_5XX=0
for path in "${TOP_URLS[@]}"; do
  CODE=$(curl -sko /dev/null -w "%{http_code}" --max-time 10 "$BASE_URL/$path")
  case "$CODE" in
    2*) SC_2xx=$((SC_2xx+1)) ;;
    3*) SC_3xx=$((SC_3xx+1)) ;;
    4*) SC_4xx=$((SC_4xx+1)) ;;
    5*) SC_5xx=$((SC_5xx+1)); HAS_5XX=1; fail "5xx on /$path  ($CODE)" ;;
  esac
done
echo "   Status code distribution:"
echo "     2xx → $SC_2xx URLs"
echo "     3xx → $SC_3xx URLs"
echo "     4xx → $SC_4xx URLs"
echo "     5xx → $SC_5xx URLs"
if [ "$HAS_5XX" = "0" ]; then
  pass "No 5xx errors on top 20 URLs"
fi

# -----------------------------------------------------------------------------
# 8. Cache headers + compression
# -----------------------------------------------------------------------------
hr
info "8. Cache + compression headers (homepage)"
HDR=$(headers "$BASE_URL/")

if echo "$HDR" | grep -qi "cache-control"; then
  CC=$(echo "$HDR" | grep -i "cache-control" | head -1 | tr -d '\r')
  pass "Cache-Control: $CC"
else
  warn "No Cache-Control header on homepage"
fi

# Test compression on a CSS asset
ENC=$(curl -skI -H "Accept-Encoding: gzip, br" --max-time 10 "$BASE_URL/" | grep -i "content-encoding" | head -1 | tr -d '\r')
if [ -n "$ENC" ]; then
  pass "Compression active: $ENC"
else
  warn "No Content-Encoding on homepage (gzip/brotli not active)"
fi

# Security headers
for header in "x-content-type-options" "x-frame-options" "referrer-policy"; do
  if echo "$HDR" | grep -qi "$header"; then
    pass "Security header present: $header"
  else
    warn "Security header missing: $header"
  fi
done

# -----------------------------------------------------------------------------
# 9. Mixed content (http:// resources on https page)
# -----------------------------------------------------------------------------
hr
info "9. Mixed content scan (homepage)"
HOMEPAGE=$(curl -sk --max-time 15 "$BASE_URL/")
MIXED=$(echo "$HOMEPAGE" | grep -oE '(src|href)="http://[^"]+"' | grep -v "schema.org" | grep -v "w3.org" | head -5)
if [ -z "$MIXED" ]; then
  pass "No mixed content on homepage"
else
  fail "Mixed content found:"
  echo "$MIXED" | sed 's/^/     /'
fi

# -----------------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------------
hr
echo
echo "${BOLD}Summary${NC}"
echo "  ${GREEN}PASS:${NC} $PASS"
echo "  ${YELLOW}WARN:${NC} $WARN"
echo "  ${RED}FAIL:${NC} $FAIL"
echo

if [ "$FAIL" -gt 0 ]; then
  echo "${RED}${BOLD}✗ Cutover verification FAILED — review failures above.${NC}"
  echo "${RED}If any of: robots.txt Disallow /, all 301s broken, 5xx on top URLs — ROLLBACK DNS NOW.${NC}"
  exit 1
elif [ "$WARN" -gt 5 ]; then
  echo "${YELLOW}${BOLD}! Verification passed but with $WARN warnings — review.${NC}"
  exit 0
else
  echo "${GREEN}${BOLD}✓ Cutover verification PASSED${NC}"
  echo "  → continue with Phase 2 (GSC sitemap submit, GA4 check, server logs) per POST-CUTOVER-VERIFICATION.md"
  exit 0
fi
