import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).parent
ENV = dict(l.split("=", 1) for l in (ROOT / ".env").read_text().split() if "=" in l)
KEYS = ["SAMVAAD_API_KEY", "ORG_ID", "WORKSPACE_ID", "APP_ID"]


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/config.json":
            # ponytail: key goes to the browser; fine on localhost, proxy it server-side before sharing publicly
            body = json.dumps({k: ENV.get(k, "") for k in KEYS}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)
        elif self.path in ("/", "/index.html"):
            self.path = "/index.html"
            super().do_GET()
        else:
            self.send_error(404)


if __name__ == "__main__":
    missing = [k for k in KEYS if not ENV.get(k)]
    if missing:
        print("Missing in .env:", ", ".join(missing))
    print("Open http://localhost:8000")
    HTTPServer(("127.0.0.1", 8000), lambda *a: Handler(*a, directory=str(ROOT))).serve_forever()
