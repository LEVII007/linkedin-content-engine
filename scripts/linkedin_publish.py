#!/usr/bin/env python3
"""Publish one approved post to the authenticated member's LinkedIn profile.

Refuses to run without an explicit --i-am-approved flag, which the task sets only
after reading Status == "Approved" from the Notion queue. There is no code path
that publishes an unapproved draft.

Usage:
    ./linkedin_publish.py --dry-run
    ./linkedin_publish.py --text-file draft.txt --i-am-approved
    ./linkedin_publish.py --text-file draft.txt --link https://... --i-am-approved
"""
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
            check=True, capture_output=True, text=True,
        ).stdout.strip()
    except subprocess.CalledProcessError:
        sys.exit("No token in keychain. Run scripts/linkedin_auth.py first.")

    data = json.loads(raw)
    left = data["expires_at"] - int(time.time())
    if left <= 0:
        sys.exit("Token expired. Run scripts/linkedin_auth.py to re-authorize.")
    if left < 7 * 86400:
        print(f"WARNING: token expires in {left // 86400} days.", file=sys.stderr)
    return data["access_token"]


def api(path: str, tok: str, payload=None):
    req = urllib.request.Request(
        f"https://api.linkedin.com{path}",
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={
            "Authorization": f"Bearer {tok}",
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json",
        },
        method="POST" if payload is not None else "GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.headers, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        sys.exit(f"LinkedIn API {e.code}: {e.read().decode(errors='replace')[:500]}")


def author_urn(tok: str) -> str:
    _, _, me = api("/v2/userinfo", tok)
    sub = me.get("sub")
    if not sub:
        sys.exit(f"Could not read member id from /v2/userinfo: {me}")
    return f"urn:li:person:{sub}"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--text-file", help="plain-text file holding the post body")
    p.add_argument("--link", help="optional URL to attach as an article share")
    p.add_argument("--visibility", default="PUBLIC", choices=["PUBLIC", "CONNECTIONS"])
    p.add_argument("--dry-run", action="store_true", help="verify auth, print payload, post nothing")
    p.add_argument(
        "--i-am-approved",
        action="store_true",
        help="required to actually publish; set only for a row the human marked Approved",
    )
    a = p.parse_args()

    tok = token()
    urn = author_urn(tok)

    if a.dry_run and not a.text_file:
        print(f"Auth OK. Author URN: {urn}")
        return 0

    if not a.text_file:
        sys.exit("--text-file is required unless --dry-run is used alone.")

    text = open(a.text_file, encoding="utf-8").read().strip()
    if not text:
        sys.exit("Draft is empty — refusing to publish.")
    if len(text) > MAX_CHARS:
        sys.exit(f"Draft is {len(text)} chars; LinkedIn's limit is {MAX_CHARS}.")

    content = {"shareCommentary": {"text": text}, "shareMediaCategory": "NONE"}
    if a.link:
        content["shareMediaCategory"] = "ARTICLE"
        content["media"] = [{"status": "READY", "originalUrl": a.link}]

    payload = {
        "author": urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {"com.linkedin.ugc.ShareContent": content},
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": a.visibility},
    }

    if a.dry_run:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        print("\n--dry-run: nothing published.")
        return 0

    if not a.i_am_approved:
        sys.exit("Refusing to publish without --i-am-approved. Only pass this for an Approved row.")

    status, headers, _ = api("/v2/ugcPosts", tok, payload)
    post_id = headers.get("X-RestLi-Id", "")
    print(f"HTTP {status}")
    print(f"Post id: {post_id}")
    if post_id:
        print(f"Permalink: https://www.linkedin.com/feed/update/{post_id}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
