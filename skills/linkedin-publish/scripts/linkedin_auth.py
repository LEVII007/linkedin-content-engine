#!/usr/bin/env python3
import http.server
import json
import os
import secrets
import subprocess
import sys
import threading
import time
import urllib.parse
import urllib.request
import webbrowser

SERVICE = "linkedin-content-engine"
ACCOUNT = "access-token"
REDIRECT = "http://localhost:8765/callback"
SCOPES = "openid profile w_member_social"
RESULT: dict[str, str] = {}


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        values = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        RESULT.update({key: value[0] for key, value in values.items()})
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(
            b"<h2>Authorized. Close this tab.</h2>"
            if "code" in RESULT
            else b"<h2>Authorization failed. Return to Claude.</h2>"
        )

    def log_message(self, *_):
        pass


def main() -> int:
    client_id = os.getenv("LINKEDIN_CLIENT_ID", "").strip()
    client_secret = os.getenv("LINKEDIN_CLIENT_SECRET", "").strip()
    if not client_id or not client_secret:
        sys.exit("Set LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET first.")

    state = secrets.token_urlsafe(24)
    url = "https://www.linkedin.com/oauth/v2/authorization?" + urllib.parse.urlencode(
        {
            "response_type": "code",
            "client_id": client_id,
            "redirect_uri": REDIRECT,
            "state": state,
            "scope": SCOPES,
        }
    )
    server = http.server.HTTPServer(("localhost", 8765), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print("Opening LinkedIn consent screen...")
    webbrowser.open(url)
    deadline = time.time() + 300
    while not ({"code", "error"} & RESULT.keys()) and time.time() < deadline:
        time.sleep(0.3)
    server.shutdown()
    if RESULT.get("state") != state:
        sys.exit("OAuth state mismatch.")
    if "code" not in RESULT:
        sys.exit(f"OAuth failed: {RESULT.get('error_description', 'timed out')}")

    request = urllib.request.Request(
        "https://www.linkedin.com/oauth/v2/accessToken",
        data=urllib.parse.urlencode(
            {
                "grant_type": "authorization_code",
                "code": RESULT["code"],
                "redirect_uri": REDIRECT,
                "client_id": client_id,
                "client_secret": client_secret,
            }
        ).encode(),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        token = json.loads(response.read())
    value = json.dumps(
        {
            "access_token": token["access_token"],
            "expires_at": int(time.time()) + int(token["expires_in"]),
        }
    )
    subprocess.run(
        [
            "security",
            "add-generic-password",
            "-U",
            "-s",
            SERVICE,
            "-a",
            ACCOUNT,
            "-w",
            value,
        ],
        check=True,
    )
    print("LinkedIn authorization stored in the macOS keychain.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
