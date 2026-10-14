"""Сборка app.html и локальный сервер без Streamlit."""
from __future__ import annotations

import argparse
import functools
import http.server
import socketserver
import sys
import threading
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
APP_HTML = ASSETS / "app.html"


def build() -> Path:
    sys.path.insert(0, str(ROOT))
    from dashboards import build_unified_html

    ASSETS.mkdir(exist_ok=True)
    html = build_unified_html()
    APP_HTML.write_text(html, encoding="utf-8")
    print(f"built {APP_HTML} ({APP_HTML.stat().st_size} bytes)")
    return APP_HTML


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8511)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()

    build()

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(ASSETS), **kw)

        def log_message(self, fmt, *args):  # quieter
            sys.stderr.write("[%s] %s\n" % (self.log_date_time_string(), fmt % args))

        def do_GET(self):
            if self.path in ("/", "/index.html"):
                self.path = "/app.html"
            return super().do_GET()

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", args.port), Handler) as httpd:
        url = f"http://127.0.0.1:{args.port}/app.html"
        print(f"serving {url}")
        if not args.no_browser:
            threading.Timer(0.4, functools.partial(webbrowser.open, url)).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
