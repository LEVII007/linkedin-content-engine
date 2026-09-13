from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


class ApiError(RuntimeError):
    def __init__(self, service: str, status: int, body: str):
        super().__init__(f"{service} API {status}: {body[:500]}")
        self.service = service
        self.status = status
        self.body = body


class HttpClient:
    def request(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        query: dict[str, Any] | None = None,
        json_body: Any | None = None,
        form: dict[str, Any] | None = None,
    ) -> tuple[int, dict[str, str], Any]:
        if query:
            encoded = urllib.parse.urlencode(query)
            url = f"{url}{'&' if '?' in url else '?'}{encoded}"

        data = None
        request_headers = dict(headers or {})
        if json_body is not None:
            data = json.dumps(json_body).encode()
            request_headers.setdefault("Content-Type", "application/json")
        elif form is not None:
            data = urllib.parse.urlencode(form).encode()
            request_headers.setdefault(
                "Content-Type", "application/x-www-form-urlencoded"
            )

        request = urllib.request.Request(
            url, data=data, headers=request_headers, method=method
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                raw = response.read()
                body = self._decode(raw, response.headers.get("Content-Type", ""))
                return response.status, dict(response.headers.items()), body
        except urllib.error.HTTPError as error:
            raw = error.read().decode(errors="replace")
            raise ApiError(self._service(url), error.code, raw) from error
        except urllib.error.URLError as error:
            raise RuntimeError(f"{self._service(url)} request failed: {error}") from error

    @staticmethod
    def _decode(raw: bytes, content_type: str) -> Any:
        if not raw:
            return {}
        text = raw.decode(errors="replace")
        if "json" in content_type:
            return json.loads(text)
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return text

    @staticmethod
    def _service(url: str) -> str:
        return urllib.parse.urlparse(url).netloc
