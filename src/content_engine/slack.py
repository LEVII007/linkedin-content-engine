from __future__ import annotations

from typing import Any

from .http import HttpClient


class SlackClient:
    def __init__(self, token: str, http: HttpClient | None = None):
        self.http = http or HttpClient()
        self.base = "https://slack.com/api"
        self.headers = {"Authorization": f"Bearer {token}"}

    def _get(self, method: str, **query: Any) -> dict[str, Any]:
        _, _, body = self.http.request(
            "GET",
            f"{self.base}/{method}",
            headers=self.headers,
            query=query,
        )
        self._check(method, body)
        return body

    def _post(self, method: str, payload: dict[str, Any]) -> dict[str, Any]:
        _, _, body = self.http.request(
            "POST",
            f"{self.base}/{method}",
            headers=self.headers,
            json_body=payload,
        )
        self._check(method, body)
        return body

    @staticmethod
    def _check(method: str, body: dict[str, Any]) -> None:
        if not body.get("ok"):
            raise RuntimeError(f"Slack {method} failed: {body.get('error', body)}")

    def history(self, channel: str, limit: int = 100) -> list[dict[str, Any]]:
        body = self._get("conversations.history", channel=channel, limit=limit)
        return body.get("messages", [])

    def replies(self, channel: str, thread_ts: str) -> list[dict[str, Any]]:
        body = self._get(
            "conversations.replies", channel=channel, ts=thread_ts, limit=100
        )
        return body.get("messages", [])[1:]

    def reactions(self, channel: str, timestamp: str) -> dict[str, set[str]]:
        try:
            body = self._get(
                "reactions.get", channel=channel, timestamp=timestamp, full="true"
            )
        except RuntimeError as error:
            if "no_reaction" in str(error):
                return {}
            raise
        message = body.get("message", {})
        return {
            reaction["name"]: set(reaction.get("users", []))
            for reaction in message.get("reactions", [])
        }

    def post(
        self, channel: str, text: str, *, thread_ts: str | None = None
    ) -> str:
        payload: dict[str, Any] = {"channel": channel, "text": text}
        if thread_ts:
            payload["thread_ts"] = thread_ts
        body = self._post("chat.postMessage", payload)
        return str(body["ts"])
