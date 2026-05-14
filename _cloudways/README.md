# `_cloudways/` — 10xseo.ge migration toolkit

ეს ფოლდერი GitHub Pages → Cloudways გადასვლისთვის. **არცერთი ფაილი ცოცხალ საიტზე გავლენას არ ახდენს** სანამ deploy workflow ხელით არ გადაიტანე `.github/workflows/`-ში.

## ფაილები (კითხვის თანმიმდევრობით)

| # | ფაილი | რა არის | როდის |
|---|---|---|---|
| 1 | [`MIGRATION-CHECKLIST.md`](MIGRATION-CHECKLIST.md) | A-დან F-მდე ბიჯ-ბიჯი ინსტრუქცია (Cloudways setup, SSH key, DNS flip, rollback) | **ჯერ ეს წაიკითხე** |
| 2 | [`REDIRECT-MAP.csv`](REDIRECT-MAP.csv) | სრული WP→CC URL მაპა GSC + Ahrefs მონაცემებით | reference / audit doc |
| 3 | [`.htaccess`](.htaccess) | Production .htaccess — HTTPS, gzip, cache, ~80 redirects, custom 404 | deploy იტვირთება საიტის root-ში |
| 4 | [`robots.txt`](robots.txt) | Production robots (Allow: / + AI crawlers) | ცვლის ცოცხალ Disallow: / |
| 5 | [`cloudways-deploy.yml`](cloudways-deploy.yml) | GitHub Actions workflow — push → rsync to Cloudways | move to `.github/workflows/` |
| 6 | [`POST-CUTOVER-VERIFICATION.md`](POST-CUTOVER-VERIFICATION.md) | 4-ფაზიანი verification გეგმა (T+0 → დღე 30) | DNS flip-ის შემდეგ |
| 7 | [`verify-cutover.sh`](verify-cutover.sh) | bash script რომელიც ფაზა 1-ის ყველა შემოწმებას ერთ ბრძანებაში გავუშვებთ | DNS flip-დან 30 წთ-ში |

## სწრაფი workflow

1. Cloudways-ში სერვერი + აპი დააყენე (PHP 8.x stack — ვიდრე WordPress)
2. SSH key + GitHub secrets
3. `mv _cloudways/cloudways-deploy.yml .github/workflows/`
4. Push → temp URL ცოცხალდება (~ 5 წთ)
5. CHECKLIST-ის სექცია C გადაიარე temp URL-ზე
6. DNS flip
7. `bash _cloudways/verify-cutover.sh` — ფაზა 1
8. POST-CUTOVER-VERIFICATION ფაზები 2-4 დროის მიხედვით

## მნიშვნელოვანი

- **`.gitignore` რომ არ გამოგრიცხოს ეს ფოლდერი** — repo-ს `.gitignore` არის allowlist (ყველაფერი blocked default-ით). თუ გინდა commit ეს ფაილები, დაამატე:
  ```
  !_cloudways/
  !_cloudways/**
  ```
  ან დატოვე როგორც ლოკალური სამუშაო doc-ი (deploy workflow მაინც გამოიყენებს გადატანამდე).

- **Deploy workflow ავტომატურად აკოპირებს** `_cloudways/.htaccess` და `_cloudways/robots.txt`-ს root-ში rsync-ის წინ — ანუ staging-ზე (GitHub Pages) ისინი არასოდეს მოხვდება.

- **Cloudways-ში PHP-ი აარჩიე**, NOT WordPress — სტატიკურ HTML-ს არც PHP არც DB არ სჭირდება, უბრალოდ Apache+Nginx-ის გარემო გვინდა.
