import unittest

from content_engine.models import Idea


class IdeaSerializationTest(unittest.TestCase):
    def test_round_trip_preserves_unicode_and_draft(self):
        idea = Idea(
            slack_ts="123.456",
            raw_text="latent heat 🧊",
            status="review",
            draft="That’s enterprise AI right now. 🚀",
        )
        self.assertEqual(Idea.from_body(idea.to_body()), idea)

    def test_rejects_unmanaged_issue(self):
        with self.assertRaises(ValueError):
            Idea.from_body("ordinary GitHub issue")


if __name__ == "__main__":
    unittest.main()
