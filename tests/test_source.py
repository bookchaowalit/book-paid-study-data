import unittest

from book_paid_study_data.capture import normalize
from book_paid_study_data.cli import resource, validate


class SourceTests(unittest.TestCase):
    def raw(self):
        return (
            "<h1>How to earn on Prolific</h1>"
            "<p>Join the waitlist</p>"
            "<p>When you're eligible for a study, it will appear on your dashboard.</p>"
            "<p>Once you've earned $/£6 in a given currency, you can cash out directly to your PayPal account.</p>"
            "<h2>Minimum payment threshold</h2>"
            "<p>Data collectors are required to pay participants at least £6.00/$8.00 per hour.</p>"
            "<h2>Data privacy</h2>"
            "<p>Data collectors only see your Prolific ID when reviewing your survey responses.</p>"
        ).encode()

    def test_prolific_source_fixture(self):
        source = resource("source.json")
        data = normalize(self.raw(), source, "2026-09-07T00:00:00Z")
        item = data["items"][0]
        item["provenance"].update(
            raw_object_key="landing/test",
            bronze_manifest_key="control/manifests/test",
        )
        self.assertEqual(item["title"], "Prolific participant studies")
        self.assertEqual(item["status"], "unknown")
        self.assertEqual(item["deadline"], {"kind": "unknown", "at": None})
        self.assertEqual(item["value"], {"kind": "variable", "amount": None, "currency": None, "guaranteed": False})
        self.assertIsNone(item["terms"]["duration_minutes"])
        self.assertTrue(item["terms"]["screening_required"])
        self.assertEqual(validate(data)["schema_version"], source["schema_version"])

    def test_source_drift_rejected(self):
        with self.assertRaises(ValueError):
            normalize(b"<h1>unrelated page</h1>", resource("source.json"), "2026-09-07T00:00:00Z")

    def test_additional_paid_study_sources_normalize(self):
        fixtures = {
            "source-respondent-paid-research-participants.json": "Participants are getting paid for research studies; one-on-one interviews and surveys.",
            "source-usertesting-paid-contributors.json": "Get paid to test. Take a quick practice test and complete surveys.",
            "source-yougov-panel-surveys.json": "Our panel includes surveys and members are paid for participation.",
            "source-nih-research-participant-compensation.json": "Compensation for Research Participation provides payment for research participants.",
        }
        for filename, text in fixtures.items():
            with self.subTest(source=filename):
                source = resource(filename)
                data = normalize(f"<p>{text}</p>".encode(), source, "2026-09-08T00:00:00Z")
                item = data["items"][0]
                item["provenance"].update(raw_object_key="landing/test", bronze_manifest_key="control/manifests/test")
                self.assertEqual(item["category"], source["category"])
                self.assertEqual(validate(data)["schema_version"], "paid_study.v1")


if __name__ == "__main__":
    unittest.main()
