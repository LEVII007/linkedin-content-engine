from __future__ import annotations

import time
from dataclasses import dataclass

from .http import HttpClient


@dataclass(frozen=True)
class PublishResult:
    post_id: str
    permalink: str


class LinkedInPublisher:
    def __init__(
        self,
        access_token: str,
        person_urn: str,
        expires_at: int,
        http: HttpClient | None = None,
    ):
        self.access_token = access_token
        self.person_urn = person_urn
        self.expires_at = expires_at
        self.http = http or HttpClient()

    @property
    def days_until_expiry(self) -> int:
        return max(0, (self.expires_at - int(time.time())) // 86400)

    def publish(self, text: str) -> PublishResult:
        if int(time.time()) >= self.expires_at:
            raise RuntimeError("LinkedIn token has expired")
        if not self.person_urn.startswith("urn:li:person:"):
            raise ValueError("LINKEDIN_PERSON_URN must start with urn:li:person:")

        payload = {
            "author": self.person_urn,
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
        status, headers, _ = self.http.request(
            "POST",
            "https://api.linkedin.com/v2/ugcPosts",
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "X-Restli-Protocol-Version": "2.0.0",
                "Content-Type": "application/json",
            },
            json_body=payload,
        )
        if status != 201:
            raise RuntimeError(f"LinkedIn returned HTTP {status}, expected 201")
        post_id = headers.get("X-RestLi-Id", "")
        if not post_id:
            raise RuntimeError(
                "LinkedIn returned 201 without X-RestLi-Id; refusing to mark posted"
            )
        return PublishResult(
            post_id=post_id,
            permalink=f"https://www.linkedin.com/feed/update/{post_id}/",
        )
