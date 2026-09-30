"""Privacy regression: normalized records never carry participant data from the page.

The captured pages are public policy pages, but a logged-in or personalised variant
could embed a participant ID, e-mail, screener answer or payout. The adapters must
emit only reviewed config/contract text, so none of that can leak into a record.
"""

import json
import unittest

from book_paid_study_data.capture import REQUIRED_MARKERS, normalize, source_config
from book_paid_study_data.cli import validate

CHECKED_AT = "2026-09-07T00:00:00Z"
LINEAGE = {"raw_object_key": "landing/test", "bronze_manifest_key": "control/manifests/test"}

# Synthetic participant data a personalised page might contain.
SENSITIVE = (
    "5f3a9c1e2b7d4a0012ab34cd",  # Prolific-style participant ID
    "participant.jane@example.org",
    "PID=5f3a9c1e",
    "Jane Q. Participant",
    "+44 7700 900123",
    "screener answer: household income 42000",
    "balance £17.42",
    "session_token=abc123secret",
)


def personalised_page(source_id):
    markers = " ".join(REQUIRED_MARKERS[source_id])
    leaked = "".join(f"<p>{value}</p>" for value in SENSITIVE)
    return (
        "<main><h1>Dashboard for Jane Q. Participant</h1>"
        f"<p>{markers}</p>{leaked}"
        '<input type="hidden" name="participant_id" value="5f3a9c1e2b7d4a0012ab34cd">'
        "</main>"
    ).encode()


class PrivacyRegressionTests(unittest.TestCase):
    def test_no_participant_data_reaches_normalized_output(self):
        for source_id in REQUIRED_MARKERS:
            with self.subTest(source_id=source_id):
                data = normalize(personalised_page(source_id), source_config(source_id), CHECKED_AT)
                serialized = json.dumps(data, ensure_ascii=False).casefold()
                for value in SENSITIVE:
                    self.assertNotIn(value.casefold(), serialized)
                self.assertNotIn("5f3a9c1e", serialized)
                self.assertNotIn("jane", serialized)

    def test_output_is_page_independent(self):
        # Two pages with the same markers but different personal content yield the
        # same record, so no page text (personal or otherwise) is copied through.
        for source_id in REQUIRED_MARKERS:
            with self.subTest(source_id=source_id):
                source = source_config(source_id)
                plain = ("<p>" + " ".join(REQUIRED_MARKERS[source_id]) + "</p>").encode("utf-8")
                self.assertEqual(
                    normalize(plain, source, CHECKED_AT),
                    normalize(personalised_page(source_id), source, CHECKED_AT),
                )

    def test_personalised_page_still_validates_against_contract(self):
        # The contract rejects unexpected fields, so a participant field cannot be added silently.
        for source_id in REQUIRED_MARKERS:
            with self.subTest(source_id=source_id):
                data = normalize(personalised_page(source_id), source_config(source_id), CHECKED_AT)
                data["items"][0]["provenance"].update(LINEAGE)
                validate(data)
                data["items"][0]["participant_id"] = "5f3a9c1e2b7d4a0012ab34cd"
                with self.assertRaises(ValueError):
                    validate(data)


if __name__ == "__main__":
    unittest.main()
