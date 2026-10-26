"""Build the service and borough pages for The Clear Out Crew.

    python3 tools/build_pages.py

The pages reuse the homepage's own CSS, header, footer and mobile call bar, pulled
straight out of site/index.html at build time, so they always match the live design.
Page copy lives in tools/pages.py. Also writes site/404.html and site/sitemap.xml.
"""
import html, json, pathlib, re, sys

R = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R / 'tools'))
import pages as P  # noqa: E402

SITE = R / 'site'
D = 'https://clearoutcrewnyc.com'
PHONE, TEL = '(917) 533-3220', '+19175333220'
HOME = (SITE / 'index.html').read_text()

# ---------- pieces lifted from the homepage ----------
styles = re.findall(r'<style>(.*?)</style>', HOME, re.S)
FONT_FACES, MAIN_CSS = styles[0], styles[1]
assert '@font-face' in FONT_FACES and '.hero' in MAIN_CSS

def absolutize(chunk):
    """Homepage-relative links -> site-absolute so they work from /some-page/."""
    chunk = re.sub(r'(src|srcset|href)="img/', r'\1="/img/', chunk)
    chunk = re.sub(r', img/', ', /img/', chunk)
    chunk = re.sub(r'href="#(?!main)', 'href="/#', chunk)
    return chunk

HEADER = absolutize(re.search(r'<header class="top">.*?</header>', HOME, re.S).group(0)).replace('href="/#top"', 'href="/"')
FOOTER = absolutize(re.search(r'<footer class="foot">.*?</footer>', HOME, re.S).group(0))
MBAR = absolutize(re.search(r'<nav class="mbar".*?</nav>', HOME, re.S).group(0))
FINAL = absolutize(re.search(r'<div class="stripe" aria-hidden="true"></div>\s*<section class="band dark final".*?</section>', HOME, re.S).group(0))
STEPS_CSS_OK = '.steps' in MAIN_CSS

# Small additions for the new pages only. Built from the same tokens; the homepage is untouched.
PAGE_CSS = """
.crumbs{margin:0 0 18px;padding:0;list-style:none;display:flex;flex-wrap:wrap;gap:6px 10px;font:600 .95rem/1.2 var(--cond);letter-spacing:.06em;text-transform:uppercase;color:var(--muted-dark)}
.crumbs li+li::before{content:"/";margin-right:10px;color:var(--ink-line)}
.crumbs a{text-decoration:none}.crumbs a:hover{color:var(--cream);text-decoration:underline}
.hero .caps{border-top-color:var(--ink-line)}
.prose{display:grid;gap:18px;font-size:1.08rem;max-width:66ch}
.prose h3{font-size:1.55rem;margin-top:10px}
.prose ul{margin:0;padding-left:22px;display:grid;gap:6px}
.dark .prose{color:var(--cream)}.dark .prose p,.dark .prose li{color:var(--muted-dark)}
.split{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);gap:clamp(32px,6vw,80px);align-items:start}
@media (max-width:860px){.split{grid-template-columns:minmax(0,1fr)}}
.svc b a,.caps b a,.boros a,.links a{color:inherit;text-decoration:none}
.svc b a:hover,.caps b a:hover,.boros a:hover,.links a:hover{text-decoration:underline;text-underline-offset:.15em}
.links{list-style:none;margin:0;padding:0;border-top:3px solid var(--ink)}
.links li{padding:16px 0;border-bottom:1px solid var(--paper-line);font:700 1.2rem/1.2 var(--cond);letter-spacing:.02em;text-transform:uppercase}
.src{margin-top:22px;color:var(--muted);font-size:.95rem}
.dark .src{color:var(--muted-dark)}
.src a{color:inherit}
@media (min-width:1000px){.boros.four{grid-template-columns:repeat(4,minmax(0,1fr))}}
"""

HERO_JS = """<script>
(function(){var hp=document.querySelector('.hero-photos');if(!hp)return;
hp.querySelectorAll('[data-side]').forEach(function(f){var go=function(){hp.setAttribute('data-front',f.getAttribute('data-side'));};
f.addEventListener('mouseenter',go);f.addEventListener('focus',go);f.addEventListener('click',go);});})();
</script>"""

esc = lambda s: html.escape(s, quote=True)


def jsonld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, indent=1, ensure_ascii=False) + '\n</script>'


def strip_tags(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s))


def page(pg):
    url = f"{D}/{pg['slug']}/"
    crumbs = [("Home", f"{D}/"), (pg['crumb_parent'][0], None), (pg['crumb'], url)] if pg.get('crumb_parent') else [("Home", f"{D}/"), (pg['crumb'], url)]
    crumb_html = '<ol class="crumbs">' + ''.join(
        f'<li><a href="/">{n}</a></li>' if i == 0 else (f'<li aria-current="page">{esc(n)}</li>' if u == url else f'<li>{esc(n)}</li>')
        for i, (n, u) in enumerate(crumbs)) + '</ol>'
    graph = [
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": strip_tags(pg['title']), "description": pg['desc'],
         "isPartOf": {"@id": f"{D}/#website"}, "about": {"@id": url + "#service"}, "breadcrumb": {"@id": url + "#breadcrumb"},
         "inLanguage": "en-US"},
        {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, **({"item": u} if u else {})} for i, (n, u) in enumerate(crumbs)]},
        {"@type": "Service", "@id": url + "#service", "name": pg['service_name'], "serviceType": pg['service_type'],
         "url": url, "description": pg['desc'], "provider": {"@id": f"{D}/#business"},
         "areaServed": pg['area_served']},
        {"@type": "WebSite", "@id": f"{D}/#website", "url": f"{D}/", "name": "The Clear Out Crew", "publisher": {"@id": f"{D}/#business"}},
        {"@type": "LocalBusiness", "@id": f"{D}/#business", "name": "The Clear Out Crew", "url": f"{D}/",
         "telephone": TEL, "email": "theclearoutcrew718@gmail.com", "image": f"{D}/img/og-image.jpg"},
    ]
    if pg.get('faq'):
        graph.append({"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": strip_tags(q), "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in pg['faq']]})
    faq_html = ''
    if pg.get('faq'):
        faq_html = f"""
  <section class="band" id="faq" aria-labelledby="faq-title">
    <div class="wrap">
      <div class="head"><h2 id="faq-title">{pg.get('faq_title', 'Questions')}</h2><p class="lede">Don't see your question? Call or text {PHONE}.</p></div>
      <div class="faq">
""" + '\n'.join(f'        <details><summary>{q}</summary><p>{a}</p></details>' for q, a in pg['faq']) + """
      </div>
    </div>
  </section>"""
    proof = ''.join(f'<li>{p}</li>' for p in pg['proof'])
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{pg['title']}</title>
<meta name="description" content="{esc(pg['desc'])}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#151513">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/img/icon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="/img/icon-180.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="The Clear Out Crew">
<meta property="og:title" content="{pg['title']}">
<meta property="og:description" content="{esc(pg['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{D}/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
{jsonld({"@context": "https://schema.org", "@graph": graph})}
<link rel="preload" href="/fonts/big-shoulders-stencil-display-700-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/barlow-400-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/barlow-condensed-700-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/barlow-condensed-600-latin.woff2" as="font" type="font/woff2" crossorigin>
<style>{FONT_FACES}</style>
<style>{MAIN_CSS}{PAGE_CSS}</style>
</head>
<body>

<a class="skip" href="#main">Skip to content</a>

{HEADER}

<main id="main">
  <section class="hero dark" id="top" aria-labelledby="hero-title">
    <div class="wrap">
      <div>
        {crumb_html}
        <h1 id="hero-title">{pg['h1']}</h1>
        <p class="lede">{pg['lede']}</p>
        <div class="hero-actions">
          <a class="btn btn-yellow" href="/#quote">{pg.get('cta', 'Get a free quote')}</a>
          <a class="btn btn-line" href="tel:{TEL}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2"/></svg>Call {PHONE}</a>
        </div>
        <ul class="proof">{proof}</ul>
      </div>
      {pg['hero_right']}
    </div>
  </section>
  <div class="stripe" aria-hidden="true"></div>
{''.join(pg['sections'])}{faq_html}

  {FINAL}
</main>

{FOOTER}

{MBAR}
{HERO_JS if 'hero-photos' in pg['hero_right'] else ''}
</body>
</html>
"""
    out = SITE / pg['slug'] / 'index.html'
    out.parent.mkdir(exist_ok=True)
    out.write_text(doc)
    return url


def not_found():
    """404 page in the same style as the privacy/terms pages."""
    priv = (SITE / 'privacy.html').read_text()
    head_css = re.findall(r'<style>.*?</style>', priv, re.S)
    links = ''.join(f'<li><a href="/{s}/">{n}</a></li>' for s, n in P.NAV_404)
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Page not found | The Clear Out Crew</title>
<meta name="description" content="That page doesn't exist. Find junk removal services and the boroughs The Clear Out Crew covers.">
<meta name="robots" content="noindex">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/img/icon-192.png" sizes="192x192" type="image/png">
{''.join(head_css)}
</head>
<body>
<header><div class="wrap"><a href="/"><img src="/img/logo.webp" srcset="/img/logo-320.webp 320w, /img/logo-640.webp 640w, /img/logo.webp 900w" sizes="118px" alt="The Clear Out Crew home" width="900" height="321"></a><a class="back" href="/">Back to site</a></div></header>
<main class="wrap">
<h1>Page not found</h1>
<p class="meta">That page doesn't exist or has moved.</p>
<p>Need junk gone? Call or text <a href="tel:{TEL}">{PHONE}</a>, or <a href="/#quote">send photos for a free quote</a>.</p>
<h2>Popular pages</h2>
<ul>{links}</ul>
</main>
<footer class="wrap">© 2026 The Clear Out Crew · <a href="tel:{TEL}">{PHONE}</a> · <a href="mailto:theclearoutcrew718@gmail.com">theclearoutcrew718@gmail.com</a><br><a href='/privacy'>Privacy Policy</a> · <a href='/terms'>Terms of Use</a> · <a href='/accessibility'>Accessibility</a></footer>
</body>
</html>
"""
    (SITE / '404.html').write_text(doc)


def sitemap(urls):
    lastmod = '2026-10-25'
    body = ''.join(f'  <url><loc>{u}</loc><lastmod>{lastmod}</lastmod></url>\n' for u in urls)
    (SITE / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + '</urlset>\n')


if __name__ == '__main__':
    built = [page(pg) for pg in P.PAGES]
    not_found()
    sitemap([f'{D}/'] + built + [f'{D}/privacy', f'{D}/terms', f'{D}/accessibility'])
    print('built', len(built), 'pages + 404 + sitemap')
