import tempfile
import time
import unittest
from dataclasses import replace
from pathlib import Path

from content_engine.config import Config
from content_engine.engine import ContentEngine
from content_engine.linkedin import PublishResult
from content_engine.models import DraftDecision, Idea, StoredIdea


def config(publish: bool = False) -> Config:
    return Config(
        github_token="gh",
        github_repository="owner/repo",
        slack_bot_token="slack",
        slack_channel_id="C123",
        slack_approver_user_id="U123",
        anthropic_api_key="anthropic",
        anthropic_model="test-model",
        linkedin_access_token="li" if publish else None,
        linkedin_person_urn="urn:li:person:abc" if publish else None,
        linkedin_token_expires_at=9999999999 if publish else None,
        publish_enabled=publish,
        max_drafts_per_run=1,
        root=Path(tempfile.gettempdir()),
    )


class FakeStore:
    def __init__(self, ideas=None):
        self.ideas = list(ideas or [])
        self.next_number = len(self.ideas) + 1
        self.token_warnings = set()

    def ensure_labels(self):
        pass

    def list(self, statuses=None):
        if statuses is None:
            return list(self.ideas)
        return [item for item in self.ideas if item.idea.status in statuses]

    def create(self, idea):
        stored = StoredIdea(self.next_number, idea)
        self.next_number += 1
        self.ideas.append(stored)
        return stored

    def update(self, stored):
        pass

    def issue_url(self, number):
        return f"https://github.test/issues/{number}"

    def token_warning_sent(self, expires_at):
        return expires_at in self.token_warnings

    def mark_token_warning_sent(self, expires_at):
        self.token_warnings.add(expires_at)


class FakeSlack:
    def __init__(self):
        self.messages = []
        self.thread_replies = {}
        self.message_reactions = {}

    def history(self, channel, limit=100):
        return list(self.messages)

    def replies(self, channel, thread_ts):
        return list(self.thread_replies.get(thread_ts, []))

    def reactions(self, channel, timestamp):
        return self.message_reactions.get(timestamp, {})

    def post(self, channel, text, thread_ts=None):
        ts = f"bot-{len(self.messages) + 1}"
        self.messages.append({"ts": ts, "text": text, "thread_ts": thread_ts})
        return ts


class FakeWriter:
    def __init__(self, decision):
        self.decision = decision

    def create_draft(self, *args, **kwargs):
        return self.decision


class FakePublisher:
    def __init__(self):
        self.posts = []

    def publish(self, text):
        self.posts.append(text)
        return PublishResult("urn:li:share:1", "https://linkedin.test/1")


class EngineTest(unittest.TestCase):
    def test_token_warning_is_sent_once(self):
        slack = FakeSlack()
        store = FakeStore()
        cfg = replace(
            config(), linkedin_token_expires_at=int(time.time()) + 3 * 86400
        )
        engine = ContentEngine(
            cfg, slack=slack, store=store, writer=FakeWriter(None)
        )
        self.assertEqual(engine.check_token_expiry(), 1)
        self.assertEqual(engine.check_token_expiry(), 0)
        self.assertIn("expires in", slack.messages[0]["text"])

    def test_ingest_accepts_only_approver_and_deduplicates(self):
        slack = FakeSlack()
        slack.messages = [
            {"ts": "1.0", "user": "U123", "text": "latent heat"},
            {"ts": "2.0", "user": "OTHER", "text": "do not ingest"},
            {"ts": "3.0", "user": "U123", "text": ""},
        ]
        store = FakeStore()
        engine = ContentEngine(
            config(), slack=slack, store=store, writer=FakeWriter(None)
        )
        self.assertEqual(engine.ingest(), 1)
        self.assertEqual(engine.ingest(), 0)
        self.assertEqual(store.ideas[0].idea.raw_text, "latent heat")

    def test_draft_requires_context_in_original_thread(self):
        slack = FakeSlack()
        stored = StoredIdea(1, Idea(slack_ts="1.0", raw_text="some idea"))
        store = FakeStore([stored])
        writer = FakeWriter(
            DraftDecision(decision="needs_context", question="What changed?")
        )
        engine = ContentEngine(config(), slack=slack, store=store, writer=writer)
        self.assertEqual(engine.draft_new(), 0)
        self.assertEqual(stored.idea.status, "needs_context")
        self.assertEqual(slack.messages[0]["thread_ts"], "1.0")

    def test_only_approver_checkmark_approves(self):
        slack = FakeSlack()
        stored = StoredIdea(
            1,
            Idea(
                slack_ts="1.0",
                raw_text="idea",
                status="review",
                draft="Draft 🚀",
                review_ts="2.0",
            ),
        )
        store = FakeStore([stored])
        engine = ContentEngine(
            config(), slack=slack, store=store, writer=FakeWriter(None)
        )
        slack.message_reactions["2.0"] = {"white_check_mark": {"OTHER"}}
        self.assertEqual(engine.process_approvals(), 0)
        slack.message_reactions["2.0"] = {"white_check_mark": {"U123"}}
        self.assertEqual(engine.process_approvals(), 1)
        self.assertEqual(stored.idea.status, "approved")

    def test_conflicting_reactions_do_not_approve(self):
        slack = FakeSlack()
        stored = StoredIdea(
            1,
            Idea(status="review", slack_ts="1", raw_text="x", review_ts="2"),
        )
        slack.message_reactions["2"] = {
            "white_check_mark": {"U123"},
            "x": {"U123"},
        }
        engine = ContentEngine(
            config(), slack=slack, store=FakeStore([stored]), writer=FakeWriter(None)
        )
        self.assertEqual(engine.process_approvals(), 0)

    def test_publish_marks_before_call_and_posts_once(self):
        slack = FakeSlack()
        stored = StoredIdea(
            1,
            Idea(
                status="approved",
                slack_ts="1",
                raw_text="x",
                review_ts="2",
                draft="A real approved post. 🚀",
            ),
        )
        publisher = FakePublisher()
        engine = ContentEngine(
            config(True),
            slack=slack,
            store=FakeStore([stored]),
            writer=FakeWriter(None),
            publisher=publisher,
        )
        self.assertEqual(engine.publish_approved(), 1)
        self.assertEqual(stored.idea.status, "posted")
        self.assertEqual(engine.publish_approved(), 0)
        self.assertEqual(len(publisher.posts), 1)


if __name__ == "__main__":
    unittest.main()
