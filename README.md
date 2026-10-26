# The Clear Out Crew – Website

Live site: https://clearoutcrewnyc.com
Built and maintained by Columbian Kenny Inc.

## Structure
- `src/index.html` – homepage (content, styles, scripts)
- `build.py` – builds `dist/`: adds SEO head tags, LocalBusiness schema, privacy/terms/thanks pages, sitemap.xml, robots.txt
- `site/img/` – compressed images, logo, icons
- `netlify.toml` – Netlify build settings and security headers

## Deploying
Netlify builds automatically on every push to `main` (`python3 build.py`, publishes `dist/`).
Test locally with `python3 build.py` and open `dist/index.html`.

## Please don't change without checking first
- The quote form (`name="quote"`, Netlify Forms) – submissions are emailed to the business
- Domain / DNS (managed at Namecheap)
- Google Search Console verification (DNS TXT record)
