# The Clear Out Crew – Website

Live site: https://clearoutcrewnyc.com
Built by Columbian Kenny Inc. SEO update (service + borough pages, performance, schema) by War-Buck Marketing, October 2026.

## Structure
- `site/` – the published site (static HTML, no build step on Netlify)
  - `index.html` – homepage. Its `<style>`, header and footer are the design source for every other page.
  - `<service>/` and `<borough>-junk-removal/` – generated pages (don't edit by hand)
  - `privacy.html`, `terms.html`, `accessibility.html`, `thanks.html`, `404.html`
  - `img/`, `fonts/` (self-hosted Google Fonts), `favicon.ico`, `sitemap.xml`, `robots.txt`
- `tools/pages.py` – copy for the service and borough pages
- `tools/build_pages.py` – regenerates those pages, `404.html` and `sitemap.xml`
- `tools/qa_crawl.py`, `tools/copylint.py`, `tools/serve.py` – checks (see DEPLOY.md)
- `docs/` – SEO report and open questions

## Editing
1. Homepage or design change: edit `site/index.html`, then run `python3 tools/build_pages.py` so the other pages pick it up.
2. Service/borough copy: edit `tools/pages.py`, then `python3 tools/build_pages.py`.
3. Check: `python3 tools/serve.py 8871` in one terminal, `python3 tools/qa_crawl.py` in another.

## Deploying
Netlify deploys automatically on every push to `main` (publishes `site/` as-is).

## Please don't change without checking first
- The quote form (`name="quote"`, Netlify Forms, `data-netlify-recaptcha`) – submissions are emailed to the business. After any change, send a test quote.
- Domain / DNS (managed at Namecheap)
- Google Search Console verification (DNS TXT record)
