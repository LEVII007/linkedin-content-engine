import unittest

from content_engine.safety import check


class SafetyTest(unittest.TestCase):
    def test_blocks_identifiers_and_secrets(self):
        for text in (
            "Patient MRN: 88213",
            "NPI 1234567890",
            "api_key=sk-secret",
            "This is confidential",
            "Call +919876543210",
        ):
            errors, _ = check(text)
            self.assertTrue(errors, text)

    def test_allows_public_funding_and_supreet_format(self):
        text = (
            "We raised $5M to build clinical-grade Voice AI. 🚀\n\n"
            "#AI #Pharma #LifeSciences #SynthioLabs"
        )
        errors, warnings = check(text)
        self.assertEqual(errors, [])
        self.assertNotIn("more than six hashtags", warnings)

    def test_warns_on_excessive_hashtags(self):
        _, warnings = check("#a #b #c #d #e #f #g")
        self.assertIn("more than six hashtags", warnings)


if __name__ == "__main__":
    unittest.main()
