# The Clear Out Crew: SEO update, deploy notes

**Deploy folder:** `site/` (static, no build step needed on Netlify).
**Do not deploy** the developer's old zip (`reference-zip/`): it's older than the live site and
would remove the reCAPTCHA, the accessibility page and the clean URLs.

## Where this came from
- `site/` started as an exact snapshot of https://clearoutcrewnyc.com on 2026-10-25
  (the live site was newer than the zip Jack sent), then optimized. `git log` shows every step.
- The live HTML is Netlify's *processed* output. The quote form was restored to Netlify's
  *source* markup (`data-netlify="true"`, `netlify-honeypot`, `data-netlify-recaptcha`) so
  Netlify detects the form and re-injects reCAPTCHA on deploy. **After deploying, send one test
  quote and confirm it arrives** before announcing anything.

## Rebuild the new pages after a copy edit
    python3 tools/build_pages.py      # service/borough pages, 404, sitemap
    python3 tools/qa_crawl.py         # needs: python3 tools/serve.py 8871 running
    python3 tools/copylint.py

New pages pull their CSS/header/footer from `site/index.html`, so edit the homepage first, then rebuild.

## Deploy (once Buck has access to the developer's Netlify site)
1. Coordinate with Columbian Kenny Inc. first (their README asks for it). If they deploy from
   their own `build.py`, it will overwrite this work. Agree who owns deploys from now on.
2. Netlify > the site > Deploys > drag the `site/` folder in (or `netlify deploy --prod --dir=site`).
3. Check: homepage, 2-3 new pages, `/sitemap.xml`, a fake URL returns the 404 page, and
   submit one real test quote (with a photo).
4. Netlify > Forms: confirm the `quote` form is still listed and notifications still email Jack.

## After deploy
- Google Search Console: resubmit `https://clearoutcrewnyc.com/sitemap.xml` and request indexing
  for the homepage and the 12 new pages. The current GSC property belongs to the developer;
  ask them to add Buck as an owner, or verify a new Domain property with a TXT record in Namecheap.
- Bing Webmaster Tools: import from GSC, submit the sitemap.
- The 5 borough pages are for organic search only. Don't use them to create extra Google
  Business Profile locations (the business has no storefronts there).
