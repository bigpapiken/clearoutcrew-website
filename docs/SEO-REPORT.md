# The Clear Out Crew: SEO audit & implementation report
clearoutcrewnyc.com · work done 2026-10-25 · not yet deployed (waiting on Netlify access)

## A. Executive summary
The developer's site was already technically solid (title, canonical, LocalBusiness schema,
sitemap, HTTPS, good accessibility). Its real SEO problem was **structure**: one URL trying to
rank for 10 services in 5 boroughs. Every competitor ranking for these searches (Junkluggers,
1-800-GOT-JUNK, Lugg, ZTERS) has a dedicated page per borough and per service, though their
borough pages are thin (ZTERS ~300 words; Junkluggers' Brooklyn page names no neighborhoods).

What changed:
- **12 new pages** (7 services, 5 boroughs) built from the site's own CSS and components, with
  copy based only on what the homepage already claims plus NYC Sanitation (DSNY) rules verified
  on nyc.gov. Linked from the existing homepage text, so nothing on the homepage looks different.
- **Layout shift fixed:** mobile CLS 0.182 → 0 (Google's "good" line is 0.1). The headline font
  loaded late and pushed the hero photos down.
- Self-hosted fonts, smaller logo/image files, favicon Google can display, schema rebuilt as a
  connected graph, canonical URL fixes, a real 404 page, an updated sitemap.
- Found that **the zip Jack sent is older than the live site**. Work was rebuilt on a snapshot of
  the live site so nothing (reCAPTCHA, accessibility page, clean URLs) gets lost.

## B. Changes implemented
**Technical SEO**
- `site/sitemap.xml`: 4 → 16 URLs, with lastmod. Uses clean URLs (`/privacy`), matching canonicals and internal links.
- Canonicals on privacy/terms/accessibility/thanks changed from `*.html` to the clean URLs the site actually links to (live had both versions returning 200 with mismatched canonicals).
- `site/404.html`: new noindex 404 page with links to every service and borough (Netlify serves it with a 404 status). Live had Netlify's default.
- `site/favicon.ico` + 192px icon: live returned 404 for /favicon.ico and only had a 32px icon (Google needs a multiple of 48px).
- `site/netlify.toml`: long cache for /fonts/*.

**Metadata & on-page**
- Homepage meta description: 216 → 143 chars (it was truncated in results). Title unchanged (already good).
- Each new page: unique title (43-57 chars), description (134-151 chars), H1, canonical, Open Graph.
- Homepage service names, "Commercial" items, borough names and footer service area are now links to the new pages, styled identically to the plain text they were.

**Structured data**
- Homepage: one `@graph` with WebSite + LocalBusiness (borough `areaServed` with Wikipedia `sameAs`, `knowsAbout`, offer catalog linking each service URL) + FAQPage matching the visible FAQ.
- New pages: WebPage + BreadcrumbList + Service (provider = the business) + FAQPage.
- Nothing invented: no address, ratings, reviews, prices or hours.

**New pages** (`tools/pages.py` → `tools/build_pages.py`)
/furniture-appliance-removal/ · /apartment-cleanouts/ · /estate-cleanouts/ · /storage-unit-cleanouts/ ·
/commercial-junk-removal/ · /construction-debris-removal/ · /property-management-cleanouts/ ·
/brooklyn-junk-removal/ · /queens-junk-removal/ · /manhattan-junk-removal/ · /bronx-junk-removal/ · /staten-island-junk-removal/
Each has unique local/practical content (building logistics, DSNY curbside rules with source links,
neighborhoods, 4-6 FAQs). 68-85% of each page's text appears on no other page.

**Performance**
- Fonts self-hosted (identical Google files) and inlined @font-face; removes 3 render-blocking Google Fonts requests. Critical weights preloaded.
- Logo: 71 KB file shown at ~130px → 20 KB version via srcset.
- 800px versions of the before/after photos added to srcsets (37-48% smaller than the 1200px files most phones were loading).

**Bug fix / deploy safety**
- The live HTML is Netlify's processed output. The quote form was restored to Netlify's source markup (`data-netlify`, honeypot, reCAPTCHA placeholder). Redeploying the live HTML as-is could have broken form detection.

## C. Before / after (measured)
| | Before (live) | After (local) |
|---|---|---|
| Indexable pages | 4 | 16 |
| Mobile CLS (homepage) | 0.182 | 0 |
| Desktop CLS (homepage) | 0.144 | 0 |
| Lighthouse SEO / A11y / Best practices | 100 / 100 / 100 | 100 / 100 / 100 (all 13 pages) |
| Lighthouse mobile performance | 90 | 97-99 (see caveat) |
| Render-blocking font requests | 3 | 0 |
| Schema.org validator | not run | 0 errors, 0 warnings, all 13 pages |
| W3C HTML validator | not run | 0 errors (1 expected Netlify attribute on the form) |
| Crawl QA (links, anchors, images, canonicals, sitemap, dup titles/H1s) | n/a | 0 problems |
| Visual regression vs live | n/a | same page heights, ≤0.05% pixels differ (logo/photo resampling only) |

Caveats: "before" was measured on the live Netlify site; "after" on a local server without
compression and without the reCAPTCHA script, so the performance score is optimistic. CLS
improvement is real (it's a font-loading fix). The storage page's LCP measured 2.6s locally,
just over the 2.5s line. Re-test on production. PageSpeed Insights API quota was exhausted
today, and the site has no Chrome field data yet (too new). Search Console data: no access.

## D. Remaining issues
1. **Not deployed.** Needs Buck on the developer's Netlify (requested). Code/infra. High.
2. **BIC registration unknown.** The site advertises construction debris and commercial waste hauling, which NYC regulates through BIC. Confirm with Jack before relaunch. External/legal. High.
3. **No analytics.** GA4 placeholder only. Needs Jack's GA4 property. External. High (can't measure results).
4. **Search Console** is owned by the developer. Need owner access or a new Domain property (TXT in Namecheap). External. High.
5. **reCAPTCHA** loads ~355 KB of script on every homepage visit (Netlify-injected, render-blocking). Option later: Netlify custom reCAPTCHA keys + lazy load, or honeypot-only. Code + Netlify config. Low-medium.
6. **No Google Business Profile link** on the site / in schema `sameAs` (need the Maps URL). External. Medium.
7. Privacy/terms meta descriptions are short boilerplate. Low.

## E. External recommendations
- Get Google reviews flowing; link the GBP from the site once we have the URL.
- Answer the questions in `qa/QUESTIONS-FOR-JACK.md` (insurance/COI, donation, pricing, hours, BIC). Each one unlocks stronger copy.
- Real job photos tagged by borough would make the borough pages much stronger.
- Citations: consistent name/phone on Yelp, Thumbtack, Angi, Bing Places, Apple Business Connect.

## F. Deployment readiness
- Build: static, no build errors. `python3 tools/build_pages.py` regenerates the new pages.
- Automated checks passed: crawl QA, copy lint, schema validator, W3C validator, Lighthouse, Chromium + WebKit (iPhone 13/SE) screenshots, no horizontal scroll.
- Design preserved on existing pages (pixel diff).
- **Not tested:** a real form submission on Netlify (can't until deployed). Do one immediately after deploy.
- Ready to deploy once Netlify access lands and the BIC question is answered. See `DEPLOY.md`.

## G. Assessment
After deploy, the site will be technically clean and crawlable with a page for every service and
borough it claims, which it lacked. Rankings now depend mostly on things outside the code:
Google Business Profile strength and reviews (the map pack dominates "junk removal near me"),
links/citations, and time. The domain was registered 2026-10-18, so expect months, not weeks, and
no guarantees. Biggest remaining on-site lever: real local proof (borough-tagged job photos,
reviews, licensing/insurance details) that we couldn't add without Jack's input.
