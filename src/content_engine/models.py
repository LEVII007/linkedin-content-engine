from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


META_START = "<!-- linkedin-engine:"
META_END = ":linkedin-engine -->"


@dataclass
class Idea:
    slack_ts: str
    raw_text: str
    status: str = "new"
    thread_text: list[str] = field(default_factory=list)
    draft: str = ""
    evidence_used: list[str] = field(default_factory=list)
    review_ts: str = ""
    last_reply_ts: str = ""
    question_ts: str = ""
    linkedin_post_id: str = ""
    permalink: str = ""

    def to_body(self) -> str:
        import json

        payload = json.dumps(asdict(self), ensure_ascii=False, sort_keys=True)
        return (
            f"{META_START}{payload}{META_END}\n\n"
            "Managed by the LinkedIn content engine. Use Slack to review or edit."
        )

    @classmethod
    def from_body(cls, body: str) -> "Idea":
        import json

        start = body.index(META_START) + len(META_START)
        end = body.index(META_END, start)
        data: dict[str, Any] = json.loads(body[start:end])
        known = {item.name for item in cls.__dataclass_fields__.values()}
        return cls(**{key: value for key, value in data.items() if key in known})


@dataclass
class StoredIdea:
    issue_number: int
    idea: Idea


@dataclass
class DraftDecision:
    decision: str
    draft: str = ""
    question: str = ""
    evidence_used: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DraftDecision":
        decision = str(data.get("decision", "")).strip().lower()
        if decision not in {"draft", "needs_context", "skip"}:
            raise ValueError(f"Unexpected draft decision: {decision!r}")
        return cls(
            decision=decision,
            draft=str(data.get("draft", "")).strip(),
            question=str(data.get("question", "")).strip(),
            evidence_used=[str(x) for x in data.get("evidence_used", [])],
        )
