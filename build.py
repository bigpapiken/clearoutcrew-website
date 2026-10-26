"""Build The Clear Out Crew site.

  src/index.html   -> the page body (also published as-is for the preview link)
  dist/            -> production site for Netlify (full <head>, SEO, schema, live form)

Set DOMAIN once Jack buys his domain, then re-run:  python3 build.py
"""
import json, pathlib, re, shutil

DOMAIN = "https://clearoutcrewnyc.com"
PHONE_DISPLAY = "(917) 533-3220"
PHONE_E164 = "+19175333220"
EMAIL = "theclearoutcrew718@gmail.com"
UPDATED = "October 2026"

ROOT = pathlib.Path(__file__).parent
SRC, DIST = ROOT / "src", ROOT / "dist"
IMG = ROOT / "site" / "img"

DESCRIPTION = ("Junk removal and property cleanouts in Brooklyn, Queens, Manhattan, the Bronx and "
               "Staten Island. Furniture, appliances, apartments, estates, storage units and commercial "
               f"jobs. Free estimates. Call {PHONE_DISPLAY}.")
TITLE = "Junk Removal NYC & Property Cleanouts | The Clear Out Crew"

# ---------- shared styles for the small pages ----------
DOC_CSS = """
:root{--ink:#151513;--paper:#ecebe5;--line:#cfccc2;--yellow:#e1ae15;--muted:#5d5b53;--cream:#f4f1e8;color-scheme:light}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:400 17px/1.65 "Barlow","Helvetica Neue",Arial,sans-serif}
header{background:var(--ink);border-bottom:6px solid var(--yellow)}
.wrap{max-width:780px;margin-inline:auto;padding-left:max(20px,env(safe-area-inset-left,0px));padding-right:max(20px,env(safe-area-inset-right,0px))}
header .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:72px}
header img{height:42px;width:auto;display:block}
header a.back{color:var(--cream);font:700 1rem/1 "Barlow Condensed","Arial Narrow",sans-serif;letter-spacing:.06em;text-transform:uppercase;text-decoration:none}
main{padding-block:48px 72px}
h1{font:800 clamp(2.4rem,7vw,3.6rem)/.95 "Big Shoulders Stencil Display","Saira Stencil One","Barlow Condensed",Impact,sans-serif;text-transform:uppercase;margin:0 0 8px}
h2{font:700 1.35rem/1.2 "Barlow Condensed","Arial Narrow",sans-serif;letter-spacing:.03em;text-transform:uppercase;margin:36px 0 8px}
p,li{max-width:68ch}.meta{color:var(--muted);margin:0 0 28px}
a{color:var(--ink)}a:focus-visible{outline:3px solid var(--ink);outline-offset:3px}
footer{border-top:1px solid var(--line);padding-block:24px 40px;color:var(--muted);font-size:.92rem}
"""
FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Stencil+Display:wght@800&display=swap">\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Saira+Stencil+One&display=swap">\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;600;700&family=Barlow+Condensed:wght@700&display=swap">')

def doc_page(slug, title, heading, body_html, noindex=False):
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} | The Clear Out Crew</title>
<meta name="description" content="{title} for The Clear Out Crew, junk removal in New York City.">
{robots}<link rel="canonical" href="{DOMAIN}/{slug}">
<link rel="icon" href="img/icon-32.png" sizes="32x32">
{FONTS}
<style>{DOC_CSS}</style>
</head>
<body>
<header><div class="wrap"><a href="index.html"><img src="img/logo.webp" alt="The Clear Out Crew home" width="900" height="321"></a><a class="back" href="index.html">Back to site</a></div></header>
<main class="wrap">
<h1>{heading}</h1>
{body_html}
</main>
<footer class="wrap">© 2026 The Clear Out Crew · <a href="tel:{PHONE_E164}">{PHONE_DISPLAY}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></footer>
</body>
</html>
"""

PRIVACY = f"""<p class="meta">Last updated: {UPDATED}</p>
<p>This policy explains what information The Clear Out Crew ("we", "us") collects through this website, how we use it, and the choices you have.</p>

<h2>What we collect</h2>
<p>When you request a quote, we collect the information you enter: your name, phone number, email address (if you give one), the job location or ZIP code, a description of the job, your preferred date, how you'd like to be contacted, and any photos you upload.</p>
<p>Like most websites, our hosting provider automatically records basic technical information such as your IP address, browser type and the pages you visit. If we use website analytics (such as Google Analytics), it collects similar usage information using cookies.</p>

<h2>How we use it</h2>
<ul>
<li>To review your job, prepare an estimate and contact you about it.</li>
<li>To schedule and complete the work you book with us.</li>
<li>To keep records of our jobs and communications.</li>
<li>To understand how people use our website and improve it.</li>
</ul>
<p>We don't sell your personal information. We won't post photos you send us online or in our marketing without asking you first.</p>

<h2>Calls and text messages</h2>
<p>If you give us your phone number, we may call or text you about your quote and job. We don't send marketing texts without your consent, and we don't share your phone number with third parties for their marketing. Reply STOP to any text from us to stop receiving texts.</p>

<h2>Who we share it with</h2>
<p>We share information only with service providers that help us run the business, such as our website host and form provider, email provider and analytics provider, and only so they can provide those services. We may also disclose information if required by law.</p>

<h2>Cookies and analytics</h2>
<p>This website doesn't use advertising cookies. If analytics is enabled, it uses cookies to measure visits. You can block or delete cookies in your browser settings, and you can opt out of Google Analytics at <a href="https://tools.google.com/dlpage/gaoptout" rel="noopener">tools.google.com/dlpage/gaoptout</a>.</p>

<h2>How long we keep it</h2>
<p>We keep quote requests and photos only as long as we need them to respond to you, complete your job and keep normal business records.</p>

<h2>Your choices</h2>
<p>You can ask us to see, correct or delete the personal information you've sent us. Email <a href="mailto:{EMAIL}">{EMAIL}</a> or call <a href="tel:{PHONE_E164}">{PHONE_DISPLAY}</a> and we'll take care of it.</p>

<h2>Security</h2>
<p>This website uses an encrypted (HTTPS) connection, and we limit access to your information to the people who need it. No website or email system is completely secure, so please don't send sensitive information such as financial or ID details through the quote form.</p>

<h2>Children</h2>
<p>This website is meant for adults arranging junk removal. We don't knowingly collect information from children under 13.</p>

<h2>Changes</h2>
<p>We may update this policy. The date at the top shows when it last changed.</p>

<h2>Contact</h2>
<p>The Clear Out Crew<br><a href="tel:{PHONE_E164}">{PHONE_DISPLAY}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
"""

TERMS = f"""<p class="meta">Last updated: {UPDATED}</p>
<p>By using this website, you agree to these terms. If you don't agree, please don't use the site.</p>

<h2>About this website</h2>
<p>This website gives general information about The Clear Out Crew's junk removal and cleanout services and lets you request a quote. Information on the site, including service descriptions and service areas, may change without notice.</p>

<h2>Quotes and estimates</h2>
<p>Estimates are free and based on the information and photos you provide. A quote request does not book a job. Final pricing and scheduling are confirmed directly with you before any work begins, and may change if the job differs from what was described.</p>

<h2>Items we can take</h2>
<p>Some items and materials, such as hazardous waste, may require special handling or may not be accepted. We'll confirm what we can remove when we give your estimate.</p>

<h2>Your submissions</h2>
<p>When you send a quote request or photos, you confirm the information is accurate and that you have the right to share the photos. We handle your information as described in our <a href="privacy.html">Privacy Policy</a>.</p>

<h2>Website content</h2>
<p>The text, logo and photos on this website belong to The Clear Out Crew and may not be copied or reused without permission.</p>

<h2>Limitation of liability</h2>
<p>This website is provided "as is". To the extent allowed by law, The Clear Out Crew is not liable for any damages arising from your use of the website. These terms don't limit any rights you have under applicable law, and they don't cover the terms of a booked job, which are agreed separately.</p>

<h2>Governing law</h2>
<p>These terms are governed by the laws of the State of New York.</p>

<h2>Contact</h2>
<p>Questions about these terms? Call <a href="tel:{PHONE_E164}">{PHONE_DISPLAY}</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
"""

THANKS = f"""<p class="meta">We got your request.</p>
<p>Thanks for reaching out. We'll review your job and get back to you with a free estimate. If it's urgent, call or text <a href="tel:{PHONE_E164}">{PHONE_DISPLAY}</a>.</p>
<p><a href="index.html">Back to the website</a></p>
"""

def schema():
    boroughs = ["Brooklyn", "Queens", "Manhattan", "Bronx", "Staten Island"]
    services = ["Residential junk removal", "Furniture and appliance removal", "Apartment and house cleanouts",
                "Estate cleanouts", "Storage unit cleanouts", "Commercial junk removal",
                "Construction debris removal", "Property management cleanouts", "Real estate cleanouts",
                "Subcontracting and large-scale removal projects"]
    data = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": f"{DOMAIN}/#business",
        "name": "The Clear Out Crew",
        "description": "Junk removal, waste hauling and property cleanouts for homes and businesses across New York City.",
        "url": f"{DOMAIN}/",
        "telephone": PHONE_E164,
        "email": EMAIL,
        "image": f"{DOMAIN}/img/og-image.jpg",
        "logo": f"{DOMAIN}/img/icon-512.png",
        "areaServed": [{"@type": "Place", "name": f"{b}, NY"} for b in boroughs] + [{"@type": "City", "name": "New York City"}],
        "hasOfferCatalog": {
            "@type": "OfferCatalog", "name": "Junk removal services",
            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s}} for s in services],
        },
    }
    return json.dumps(data, indent=1)

def head(extra_css_and_links):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{TITLE}</title>
<meta name="description" content="{DESCRIPTION}">
<link rel="canonical" href="{DOMAIN}/">
<meta name="theme-color" content="#151513">
<link rel="icon" href="img/icon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="img/icon-180.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="The Clear Out Crew">
<meta property="og:title" content="The Clear Out Crew | NYC Junk Removal & Cleanouts">
<meta property="og:description" content="Junk removal and property cleanouts across all five boroughs. Send photos for a free estimate.">
<meta property="og:url" content="{DOMAIN}/">
<meta property="og:image" content="{DOMAIN}/img/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<!-- ANALYTICS: paste the Google Analytics (GA4) tag here once Jack's GA property exists. -->
<script type="application/ld+json">
{schema()}
</script>
{extra_css_and_links}
</head>
<body>
"""

def build():
    if DIST.exists():
        shutil.rmtree(DIST)
    (DIST / "img").mkdir(parents=True)
    for f in IMG.iterdir():
        shutil.copy(f, DIST / "img" / f.name)

    src = (SRC / "index.html").read_text()
    cut = src.index('<a class="skip"')
    top, body = src[:cut], src[cut:]
    # keep only <link> and <style> from the fragment's top for the real <head>
    keep = "\n".join(re.findall(r"<link[^>]*>", top)) + "\n" + re.search(r"<style>.*?</style>", top, re.S).group(0)
    body = body.replace('data-netlify="true"', 'data-netlify="true" data-live="true"')
    (DIST / "index.html").write_text(head(keep) + body + "\n</body>\n</html>\n")

    pages = {"privacy.html": ("Privacy Policy", "Privacy policy", PRIVACY, False),
             "terms.html": ("Terms of Use", "Terms of use", TERMS, False),
             "thanks.html": ("Request received", "Thanks!", THANKS, True)}
    for slug, (t, h, b, ni) in pages.items():
        html = doc_page(slug, t, h, b, ni)
        (DIST / slug).write_text(html)
        (ROOT / "site" / slug).write_text(html)   # same pages for the preview link

    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    urls = ["/", "/privacy.html", "/terms.html"]
    (DIST / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{DOMAIN}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    (DIST / "netlify.toml").write_text("""[[headers]]
  for = "/*"
  [headers.values]
    X-Content-Type-Options = "nosniff"
    X-Frame-Options = "DENY"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Permissions-Policy = "camera=(), microphone=(), geolocation=()"

[[headers]]
  for = "/img/*"
  [headers.values]
    Cache-Control = "public, max-age=2592000"
""")
    print("built", sorted(p.name for p in DIST.iterdir()))

if __name__ == "__main__":
    build()
