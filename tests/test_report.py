"""Tests for report assembly — the shape of the JSON the workflow commits."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from gemara_metrics import report


def context(**overrides):
    base = {
        "org": "gemaraproj",
        "window": ("2026-08-19", "2026-11-17"),
        "generated_at": "2026-11-18T00:00:00Z",
        "repos": [
            {
                "name": "gemara",
                "description": "spec",
                "topics": ["grc"],
                "license_spdx": "Apache-2.0",
                "has_discussions": False,
                "has_issue_template": True,
                "has_contributing": True,
                "has_security_insights": True,
                "good_first_issues": 0,
                "forks": 31,
                "open_issues": 34,
                "open_prs": 39,
                "releases": 30,
            }
        ],
        "prs_all_time": [
            {"repo": "gemara", "author": "veteran", "author_is_bot": False,
             "created_at": "2025-01-01T00:00:00Z", "merged_at": "2025-01-02T00:00:00Z"},
            {"repo": "gemara", "author": "newcomer", "author_is_bot": False,
             "created_at": "2026-10-05T00:00:00Z", "merged_at": "2026-10-05T06:00:00Z"},
        ],
        "issues_window": [
            {"repo": "gemara", "author": "asker", "created_at": "2026-10-01T00:00:00Z", "comments": []}
        ],
        "reviews_window": [{"repo": "gemara", "author": "jpower432", "author_is_bot": False}],
        "adopters": {"source": "data/adopters.yml", "spec": [], "sdk": []},
    }
    base.update(overrides)
    return base


class ReportShapeTest(unittest.TestCase):
    def test_records_the_window_and_scope_in_the_metadata(self):
        result = report.build(**context())

        self.assertEqual("gemaraproj", result["meta"]["org"])
        self.assertEqual("2026-08-19", result["meta"]["window_start"])
        self.assertEqual("2026-11-17", result["meta"]["window_end"])
        self.assertEqual(1, result["meta"]["repos_in_scope"])

    def test_scale_counts_only_merges_inside_the_window(self):
        result = report.build(**context())

        self.assertEqual(1, result["scale"]["merged_in_window"]["human_merged"])

    def test_the_new_contributor_cohort_comes_from_all_time_history(self):
        result = report.build(**context())

        self.assertEqual(["newcomer"], [c["login"] for c in result["new_contributors"]["cohort"]])
        self.assertEqual(1, result["new_contributors"]["count"])

    def test_carries_the_responsiveness_and_review_sections(self):
        result = report.build(**context())

        self.assertEqual(1, result["responsiveness"]["unanswered"])
        self.assertEqual(1, result["reviews"]["human_reviews"])

    def test_passes_the_curated_adopter_list_straight_through(self):
        result = report.build(**context())

        self.assertEqual("data/adopters.yml", result["adoption"]["source"])

    def test_adoption_says_why_it_is_curated_rather_than_searched(self):
        """Code search needs a PAT. Rather than add one, the list is kept by
        hand — and the report has to say so instead of implying a crawl."""
        result = report.build(**context())

        self.assertIn("curated", result["adoption"]["method"].lower())


class LfxDelegationTest(unittest.TestCase):
    def test_the_report_links_to_lfx_instead_of_restating_it(self):
        result = report.build(**context())

        self.assertIn("lfx_insights", result)
        self.assertTrue(result["lfx_insights"]["see_lfx_instead"])

    def test_no_section_computes_a_metric_lfx_already_owns(self):
        result = report.build(**context())

        delegated = {entry["metric"] for entry in result["lfx_insights"]["see_lfx_instead"]}
        computed = set(result.keys()) | set(result["scale"].keys())
        self.assertEqual(set(), delegated & computed)


if __name__ == "__main__":
    unittest.main()
