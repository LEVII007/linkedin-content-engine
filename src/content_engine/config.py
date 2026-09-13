from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def _bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Config:
    github_token: str
    github_repository: str
    slack_bot_token: str
    slack_channel_id: str
    slack_approver_user_id: str
    anthropic_api_key: str
    anthropic_model: str
    linkedin_access_token: str | None
    linkedin_person_urn: str | None
    linkedin_token_expires_at: int | None
    publish_enabled: bool
    max_drafts_per_run: int
    root: Path

    @classmethod
    def from_env(cls) -> "Config":
        expiry = os.getenv("LINKEDIN_TOKEN_EXPIRES_AT", "").strip()
        return cls(
            github_token=_required("GITHUB_TOKEN"),
            github_repository=_required("GITHUB_REPOSITORY"),
            slack_bot_token=_required("SLACK_BOT_TOKEN"),
            slack_channel_id=_required("SLACK_CHANNEL_ID"),
            slack_approver_user_id=_required("SLACK_APPROVER_USER_ID"),
            anthropic_api_key=_required("ANTHROPIC_API_KEY"),
            anthropic_model=(
                os.getenv("ANTHROPIC_MODEL", "").strip() or "claude-sonnet-5"
            ),
            linkedin_access_token=os.getenv("LINKEDIN_ACCESS_TOKEN") or None,
            linkedin_person_urn=os.getenv("LINKEDIN_PERSON_URN") or None,
            linkedin_token_expires_at=int(expiry) if expiry else None,
            publish_enabled=_bool("PUBLISH_ENABLED"),
            max_drafts_per_run=int(os.getenv("MAX_DRAFTS_PER_RUN", "1")),
            root=Path(__file__).resolve().parents[2],
        )

    def validate_publish(self) -> None:
        if not self.publish_enabled:
            return
        missing = [
            name
            for name, value in (
                ("LINKEDIN_ACCESS_TOKEN", self.linkedin_access_token),
                ("LINKEDIN_PERSON_URN", self.linkedin_person_urn),
                ("LINKEDIN_TOKEN_EXPIRES_AT", self.linkedin_token_expires_at),
            )
            if not value
        ]
        if missing:
            raise ValueError(
                f"Publishing is enabled but these values are missing: {', '.join(missing)}"
            )
