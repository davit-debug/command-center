# Post-Cutover Verification Plan — 10xseo.ge

ფაზური verification გეგმა DNS flip-ის შემდეგ. ყველა ფაზაში — **რა შევამოწმოთ**, **როგორ შევამოწმოთ**, **რა არის წითელი ალარმი**.

GSC baseline (90 დღე) რომელსაც უნდა შევუდაროთ:

| URL | Clicks | Impressions | რას ვამოწმებთ |
|---|---|---|---|
| `/ra-aris-seo/` | 81 | 4,972 | ყველაზე დიდი ტრაფიკის წყარო — 301 → `/ra-aris-seo.html` |
| `/seo-management/` | 30 | 1,854 | მთავარი სერვისი — 301 → `/seo-management.html` |
| `/best-seo-agency-in-georgia/` | 8 | 1,155 | 301 → `/blog/best-seo-agency-in-georgia.html` |
| `/seo-saagento/` | 2 | 1,222 | მაღალი imp — 301 → `/blog/seo-saagento.html` (blog — user confirmed) |
| `/cifruli-marketingi/` | 2 | 548 | 301 → `/blog/cifruli-marketingi.html` |
| `/contact-us/` | 2 | 216 | 301 → `/contact-us.html` |
| `/local-seo/` | 4 | 150 | 301 → `/blog/local-seo.html` |
| `/link-building/` | 3 | 162 | 301 → `/seo-management.html` |
| `/blog/` | 2 | 139 | 301 → `/blog.html` |
| `/ra-aris-aeo/` | 2 | 92 | 301 → `/blog/ra-aris-aeo.html` |
| `/seo-optimizacia/` | — | — | **3 backlink-ი** — 301 → `/ra-aris-seo.html` (matches WP's existing redirect chain) |
| `/ufaso-seo-auditi/` | — | — | **1 backlink** — 301 → `/seo-audit.html` |

---

## ფაზა 1 — T+0 (DNS flip-დან 30 წთ-ში)

**მიზანი:** გავიგოთ საიტი მთლიანად ცოცხალი დარჩა თუ კატასტროფაა.
**წითელი ალარმი:** ერთ-ერთი fail-იც ნიშნავს rollback-ს (DNS უკან WP-ზე).

### 1.1 DNS propagation
```bash
# რამდენიმე nameserver-დან:
dig +short 10xseo.ge @8.8.8.8       # Google
dig +short 10xseo.ge @1.1.1.1       # Cloudflare
dig +short 10xseo.ge @208.67.222.222 # OpenDNS
```
**Pass:** სამივე აბრუნებს Cloudways-ის IP-ს.
**Fail:** რომელიმე ჯერ ძველ IP-ს აბრუნებს — დაელოდე 5-15 წთ.

### 1.2 HTTPS + canonical host
```bash
curl -sI http://10xseo.ge/        | head -3   # უნდა იყოს 301 → https
curl -sI https://www.10xseo.ge/   | head -3   # უნდა იყოს 301 → apex
curl -sI https://10xseo.ge/       | head -3   # უნდა იყოს 200
```
**Pass:** პირველი ორი 301-ია, მესამე 200.
**Fail:** SSL error (`SSL certificate problem`) — Cloudways-ში Let's Encrypt არ გაიცა; `Domain Management`-ში ხელახლა გენერირება.

### 1.3 robots.txt — ინდექსაცია ნებადართულია
```bash
curl -s https://10xseo.ge/robots.txt
```
**Pass:** ხედავ `Allow: /` — **არა** `Disallow: /`.
**Fail (კრიტიკული):** თუ Disallow: / გადავიდა შეცდომით — მაშინვე ჩაასწორე და ხელახლა deploy. Google შეიძლება 24-ში დაიწყოს deindexing.

### 1.4 5 ყველაზე მაღალი ტრაფიკის 301 (ერთ ბრძანებაში)
```bash
for url in ra-aris-seo seo-management best-seo-agency-in-georgia seo-saagento contact-us; do
  echo "=== /$url/ ==="
  curl -sI "https://10xseo.ge/$url/" | head -2
done
```
**Pass:** თითოეული `301` + `Location:` სწორი `.html` URL-ზე.
**Fail:** 200 (redirect არ მუშაობს, ხსნის ცარიელ გვერდს) ან 404 — `.htaccess` ან mod_rewrite არ მუშაობს. Cloudways → Application Settings → დაუძახე `.htaccess override`-ს.

### 1.5 Backlink-ების 301-ები (Ahrefs-დან)
```bash
curl -sI "https://10xseo.ge/seo-optimizacia/" | head -2   # 3 backlink — კრიტიკული
curl -sI "https://10xseo.ge/ufaso-seo-auditi/" | head -2  # 1 backlink
```
**Pass:** 301 → `/seo-management.html` და `/seo-audit.html` შესაბამისად.

### 1.6 Sitemap + custom 404
```bash
curl -sI https://10xseo.ge/sitemap.xml | head -1   # 200
curl -sI https://10xseo.ge/this-does-not-exist | head -1   # 404 (NOT 200)
curl -s  https://10xseo.ge/this-does-not-exist | grep -o '<title>[^<]*' | head -1
```
**Pass:** sitemap = 200, არასწორი URL = 404 და title-ში ჩვენი 404 გვერდი.
**Fail:** 404 status code-ით 200 აბრუნებს (soft 404) — მავნე SEO-ს.

### 1.7 No 5xx errors
```bash
# 20 ყველაზე მნიშვნელოვან URL-ს ვცემთ თავს:
for path in "" sitemap.xml seo-management.html seo-audit.html ai-seo.html cro.html copywriting.html google-ads.html ra-aris-seo.html blog.html case-studies.html portfolio.html about-us.html contact-us.html services.html seo-tools.html en/ en/seo-management.html en/contact-us.html en/blog.html; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "https://10xseo.ge/$path")
  echo "$code  /$path"
done | sort | uniq -c
```
**Pass:** ყველა 200 (homepage და /en/-ისთვის — დირექტორიას ემსახურება index.html).
**Fail:** ერთიც 5xx — Cloudways logs შეამოწმე (`Application Logs`-ში).

> **განაცხადი:** ფაზა 1 უნდა დასრულდეს **30 წუთში**. თუ რომელიმე ალარმი მოწითლდა — DNS-ის დაბრუნება WP-ზე და გასარკვევია გადადება.

---

## ფაზა 2 — T+1სთ-დან T+24სთ-მდე

**მიზანი:** რეალური მომხმარებელი + ბოტები ხედავენ ახალ საიტს, ყველაფერი გათლილია.

### 2.1 Search Console — sitemap ხელახლა გაგზავნე
- GSC → Sitemaps → წაშალე ძველი → დაამატე `https://10xseo.ge/sitemap.xml` → "Submit"
- 1-2 საათში: Status = "Success"; Discovered URLs ≈ 120

### 2.2 Top 10 URL-ის reindex მოთხოვნა
GSC → URL Inspection → თითო-თითოდ:
- `https://10xseo.ge/`
- `https://10xseo.ge/seo-management.html`
- `https://10xseo.ge/seo-audit.html`
- `https://10xseo.ge/ra-aris-seo.html`
- `https://10xseo.ge/blog.html`
- `https://10xseo.ge/contact-us.html`
- `https://10xseo.ge/about-us.html`
- `https://10xseo.ge/copywriting.html`
- `https://10xseo.ge/services.html`
- `https://10xseo.ge/portfolio.html`

თითოეულზე → "Request indexing"

### 2.3 GA4 / Analytics — ხედავს თუ არა ტრაფიკს
- GA4 → Realtime → უნდა ჩანდეს მინიმუმ 1-2 აქტიური მომხმარებელი (შენ ხარ უმეტეს შემთხვევაში)
- **Fail:** gtag არ ჩაიტვირთა — ხედავ Tag Assistant-ში
- ფაილში `<script async src="https://www.googletagmanager.com/gtag/js...">` უნდა ჩატვირთოს

### 2.4 Cloudways Server Logs — 5xx & 404 spike
Cloudways Console → Application → **Application Logs**:
- Apache error log — `5xx` რაოდენობა < 5 პირველ საათში
- Access log — `404` სიხშირე — არ უნდა იყოს > 50/სთ
- ყველაზე ხშირი 404-ები რომელია? თუ ერთი და იგივე URL-ი 50-ჯერ მოვიდა → იქ აშკარად backlink-ია სადღაც, .htaccess-ში redirect-ი დაამატე

### 2.5 Form submissions test
- გახსენი `/contact-us.html`, `/seo-audit.html`, `/vacancies.html` და გააგზავნე ტესტ-ფორმა
- Tally / external form tool-ში confirm რომ submission ჩაჯდა
- **Fail:** ფორმა გასცემს ცარიელ გვერდს ან CORS error — embed src-ი სწორი domain-ზე უნდა მიდიოდეს

### 2.6 Third-party widgets
- YouTube embed (`/ai-seo.html` ვიდეო) — ჩატვირთოს ჩვეულებრივ
- Calendly (`/copywriting.html` თუ რომელ-რომელ გვერდზეა) — გახსნას booking modal
- Hex animation — homepage-ზე და სხვა გვერდებზე ვიზუალურად მუშაობს
- Mobile menu — hamburger-მა იხსნას

### 2.7 Mixed-content & broken assets
```bash
# გაუშვი homepage-ზე — http:// რესურსი არსებობს?
curl -s https://10xseo.ge/ | grep -oE 'src="http://[^"]+"|href="http://[^"]+"' | head -5
```
**Pass:** ცარიელი output — მხოლოდ https:// რესურსები.
**Fail:** რომელიმე http://-ით — browser console-ში "Mixed Content" warning, padlock იქცევა გადახაზულ.

---

## ფაზა 3 — დღე 2-დან დღე 7-მდე (ინდექსის მიგრაცია)

**მიზანი:** Google ხვდება რომ URL-ები გადავიდა, ძველი deindex-დება, ახალი ინდექსდება.

### 3.1 GSC Coverage report — დღიური check
GSC → Pages (Indexing) → ყურადღებით:
- **"Page with redirect"** — ეს უნდა იზრდებოდეს (კარგი ნიშანია, ძველი WP URL-ები 301-ით მოდიან). მე-3-მე-7 დღე — უნდა დაინახო ~80 URL ამ კატეგორიაში.
- **"Not found (404)"** — ეს არ უნდა იზრდებოდეს. თუ 5+ ახალი 404 ჩნდება — შეამოწმე რომელი URL-ები და დაამატე .htaccess-ში.
- **"Crawled - currently not indexed"** — დროებით გაიზრდება (ახალი URL-ები დასაინდექსად დგას ნავაში). მე-7 დღემდე უნდა დაიწყოს კლება.
- **"Indexed"** — საბაზისო რიცხვი (cutover-მდე) — ნახე და ჩაიწერე ახლა. მე-7 დღემდე ≥ 80%-ს უნდა მიაღწიოს.

### 3.2 Top URL-ების impression trend
GSC → Performance → შეადარე "Last 7 days" vs "Previous 7 days"
- ნახე ცალკ-ცალკე top-10 URL-ის (ცხრილი ზემოთ) Impressions
- **Pass:** მთლიანი impressions უცვლელი ან +5%
- **Yellow:** −10-დან −25%-მდე — ნორმაა მიგრაციის პერიოდისთვის, დააკვირდი დღე 14-მდე
- **Red:** −30%+ — გასარკვევია; გაუშვი თითო URL-ის "URL Inspection" და ნახე რა ხდება

### 3.3 ხელით 301 chain check (კრიტიკული)
```bash
# ყოველი redirect ერთ-ჰოპიანი უნდა იყოს. /seo-management/ → /seo-management.html. წერტილი.
# არა /seo-management/ → /seo-management → /seo-management.html (chain)
for url in ra-aris-seo seo-management best-seo-agency-in-georgia seo-saagento copywriting; do
  echo "=== /$url/ ==="
  curl -sIL "https://10xseo.ge/$url/" | grep -E "HTTP|Location" | head -10
done
```
**Pass:** თითო URL-ისთვის — 1 × `301` და 1 × `200`. ჯამში 2 ხაზი ერთი URL-ისთვის.
**Fail:** 2+ × `301` — chain-ი გაქვს (slow, juice loss). გასწორება: .htaccess-ში RewriteRule სწორ target-ზე უშუალოდ აპირებს.

### 3.4 PageSpeed Insights — top 5
```
https://pagespeed.web.dev/analysis?url=https://10xseo.ge/
https://pagespeed.web.dev/analysis?url=https://10xseo.ge/seo-management.html
https://pagespeed.web.dev/analysis?url=https://10xseo.ge/blog.html
https://pagespeed.web.dev/analysis?url=https://10xseo.ge/case-studies.html
https://pagespeed.web.dev/analysis?url=https://10xseo.ge/contact-us.html
```
**Pass:** Mobile score ≥ 80, Desktop ≥ 95. LCP < 2.5s, CLS < 0.1, INP < 200ms.

### 3.5 SERP ranking spot-check (ხელით)
ანონიმური Chrome (Incognito) + VPN GE-ზე → დაუძახე:
- `seo სააგენტო` — ვართ თუ არა ისევე top-10-ში როგორც ადრე?
- `სეო სააგენტო` — იგივე
- `seo აუდიტი`
- `link building საქართველო`
- `ra aris seo`

თუ რომელიმე keyword-ზე SERP-ში ჩამოვცვივდით 5+ პოზიციით — შეიძლება URL მაპინგი არასწორი იყოს, ან Google-მა ჯერ არ მოასწრო.

### 3.6 Mobile rendering check
- Chrome DevTools → Toggle Device → iPhone 14, Galaxy S20 — მოხვედი ბევრი გვერდი
- Lighthouse → Mobile mode — Run

### 3.7 Hreflang / canonical-ების ვალიდაცია
```bash
# Hreflang-ი თუ წერია — გადამოწმება რომ URL-ები არსებობს:
curl -s https://10xseo.ge/seo-management.html | grep -oE '<link rel="alternate" hreflang="[^"]+" href="[^"]+"' | head -5
# Canonical-ი თუ ვერ მიდის ძველი WP URL-ზე:
curl -s https://10xseo.ge/seo-management.html | grep -oE '<link rel="canonical" href="[^"]+"'
```
**Pass:** canonical = `https://10xseo.ge/seo-management.html` (NOT `/seo-management/`)
**Fail:** canonical ისევ ძველი WP-ის ფორმატით — გრამატიკული შეცდომაა, სწრაფად გასწორდი.

---

## ფაზა 4 — დღე 8-დან დღე 30-მდე (settled)

**მიზანი:** დარწმუნდეთ მიგრაცია მთლიანად დასრულდა, regression არ აქვს.

### 4.1 GSC 28-დღიანი ჯამი vs ბაზელაინი
GSC → Performance → "Compare" → "Last 28 days" vs "Previous 28 days"
- **Total Clicks** — უნდა იყოს ≥ 90% ბაზელაინის
- **Total Impressions** — უნდა იყოს ≥ 95%
- **Average Position** — არ უნდა გაიზარდოს 2+ პოზიციით (გახსოვდეს, position დაბალი = კარგი)
- **Average CTR** — უცვლელი ან მცირე ვარდნა (ნორმაა — ახალი URL-ები ჯერ ვერ მოხვდა SERP-ის ცნობად ფორმატში)

### 4.2 Indexed pages count
GSC → Pages → "Indexed" — უნდა იყოს ≥ ცუდმე ცხოვრებაზე ცოტა მეტი (ბევრი URL დაიწერა გადააკვანებად, ცოტა ახალი დაემატა)

### 4.3 Backlink integrity check (Ahrefs)
- Ahrefs → Site Explorer → 10xseo.ge → Backlinks
- შეადარე "New" / "Lost" backlinks ბოლო 28 დღეში
- **Pass:** "Lost" < 5%-ზე ცოტა მეტი (ბუნებრივი churn)
- **Fail:** ერთ-ერთ მაღალი DR backlink-მა მიგრაციის შემდეგ "Lost" სტატუსი — შეიძლება chain ან 404 აქვს. შეასწორე .htaccess.
- სპეციფიკური check: `/seo-optimizacia/` და `/ufaso-seo-auditi/` ჯერ კიდევ 301 → სწორ target-ზე

### 4.4 Server logs სრული scan
Cloudways → Application Logs → ბოლო 30 დღე → ყველაზე ხშირი 404-ები:
```bash
# Cloudways SSH-ით:
ssh master_xxx@SERVER 'cd ~/applications/APP/logs/apache_logs/ && \
  awk "{print \$7, \$9}" access.log* | grep " 404$" | awk "{print \$1}" | \
  sort | uniq -c | sort -rn | head -20'
```
ნახე top 20 — ყველა გასაგებია? ხელახლა გადააწეროს redirect თუ რამე ახალი backlink ისე დააწერა URL-ი რომელზეც .htaccess-ში წესი არ გვაქვს.

### 4.5 Cleanup — საბოლოო
- [ ] ძველი WordPress hosting — მოშალე subscription (30 დღე გავიდა, კარგი backup-ი გვაქვს)
- [ ] GitHub Pages workflows (`pages.yml`, `deploy.yml`) — მოშალე ან გამორთე — ისინი ისევ აქმნიან artifact-ებს ფუჭად
- [ ] DNS TTL აწიე 3600 ან 86400-მდე (cutover TTL 300 აღარ გვჭირდება)
- [ ] Cloudways → enable HSTS in `.htaccess` (uncomment Strict-Transport-Security ხაზი) მხოლოდ მას შემდეგ რაც დარწმუნდი HTTPS ყველგან მუშაობს
- [ ] Cloudways → enable Cloudflare integration (free CDN — additional speed boost)

### 4.6 Backup verify
Cloudways → Backups → ნახე ავტო-backup-ი ხდება ყოველდღე
- ხელახლა გადააკეთე manual backup ინდექსაციის გასწვრივ

---

## დამხმარე script — ერთი ბრძანებით ფაზა 1-ის გავლა

ფაილი: `_cloudways/verify-cutover.sh` (შემდეგი ფაილი)
```bash
bash _cloudways/verify-cutover.sh
```
ერთ ჯერზე ყველა URL-ის სტატუსს, redirect target-ს, headers-ს გვიყურებს და "PASS / FAIL" აჩვენებს ცხრილად.

---

## რა რაოდენობით უნდა ცდილობდე verify-ს

| ფაზა | სავარაუდო დრო |
|---|---|
| ფაზა 1 (T+0..30წთ) | 15-20 წუთი ხელით |
| ფაზა 2 (T+1სთ..24სთ) | 1 საათი (ფორმების ტესტი + GSC submission) |
| ფაზა 3 (დღე 2-7) | 10 წთ/დღეში check |
| ფაზა 4 (დღე 8-30) | 30 წთ კვირაში |

**კრიტიკული წითელი ალარმები** რომელთა შემთხვევაში DNS-ი მაშინვე უნდა გადააბრუნო ძველზე:
1. ფაზა 1.3: robots.txt-ში `Disallow: /` შეცდომით
2. ფაზა 1.4: ყველა 301 ცარიელ გვერდს გასცემს ან 404-ს
3. ფაზა 1.7: 5+ URL აბრუნებს 5xx
4. ფაზა 2.5: ყველა ფორმა გატეხილია
