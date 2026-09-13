from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .http import HttpClient
from .models import DraftDecision


class Writer:
    def __init__(
        self,
        api_key: str,
        model: str,
        root: Path,
        http: HttpClient | None = None,
    ):
        self.api_key = api_key
        self.model = model
        self.root = root
        self.http = http or HttpClient()

    def create_draft(
        self,
        raw_text: str,
        thread_text: list[str],
        *,
        previous_draft: str = "",
        edit_request: str = "",
    ) -> DraftDecision:
        voice = (self.root / "references" / "voice-supreet.md").read_text()
        gate = (self.root / "references" / "epistemic-gate.md").read_text()
        prompt = f"""
You draft LinkedIn posts for Supreet Deshpande. Return JSON only.

AUTHORITATIVE VOICE PROFILE:
{voice}

TRUTH AND CONFIDENTIALITY GATE:
{gate}

RAW THOUGHT:
{raw_text}

THREAD CONTEXT FROM SUPREET:
{json.dumps(thread_text, ensure_ascii=False)}

PREVIOUS DRAFT:
{previous_draft or "(none)"}

EDIT REQUEST FROM SUPREET:
{edit_request or "(none)"}

Rules:
- The raw thought and thread are the topic source. Do not introduce a news topic.
- Do not invent a scene, analogy, number, customer, quote, or personal experience.
- Public claims in the voice profile are examples and a source index, not automatic permission to
  insert them. Use a factual claim only when the raw thought/thread supports it.
- If a strong post cannot be written without one or two missing facts, return needs_context and ask
  one short, concrete question Supreet can answer in the Slack thread.
- If the material is logistics, private customer information, patient data, or not suitable for a
  post, return skip.
- If an edit request exists, revise the previous draft. Follow it unless it asks you to invent or
  disclose unsafe material.
- A draft must be plain text, at most 3000 characters, and contain one idea.

Return exactly:
{{
  "decision": "draft" | "needs_context" | "skip",
  "draft": "plain text or empty",
  "question": "one question or empty",
  "evidence_used": ["short descriptions of statements supplied by Supreet"]
}}
""".strip()
        data = self._message(prompt)
        decision = DraftDecision.from_dict(data)
        if decision.decision == "draft" and not decision.draft:
            raise ValueError("Writer returned draft decision with empty draft")
        if decision.decision == "needs_context" and not decision.question:
            raise ValueError("Writer requested context without a question")
        return decision

    def _message(self, prompt: str) -> dict[str, Any]:
        _, _, body = self.http.request(
            "POST",
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
            },
            json_body={
                "model": self.model,
                "max_tokens": 1800,
                "temperature": 0.3,
                "messages": [{"role": "user", "content": prompt}],
            },
        )
        text = "".join(
            block.get("text", "")
            for block in body.get("content", [])
            if block.get("type") == "text"
        ).strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text)
        try:
            return json.loads(text)
        except json.JSONDecodeError as error:
            raise ValueError(f"Writer returned invalid JSON: {text[:300]}") from error
