"""Copy lint over the rendered HTML: python3 build/copylint.py"""
import glob, os, re, html, sys
ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'site')
BANNED = ["elevate", "transform your", "unlock", "next level", "trusted partner", "unparalleled", "state-of-the-art", "world-class", "we understand",
          "we pride ourselves", "rest assured", "peace of mind", "seamless", "robust", "leverage", "bespoke", "curated", "testament to", "boasts", "nestled",
          "in today's", "whether you're", "welcome to", "look no further", "one-stop", "hassle-free", "top-notch", "second to none", "lorem", "delve"]
UK = ["colour", "grey", "tyre", "odour", "labour", "centre", "catalogue", "enquir", "organis", "neighbour", "metre", "favourite"]
UNCON = [r"(?<!where )(?<!wherever )\bit is\b", r"\bdo not\b", r"(?<!when )\byou are\b", r"\bwe will\b", r"\bdoes not\b", r"\bcannot\b", r"\bwe are\b", r"\byou will\b", r"\bthat is\b", r"\bis not\b", r"\bwe have\b", r"\bwill not\b"]
bad = 0
h1s = {}
for f in sorted(glob.glob(ROOT + '/**/*.html', recursive=True)):
    if '/build/' in f or '/node_modules/' in f: continue
    rel = f.replace(ROOT, '')
    legal = 'privacy' in f or 'terms' in f
    if '/src-img/' in f or '/qa/' in f: continue
    d = open(f, encoding='utf-8').read()
    body = re.sub(r'<(script|style)[\s\S]*?</\1>', ' ', d)
    body = re.sub(r'<header[\s\S]*?</header>|<footer[\s\S]*?</footer>|<div class="menu"[\s\S]*?</nav>|<blockquote[\s\S]*?</blockquote>|<figcaption[\s\S]*?</figcaption>', ' ', body)
    txt = html.unescape(re.sub(r'<[^>]+>', '. ', body)).replace('’', "'")
    low = txt.lower()
    out = []
    if '—' in body or '–' in body: out.append('dash')
    if '&amp;amp;' in d: out.append('double-escaped entity')
    for b in BANNED:
        if b in low: out.append('banned: ' + b)
    for u in UK:
        if u in low: out.append('UK spelling: ' + u)
    if not legal:
        for u in UNCON:
            m = re.search(u, low)
            if m: out.append('uncontracted: ' + low[max(0, m.start() - 30):m.end() + 20].strip())
    for s in re.split(r'(?<=[.!?])\s+', txt):
        n = len(s.split())
        if n > 34 and not legal: out.append('long sentence (%d): %s...' % (n, s[:70]))
    if txt.count('!') > 0: out.append('exclamation marks: %d' % txt.count('!'))
    m = re.search(r'<h1[^>]*>([\s\S]*?)</h1>', d)
    if m:
        h = re.sub(r'<[^>]+>', '', m.group(1)); h1s.setdefault(h, []).append(rel)
    t = re.search(r'<title>(.*?)</title>', d).group(1); desc = re.search(r'name="description" content="(.*?)"', d).group(1)
    if len(html.unescape(t)) > 68: out.append('title %d chars' % len(html.unescape(t)))
    if not (70 <= len(html.unescape(desc)) <= 165) and 'thank' not in f and '404' not in f: out.append('meta description %d chars' % len(html.unescape(desc)))
    if out:
        bad += 1; print(rel); [print('   ', o) for o in out]
for h, fs in h1s.items():
    if len(fs) > 1: bad += 1; print('duplicate H1:', h, fs)
print('copylint:', 'clean' if not bad else '%d files flagged' % bad)
