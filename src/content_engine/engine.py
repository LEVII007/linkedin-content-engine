from __future__ import annotations

import logging
import time

from .config import Config
from .github_store import GitHubStore
from .linkedin import LinkedInPublisher
from .models import DraftDecision, Idea, StoredIdea
from .safety import check
from .slack import SlackClient
from .writer import Writer

LOG = logging.getLogger(__name__)


class ContentEngine:
    def __init__(
        self,
        config: Config,
        *,
        slack: SlackClient | None = None,
        store: GitHubStore | None = None,
        writer: Writer | None = None,
        publisher: LinkedInPublisher | None = None,
    ):
        self.config = config
        self.slack = slack or SlackClient(config.slack_bot_token)
        self.store = store or GitHubStore(
            config.github_token, config.github_repository
        )
        self.writer = writer or Writer(
            config.anthropic_api_key,
            config.anthropic_model,
            config.root,
        )
        if publisher is not None:
            self.publisher = publisher
        elif config.publish_enabled:
            config.validate_publish()
            self.publisher = LinkedInPublisher(
                config.linkedin_access_token or "",
                config.linkedin_person_urn or "",
                config.linkedin_token_expires_at or 0,
            )
        else:
            self.publisher = None

    def run(self) -> dict[str, int]:
        self.store.ensure_labels()
        counts = {
            "token_warnings": self.check_token_expiry(),
            "ingested": self.ingest(),
            "context_updated": self.process_context(),
            "edits": self.process_edits(),
            "approved": self.process_approvals(),
            "drafted": self.draft_new(),
            "published": self.publish_approved(),
        }
        LOG.info("Run complete: %s", counts)
        return counts

    def check_token_expiry(self) -> int:
        expires_at = self.config.linkedin_token_expires_at
        if not expires_at:
            return 0
        days = (expires_at - int(time.time())) // 86400
        if days > 7 or self.store.token_warning_sent(expires_at):
            return 0
        message = (
            "LinkedIn authorization has expired. Please renew it."
            if days < 0
            else f"LinkedIn authorization expires in {days} day(s). Please renew it."
        )
        self.slack.post(self.config.slack_channel_id, message)
        self.store.mark_token_warning_sent(expires_at)
        return 1

    def ingest(self) -> int:
        known = {item.idea.slack_ts for item in self.store.list()}
        messages = self.slack.history(self.config.slack_channel_id)
        candidates = [
            message
            for message in messages
            if message.get("user") == self.config.slack_approver_user_id
            and not message.get("subtype")
            and message.get("text", "").strip()
            and message.get("ts") not in known
        ]
        for message in reversed(candidates):
            self.store.create(
                Idea(slack_ts=str(message["ts"]), raw_text=message["text"].strip())
            )
        return len(candidates)

    def process_context(self) -> int:
        updated = 0
        for stored in self.store.list({"needs_context"}):
            replies = self._new_human_replies(
                stored.idea.slack_ts, stored.idea.last_reply_ts
            )
            if not replies:
                continue
            stored.idea.thread_text.extend(reply["text"].strip() for reply in replies)
            stored.idea.last_reply_ts = str(replies[-1]["ts"])
            decision = self.writer.create_draft(
                stored.idea.raw_text, stored.idea.thread_text
            )
            self._apply_decision(stored, decision)
            updated += 1
        return updated

    def process_edits(self) -> int:
        updated = 0
        for stored in self.store.list({"review"}):
            if not stored.idea.review_ts:
                continue
            replies = self._new_human_replies(
                stored.idea.review_ts, stored.idea.last_reply_ts
            )
            if not replies:
                continue
            edit_request = "\n".join(reply["text"].strip() for reply in replies)
            decision = self.writer.create_draft(
                stored.idea.raw_text,
                stored.idea.thread_text,
                previous_draft=stored.idea.draft,
                edit_request=edit_request,
            )
            stored.idea.last_reply_ts = str(replies[-1]["ts"])
            self._apply_decision(stored, decision)
            updated += 1
        return updated

    def process_approvals(self) -> int:
        approved = 0
        for stored in self.store.list({"review"}):
            if not stored.idea.review_ts:
                continue
            reactions = self.slack.reactions(
                self.config.slack_channel_id, stored.idea.review_ts
            )
            user = self.config.slack_approver_user_id
            has_yes = user in reactions.get("white_check_mark", set())
            has_no = user in reactions.get("x", set())
            if has_yes and not has_no:
                stored.idea.status = "approved"
                self.store.update(stored)
                approved += 1
        return approved

    def draft_new(self) -> int:
        drafted = 0
        for stored in self.store.list({"new"})[: self.config.max_drafts_per_run]:
            replies = self._new_human_replies(stored.idea.slack_ts, "")
            stored.idea.thread_text = [reply["text"].strip() for reply in replies]
            if replies:
                stored.idea.last_reply_ts = str(replies[-1]["ts"])
            decision = self.writer.create_draft(
                stored.idea.raw_text, stored.idea.thread_text
            )
            self._apply_decision(stored, decision)
            if decision.decision == "draft":
                drafted += 1
        return drafted

    def publish_approved(self) -> int:
        if not self.publisher:
            return 0
        approved = self.store.list({"approved"})
        if not approved:
            return 0

        stored = approved[0]
        errors, _ = check(stored.idea.draft)
        if errors:
            stored.idea.status = "failed"
            self.store.update(stored)
            self.slack.post(
                self.config.slack_channel_id,
                "I stopped this publish because the final safety check failed:\n• "
                + "\n• ".join(errors),
                thread_ts=stored.idea.review_ts,
            )
            return 0

        # Mark first. If the process dies after LinkedIn accepts the post, the next run
        # will not retry blindly and create a duplicate.
        stored.idea.status = "publishing"
        self.store.update(stored)
        try:
            result = self.publisher.publish(stored.idea.draft)
        except Exception as error:
            stored.idea.status = "failed"
            self.store.update(stored)
            self.slack.post(
                self.config.slack_channel_id,
                f"LinkedIn publish failed and will not retry automatically: {error}",
                thread_ts=stored.idea.review_ts,
            )
            raise

        stored.idea.status = "posted"
        stored.idea.linkedin_post_id = result.post_id
        stored.idea.permalink = result.permalink
        self.store.update(stored)
        self.slack.post(
            self.config.slack_channel_id,
            f"Published ✅\n{result.permalink}",
            thread_ts=stored.idea.review_ts,
        )
        return 1

    def _apply_decision(
        self, stored: StoredIdea, decision: DraftDecision
    ) -> None:
        if decision.decision == "skip":
            stored.idea.status = "skipped"
            self.store.update(stored)
            return
        if decision.decision == "needs_context":
            stored.idea.status = "needs_context"
            stored.idea.question_ts = self.slack.post(
                self.config.slack_channel_id,
                f"I can turn this into a post, but I need one detail:\n"
                f"{decision.question}",
                thread_ts=stored.idea.slack_ts,
            )
            self.store.update(stored)
            return

        errors, warnings = check(decision.draft)
        if errors:
            stored.idea.status = "failed"
            self.store.update(stored)
            self.slack.post(
                self.config.slack_channel_id,
                "I drafted this, but the safety check blocked it:\n• "
                + "\n• ".join(errors),
                thread_ts=stored.idea.slack_ts,
            )
            return

        stored.idea.status = "review"
        stored.idea.draft = decision.draft
        stored.idea.evidence_used = decision.evidence_used
        warning_text = (
            "\n\nReview note: " + "; ".join(warnings) if warnings else ""
        )
        stored.idea.review_ts = self.slack.post(
            self.config.slack_channel_id,
            f"Draft ready:\n\n{decision.draft}{warning_text}\n\n"
            "React ✅ to approve. Reply in this thread with edits. "
            "Nothing publishes without your ✅.",
        )
        # Replies to the previous review message must not be replayed against this one.
        stored.idea.last_reply_ts = ""
        self.store.update(stored)

    def _new_human_replies(
        self, thread_ts: str, after_ts: str
    ) -> list[dict[str, str]]:
        return [
            reply
            for reply in self.slack.replies(
                self.config.slack_channel_id, thread_ts
            )
            if reply.get("user") == self.config.slack_approver_user_id
            and reply.get("text", "").strip()
            and float(str(reply.get("ts", "0"))) > float(after_ts or "0")
        ]
