"""Crawl the local site from / and check every page. Usage: python3 tools/qa_crawl.py [base]
Checks: status codes, unique titles/descriptions/H1s, canonical == crawled URL (production
form), robots meta, duplicate IDs, internal links + #anchors resolve, images exist and have
alt + width/height, JSON-LD parses and @id references resolve, sitemap matches indexable
canonicals, orphan pages."""
import json, re, sys, urllib.request, urllib.error, html
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8871'
PROD = 'https://clearoutcrewnyc.com'
problems, info = [], []


def get(url):
    try:
        r = urllib.request.urlopen(url)
        return r.status, r.read().decode('utf-8', 'replace'), r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', 'replace'), url


class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.links, s.ids, s.imgs, s.h1, s.in_h1, s.heads, s.cur = [], [], [], [], False, [], None
    def handle_starttag(s, t, a):
        a = dict(a)
        if 'id' in a: s.ids.append(a['id'])
        if t == 'a' and 'href' in a: s.links.append(a['href'])
        if t == 'img': s.imgs.append(a)
        if t in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'): s.cur = [t, '']
        if t == 'h1': s.in_h1 = True
    def handle_endtag(s, t):
        if s.cur and t == s.cur[0]: s.heads.append((s.cur[0], s.cur[1].strip())); s.cur = None
        if t == 'h1': s.in_h1 = False
    def handle_data(s, d):
        if s.cur: s.cur[1] += d


pages, queue, seen, inlinks = {}, ['/'], set(), {}
while queue:
    path = queue.pop(0)
    if path in seen: continue
    seen.add(path)
    st, body, final = get(BASE + path)
    if st != 200: problems.append(f'{path}: HTTP {st}'); continue
    p = P(); p.feed(body)
    pages[path] = (body, p)
    for href in p.links:
        u = urlparse(urljoin(BASE + path, href))
        if u.scheme in ('mailto', 'tel') or (u.netloc and u.netloc != urlparse(BASE).netloc): continue
        tgt = u.path or '/'
        inlinks.setdefault(tgt, set()).add(path)
        if tgt not in seen and not tgt.endswith(('.png', '.jpg', '.webp', '.xml', '.txt')): queue.append(tgt)

titles, descs, h1s = {}, {}, {}
ids_by_page = {p: set(v[1].ids) for p, v in pages.items()}
all_ids = {}
for path, (body, p) in pages.items():
    t = re.search(r'<title>(.*?)</title>', body, re.S); t = html.unescape(t.group(1)) if t else None
    d = re.search(r'<meta name="description" content="([^"]*)"', body); d = html.unescape(d.group(1)) if d else None
    c = re.search(r'<link rel="canonical" href="([^"]*)"', body); c = c.group(1) if c else None
    robots = re.search(r'<meta name="robots" content="([^"]*)"', body)
    noindex = bool(robots and 'noindex' in robots.group(1))
    if not t: problems.append(f'{path}: no <title>')
    if not d: problems.append(f'{path}: no meta description')
    titles.setdefault(t, []).append(path); descs.setdefault(d, []).append(path)
    if not noindex:
        want = PROD + (path if path != '/' else '/')
        if c != want: problems.append(f'{path}: canonical {c} != {want}')
    h = [x for x in p.heads if x[0] == 'h1']
    if len(h) != 1: problems.append(f'{path}: {len(h)} H1s')
    for x in h: h1s.setdefault(x[1], []).append(path)
    # heading order: no skipped levels (h2 -> h4)
    last = 1
    for tag, txt in p.heads:
        lvl = int(tag[1])
        if lvl > last + 1: problems.append(f'{path}: heading jump h{last} -> {tag} "{txt[:40]}"')
        last = lvl
    dup = {i for i in p.ids if p.ids.count(i) > 1}
    if dup: problems.append(f'{path}: duplicate ids {dup}')
    for href in p.links:
        u = urlparse(urljoin(BASE + path, href))
        if u.scheme in ('mailto', 'tel') or (u.netloc and u.netloc != urlparse(BASE).netloc): continue
        tgt = u.path or '/'
        if u.fragment and u.fragment != 'main':
            if tgt in ids_by_page and u.fragment not in ids_by_page[tgt]: problems.append(f'{path}: link {href} -> missing #{u.fragment}')
    for im in p.imgs:
        if 'alt' not in im: problems.append(f'{path}: img without alt {im.get("src")}')
        if not ('width' in im and 'height' in im): problems.append(f'{path}: img without width/height {im.get("src")}')
        for src in [im.get('src')] + [s.strip().split(' ')[0] for s in im.get('srcset', '').split(',') if s.strip()]:
            if src and get(urljoin(BASE + path, src))[0] != 200: problems.append(f'{path}: missing image {src}')
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', body, re.S):
        try: data = json.loads(m.group(1))
        except Exception as e: problems.append(f'{path}: JSON-LD parse error {e}'); continue
        nodes = data.get('@graph', [data])
        defined = {n.get('@id') for n in nodes}
        refs = set(re.findall(r'"@id": "([^"]+)"', json.dumps(data)))
        for r in refs - defined:
            problems.append(f'{path}: JSON-LD @id reference not defined on page: {r}')
        for n in nodes:
            if n.get('@type') == 'FAQPage':
                vis = len(re.findall(r'<details><summary>', body))
                if vis != len(n['mainEntity']): problems.append(f'{path}: FAQPage has {len(n["mainEntity"])} Qs, page shows {vis}')
    info.append((path, t, len(t or ''), len(d or ''), noindex))

for k, v in titles.items():
    if len(v) > 1: problems.append(f'duplicate title {k!r}: {v}')
for k, v in descs.items():
    if len(v) > 1: problems.append(f'duplicate description: {v}')
for k, v in h1s.items():
    if len(v) > 1: problems.append(f'duplicate H1 {k!r}: {v}')

# sitemap vs indexable canonicals
st, sm, _ = get(BASE + '/sitemap.xml')
locs = re.findall(r'<loc>(.*?)</loc>', sm)
indexable = set()
for p, (b, _) in pages.items():
    r = re.search(r'<meta name="robots" content="([^"]*)"', b)
    if not (r and 'noindex' in r.group(1)): indexable.add(PROD + p)
for l in locs:
    if l not in indexable: problems.append(f'sitemap URL not an indexable crawled page: {l}')
for u in indexable - set(locs): problems.append(f'indexable page missing from sitemap: {u}')
st, rb, _ = get(BASE + '/robots.txt')
if 'Sitemap: https://clearoutcrewnyc.com/sitemap.xml' not in rb: problems.append('robots.txt sitemap line missing')
# 404 behaviour
st, b404, _ = get(BASE + '/definitely-not-a-page')
if st != 404: problems.append(f'404 page returns {st}')

print(f'{"page":40} {"title len":>9} {"desc len":>8}  noindex')
for path, t, tl, dl, ni in sorted(info):
    print(f'{path:40} {tl:9} {dl:8}  {"yes" if ni else ""}')
print(f'\ncrawled {len(pages)} pages, sitemap {len(locs)} URLs')
print('\n'.join('PROBLEM: ' + x for x in problems) if problems else 'NO PROBLEMS')
