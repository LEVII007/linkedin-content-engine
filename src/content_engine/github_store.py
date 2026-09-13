from __future__ import annotations

import urllib.parse
from typing import Any

from .http import HttpClient
from .models import Idea, StoredIdea


STATUS_LABELS = {
    "new": "content:new",
    "needs_context": "content:needs-context",
    "review": "content:review",
    "approved": "content:approved",
    "publishing": "content:publishing",
    "posted": "content:posted",
    "skipped": "content:skipped",
    "failed": "content:failed",
}


class GitHubStore:
    def __init__(self, token: str, repository: str, http: HttpClient | None = None):
        self.repository = repository
        self.http = http or HttpClient()
        self.base = f"https://api.github.com/repos/{repository}"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def ensure_labels(self) -> None:
        colors = {
            "new": "1d76db",
            "needs_context": "fbca04",
            "review": "d4c5f9",
            "approved": "0e8a16",
            "publishing": "0052cc",
            "posted": "5319e7",
            "skipped": "cfd3d7",
            "failed": "b60205",
        }
        for status, name in STATUS_LABELS.items():
            try:
                self.http.request(
                    "POST",
                    f"{self.base}/labels",
                    headers=self.headers,
                    json_body={
                        "name": name,
                        "color": colors[status],
                        "description": f"LinkedIn content status: {status}",
                    },
                )
            except Exception as error:
                if "422" not in str(error):
                    raise
        try:
            self.http.request(
                "POST",
                f"{self.base}/labels",
                headers=self.headers,
                json_body={
                    "name": "system:token-warning",
                    "color": "f9d0c4",
                    "description": "LinkedIn OAuth renewal warning",
                },
            )
        except Exception as error:
            if "422" not in str(error):
                raise

    def list(self, statuses: set[str] | None = None) -> list[StoredIdea]:
        _, _, issues = self.http.request(
            "GET",
            f"{self.base}/issues",
            headers=self.headers,
            query={"state": "all", "per_page": 100, "sort": "created", "direction": "asc"},
        )
        result: list[StoredIdea] = []
        for issue in issues:
            if "pull_request" in issue:
                continue
            try:
                idea = Idea.from_body(issue.get("body") or "")
            except (ValueError, KeyError):
                continue
            if statuses is None or idea.status in statuses:
                result.append(StoredIdea(issue["number"], idea))
        return result

    def find_by_slack_ts(self, slack_ts: str) -> StoredIdea | None:
        return next(
            (stored for stored in self.list() if stored.idea.slack_ts == slack_ts),
            None,
        )

    def create(self, idea: Idea) -> StoredIdea:
        title = idea.raw_text.replace("\n", " ").strip()[:90] or "Untitled thought"
        _, _, issue = self.http.request(
            "POST",
            f"{self.base}/issues",
            headers=self.headers,
            json_body={
                "title": f"Idea: {title}",
                "body": idea.to_body(),
                "labels": [STATUS_LABELS[idea.status]],
            },
        )
        return StoredIdea(issue["number"], idea)

    def update(self, stored: StoredIdea) -> None:
        self.http.request(
            "PATCH",
            f"{self.base}/issues/{stored.issue_number}",
            headers=self.headers,
            json_body={
                "body": stored.idea.to_body(),
                "labels": [STATUS_LABELS[stored.idea.status]],
                "state": "closed" if stored.idea.status in {"posted", "skipped"} else "open",
            },
        )

    def issue_url(self, number: int) -> str:
        return f"https://github.com/{self.repository}/issues/{number}"

    def token_warning_sent(self, expires_at: int) -> bool:
        title = f"LinkedIn token expires at {expires_at}"
        _, _, issues = self.http.request(
            "GET",
            f"{self.base}/issues",
            headers=self.headers,
            query={
                "state": "all",
                "labels": "system:token-warning",
                "per_page": 100,
            },
        )
        return any(issue.get("title") == title for issue in issues)

    def mark_token_warning_sent(self, expires_at: int) -> None:
        self.http.request(
            "POST",
            f"{self.base}/issues",
            headers=self.headers,
            json_body={
                "title": f"LinkedIn token expires at {expires_at}",
                "body": "Renew with `scripts/linkedin_auth_github.py`.",
                "labels": ["system:token-warning"],
            },
        )
