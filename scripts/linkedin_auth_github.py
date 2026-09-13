#!/usr/bin/env python3
"""Authorize Supreet and store the LinkedIn token as a GitHub Actions secret.

Run locally. The token is sent directly to GitHub through `gh secret set`; it is
never printed or written to this repository.
"""
import argparse
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

REDIRECT = "http://localhost:8765/callback"
SCOPES = "openid profile w_member_social"
RESULT: dict[str, str] = {}


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        RESULT.update({key: value[0] for key, value in query.items()})
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        message = (
            b"<h2>Authorized. You can close this tab.</h2>"
            if "code" in RESULT
            else b"<h2>Authorization failed. Return to the terminal.</h2>"
        )
        self.wfile.write(message)

    def log_message(self, *_):
        pass


def exchange(client_id: str, client_secret: str) -> tuple[str, int, str]:
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
    print("Opening LinkedIn. Supreet must complete this consent screen himself.")
    webbrowser.open(url)
    deadline = time.time() + 300
    while not ({"code", "error"} & RESULT.keys()) and time.time() < deadline:
        time.sleep(0.3)
    server.shutdown()
    if RESULT.get("state") != state:
        raise RuntimeError("OAuth state mismatch")
    if "code" not in RESULT:
        raise RuntimeError(
            f"OAuth failed: {RESULT.get('error_description', 'timed out')}"
        )

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
        token_data = json.loads(response.read())
    access_token = token_data["access_token"]
    expires_at = int(time.time()) + int(token_data["expires_in"])

    profile_request = urllib.request.Request(
        "https://api.linkedin.com/v2/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    with urllib.request.urlopen(profile_request, timeout=30) as response:
        profile = json.loads(response.read())
    return access_token, expires_at, f"urn:li:person:{profile['sub']}"


def gh(*args: str, stdin: str | None = None) -> None:
    subprocess.run(["gh", *args], input=stdin, text=True, check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, help="owner/private-repository")
    args = parser.parse_args()
    client_id = os.getenv("LINKEDIN_CLIENT_ID", "").strip()
    client_secret = os.getenv("LINKEDIN_CLIENT_SECRET", "").strip()
    if not client_id or not client_secret:
        sys.exit("Set LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET first.")

    token, expires_at, person_urn = exchange(client_id, client_secret)
    gh(
        "secret",
        "set",
        "LINKEDIN_ACCESS_TOKEN",
        "--repo",
        args.repo,
        "--body",
        token,
    )
    gh(
        "variable",
        "set",
        "LINKEDIN_PERSON_URN",
        "--repo",
        args.repo,
        "--body",
        person_urn,
    )
    gh(
        "variable",
        "set",
        "LINKEDIN_TOKEN_EXPIRES_AT",
        "--repo",
        args.repo,
        "--body",
        str(expires_at),
    )
    print("LinkedIn token and profile URN stored in GitHub. Token was not printed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
