#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request

SERVICE = "linkedin-content-engine"
ACCOUNT = "access-token"
MAX_CHARS = 3000


def token() -> str:
    try:
        raw = subprocess.run(
            ["security", "find-generic-password", "-s", SERVICE, "-a", ACCOUNT, "-w"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except subprocess.CalledProcessError:
        sys.exit("No LinkedIn authorization. Run /linkedin-publish setup.")
    data = json.loads(raw)
    if int(data["expires_at"]) <= int(time.time()):
        sys.exit("LinkedIn authorization expired. Run /linkedin-publish setup.")
    return str(data["access_token"])


def api(path: str, access_token: str, payload=None):
    request = urllib.request.Request(
        f"https://api.linkedin.com{path}",
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={
            "Authorization": f"Bearer {access_token}",
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json",
        },
        method="POST" if payload is not None else "GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read()
            return response.status, response.headers, json.loads(raw or b"{}")
    except urllib.error.HTTPError as error:
        sys.exit(
            f"LinkedIn API {error.code}: "
            f"{error.read().decode(errors='replace')[:500]}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text-file", required=True)
    parser.add_argument("--i-am-approved", action="store_true")
    args = parser.parse_args()
    if not args.i_am_approved:
        sys.exit("Refusing to publish without explicit approval.")

    text = open(args.text_file, encoding="utf-8").read().strip()
    if not text or len(text) > MAX_CHARS:
        sys.exit(f"Draft must contain 1–{MAX_CHARS} characters.")

    access_token = token()
    _, _, profile = api("/v2/userinfo", access_token)
    person = profile.get("sub")
    if not person:
        sys.exit("LinkedIn did not return the authenticated member id.")
    payload = {
        "author": f"urn:li:person:{person}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        },
    }
    status, headers, _ = api("/v2/ugcPosts", access_token, payload)
    post_id = headers.get("X-RestLi-Id", "")
    if status != 201 or not post_id:
        sys.exit(
            "LinkedIn response was ambiguous. Check the profile before retrying."
        )
    print(f"https://www.linkedin.com/feed/update/{post_id}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
