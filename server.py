import re
import urllib.error
import urllib.request
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).parent
ENV = dict(l.split("=", 1) for l in (ROOT / ".env").read_text().split() if "=" in l)
SARVAM = "https://apps.sarvam.ai/api/app-runtime/"
# Only the signed-URL endpoint is proxied; same rule as netlify/functions/api.mjs
ALLOWED = re.compile(r"^/api/(orgs/[\w-]+/workspaces/[\w-]+/apps/[\w-]+/url(\?.*)?)$")


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        m = ALLOWED.match(self.path)
        if m:
            req = urllib.request.Request(SARVAM + m[1], headers={"X-API-Key": ENV["SAMVAAD_API_KEY"]})
            try:
                with urllib.request.urlopen(req) as r:
                    status, body = r.status, r.read()
            except urllib.error.HTTPError as e:
                status, body = e.code, e.read()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)
        elif self.path in ("/", "/index.html"):
            self.path = "/index.html"
            super().do_GET()
        else:
            self.send_error(404)


if __name__ == "__main__":
    print("Open http://localhost:8000")
    HTTPServer(("127.0.0.1", 8000), lambda *a: Handler(*a, directory=str(ROOT))).serve_forever()
