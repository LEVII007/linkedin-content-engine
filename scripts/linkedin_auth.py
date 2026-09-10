#!/usr/bin/env python3
"""One-time (per ~60 days) OAuth for LinkedIn Share-on-LinkedIn posting.

Opens the consent screen, catches the redirect on localhost, exchanges the code,
and stores the token in the macOS keychain. Nothing is written to disk.

Usage:
    export LINKEDIN_CLIENT_ID=...
    export LINKEDIN_CLIENT_SECRET=...
    ./linkedin_auth.py
"""
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

_result = {}


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        _result.update({k: v[0] for k, v in q.items()})
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        ok = "code" in _result
        self.wfile.write(
            b"<h2>Authorized. Close this tab.</h2>" if ok
            else b"<h2>Authorization failed. Check the terminal.</h2>"
        )

    def log_message(self, *a):
        pass


def keychain_set(value: str) -> None:
    subprocess.run(
        ["security", "add-generic-password", "-U", "-s", SERVICE, "-a", ACCOUNT, "-w", value],
        check=True,
    )


def main() -> int:
    cid = os.environ.get("LINKEDIN_CLIENT_ID")
    csec = os.environ.get("LINKEDIN_CLIENT_SECRET")
    if not cid or not csec:
        print("Set LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET first.", file=sys.stderr)
        return 2

    state = secrets.token_urlsafe(16)
    auth_url = "https://www.linkedin.com/oauth/v2/authorization?" + urllib.parse.urlencode(
        {
            "response_type": "code",
            "client_id": cid,
            "redirect_uri": REDIRECT,
            "state": state,
            "scope": SCOPES,
        }
    )

    server = http.server.HTTPServer(("localhost", 8765), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()

    print("Opening LinkedIn consent screen...")
    print(f"If nothing opens, visit:\n{auth_url}\n")
    webbrowser.open(auth_url)

    deadline = time.time() + 180
    while "code" not in _result and "error" not in _result and time.time() < deadline:
        time.sleep(0.3)
    server.shutdown()

    if "error" in _result:
        print(f"Denied: {_result.get('error')} {_result.get('error_description', '')}", file=sys.stderr)
        return 1
    if "code" not in _result:
        print("Timed out waiting for the redirect.", file=sys.stderr)
        return 1
    if _result.get("state") != state:
        print("State mismatch — aborting.", file=sys.stderr)
        return 1

    body = urllib.parse.urlencode(
        {
            "grant_type": "authorization_code",
            "code": _result["code"],
            "redirect_uri": REDIRECT,
            "client_id": cid,
            "client_secret": csec,
        }
    ).encode()
    req = urllib.request.Request(
        "https://www.linkedin.com/oauth/v2/accessToken",
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        tok = json.loads(resp.read())

    expires_at = int(time.time()) + int(tok.get("expires_in", 0))
    keychain_set(json.dumps({"access_token": tok["access_token"], "expires_at": expires_at}))

    days = int(tok.get("expires_in", 0)) // 86400
    print(f"Token stored in keychain (service: {SERVICE}).")
    print(f"Valid ~{days} days. Re-run this script when it expires.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
