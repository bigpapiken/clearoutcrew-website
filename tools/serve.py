"""Local server that mimics Netlify: /page -> page.html, /dir/ -> dir/index.html, 404.html on miss.
Usage: python3 tools/serve.py <port>"""
import http.server, os, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent / 'site'
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(s, *a, **k): super().__init__(*a, directory=str(ROOT), **k)
    def log_message(s, *a): pass
    def send_head(s):
        path = s.path.split('?')[0].split('#')[0]
        f = ROOT / path.lstrip('/')
        if path.endswith('/') and (f / 'index.html').exists(): return super().send_head()
        if f.is_dir() and (f / 'index.html').exists():
            s.send_response(301); s.send_header('Location', path + '/'); s.end_headers(); return None
        if not f.exists() and (ROOT / (path.lstrip('/') + '.html')).exists():
            s.path = path + '.html'; return super().send_head()
        if not f.exists():
            body = (ROOT / '404.html').read_bytes() if (ROOT / '404.html').exists() else b'404'
            s.send_response(404); s.send_header('Content-Type', 'text/html'); s.send_header('Content-Length', str(len(body))); s.end_headers()
            s.wfile.write(body); return None
        return super().send_head()
http.server.ThreadingHTTPServer(('127.0.0.1', int(sys.argv[1])), H).serve_forever()
