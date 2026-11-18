"""Tests for the pure aggregation layer.

These never touch the network. Every test feeds in the same shape of record
the GitHub client emits and checks the number that lands in the report.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from gemara_metrics import aggregate


def pr(author, merged_at, repo="gemara", bot=False):
    return {
        "repo": repo,
        "author": author,
        "author_is_bot": bot,
        "merged_at": merged_at,
    }


class NewContributorsTest(unittest.TestCase):
    def test_counts_an_author_whose_first_ever_merge_is_inside_the_window(self):
        prs = [pr("newcomer", "2026-10-05T12:00:00Z")]

        result = aggregate.new_contributors(prs, "2026-08-19", "2026-11-17")

        self.assertEqual([("newcomer", "2026-10-05")], [(r["login"], r["first_merge"]) for r in result])

    def test_ignores_an_author_who_already_merged_before_the_window(self):
        prs = [
            pr("veteran", "2025-04-01T09:00:00Z"),
            pr("veteran", "2026-10-05T12:00:00Z"),
        ]

        result = aggregate.new_contributors(prs, "2026-08-19", "2026-11-17")

        self.assertEqual([], result)

    def test_ignores_bot_authors(self):
        prs = [pr("dependabot[bot]", "2026-10-05T12:00:00Z", bot=True)]

        result = aggregate.new_contributors(prs, "2026-08-19", "2026-11-17")

        self.assertEqual([], result)

    def test_orders_the_cohort_by_first_merge_date(self):
        prs = [
            pr("second", "2026-10-25T00:00:00Z"),
            pr("first", "2026-09-10T00:00:00Z"),
            pr("third", "2026-11-07T00:00:00Z"),
        ]

        result = aggregate.new_contributors(prs, "2026-08-19", "2026-11-17")

        self.assertEqual(["first", "second", "third"], [r["login"] for r in result])


def issue(author, created_at, comments=(), repo="gemara"):
    return {
        "repo": repo,
        "author": author,
        "created_at": created_at,
        "comments": [
            {"author": c[0], "author_is_bot": c[2] if len(c) > 2 else False, "created_at": c[1]}
            for c in comments
        ],
    }


class ResponsivenessTest(unittest.TestCase):
    def test_counts_an_issue_with_no_comments_as_unanswered(self):
        issues = [issue("asker", "2026-10-01T00:00:00Z")]

        result = aggregate.responsiveness(issues)

        self.assertEqual(1, result["opened"])
        self.assertEqual(1, result["unanswered"])

    def test_a_reply_from_someone_else_answers_the_issue(self):
        issues = [issue("asker", "2026-10-01T00:00:00Z", [("maintainer", "2026-10-03T00:00:00Z")])]

        result = aggregate.responsiveness(issues)

        self.assertEqual(0, result["unanswered"])
        self.assertEqual(2.0, result["median_days_to_first_response"])

    def test_the_author_talking_to_themselves_is_not_a_response(self):
        issues = [issue("asker", "2026-10-01T00:00:00Z", [("asker", "2026-10-02T00:00:00Z")])]

        result = aggregate.responsiveness(issues)

        self.assertEqual(1, result["unanswered"])

    def test_a_bot_comment_is_not_a_response(self):
        issues = [issue("asker", "2026-10-01T00:00:00Z", [("coderabbitai", "2026-10-02T00:00:00Z", True)])]

        result = aggregate.responsiveness(issues)

        self.assertEqual(1, result["unanswered"])

    def test_median_uses_the_earliest_human_reply_on_each_issue(self):
        issues = [
            issue("asker", "2026-10-01T00:00:00Z", [
                ("late", "2026-10-09T00:00:00Z"),
                ("early", "2026-10-02T00:00:00Z"),
            ]),
            issue("asker", "2026-10-01T00:00:00Z", [("other", "2026-10-05T00:00:00Z")]),
        ]

        result = aggregate.responsiveness(issues)

        self.assertEqual(2.5, result["median_days_to_first_response"])

    def test_median_is_none_when_nothing_was_answered(self):
        issues = [issue("asker", "2026-10-01T00:00:00Z")]

        result = aggregate.responsiveness(issues)

        self.assertIsNone(result["median_days_to_first_response"])


class MergeVelocityTest(unittest.TestCase):
    def test_reports_the_median_hours_between_opening_and_merging(self):
        prs = [
            {"author_is_bot": False, "created_at": "2026-10-01T00:00:00Z", "merged_at": "2026-10-01T02:00:00Z"},
            {"author_is_bot": False, "created_at": "2026-10-01T00:00:00Z", "merged_at": "2026-10-01T10:00:00Z"},
        ]

        self.assertEqual(6.0, aggregate.merge_velocity(prs)["median_hours_to_merge"])

    def test_leaves_bot_pull_requests_out_of_the_median(self):
        prs = [
            {"author_is_bot": False, "created_at": "2026-10-01T00:00:00Z", "merged_at": "2026-10-01T04:00:00Z"},
            {"author_is_bot": True, "created_at": "2026-10-01T00:00:00Z", "merged_at": "2026-10-01T00:01:00Z"},
        ]

        result = aggregate.merge_velocity(prs)

        self.assertEqual(4.0, result["median_hours_to_merge"])
        self.assertEqual(1, result["human_merged"])
        self.assertEqual(1, result["bot_merged"])

    def test_skips_pull_requests_that_were_never_merged(self):
        prs = [{"author_is_bot": False, "created_at": "2026-10-01T00:00:00Z", "merged_at": None}]

        result = aggregate.merge_velocity(prs)

        self.assertEqual(0, result["human_merged"])
        self.assertIsNone(result["median_hours_to_merge"])


class ReviewConcentrationTest(unittest.TestCase):
    def test_reports_what_share_of_reviews_the_top_people_carry(self):
        reviews = [{"author": "a", "author_is_bot": False}] * 8 + [{"author": "b", "author_is_bot": False}] * 2

        result = aggregate.review_concentration(reviews, top_n=1)

        self.assertEqual(10, result["human_reviews"])
        self.assertEqual(80.0, result["top_n_share_pct"])
        self.assertEqual([("a", 8)], [(r["login"], r["reviews"]) for r in result["top_reviewers"]])

    def test_bot_reviews_are_counted_separately_not_mixed_into_the_share(self):
        reviews = [
            {"author": "a", "author_is_bot": False},
            {"author": "coderabbitai", "author_is_bot": True},
        ]

        result = aggregate.review_concentration(reviews, top_n=1)

        self.assertEqual(1, result["human_reviews"])
        self.assertEqual(1, result["bot_reviews"])
        self.assertEqual(100.0, result["top_n_share_pct"])


def repo(name, **overrides):
    base = {
        "name": name,
        "description": "does a thing",
        "topics": ["grc"],
        "license_spdx": "Apache-2.0",
        "has_discussions": True,
        "has_issue_template": True,
        "has_contributing": True,
        "has_security_insights": True,
        "good_first_issues": 2,
    }
    base.update(overrides)
    return base


class EaseOfEntryTest(unittest.TestCase):
    def test_a_fully_furnished_repo_reports_no_gaps(self):
        result = aggregate.ease_of_entry([repo("gemara")])

        self.assertEqual([], result["repos"][0]["gaps"])

    def test_flags_a_repo_with_no_topics(self):
        result = aggregate.ease_of_entry([repo("gemara", topics=[])])

        self.assertIn("no_topics", result["repos"][0]["gaps"])

    def test_flags_a_missing_description_and_contributing_guide(self):
        result = aggregate.ease_of_entry([repo("website", description=None, has_contributing=False)])

        self.assertIn("no_description", result["repos"][0]["gaps"])
        self.assertIn("no_contributing", result["repos"][0]["gaps"])

    def test_treats_an_unrecognised_license_as_a_gap(self):
        result = aggregate.ease_of_entry([repo("eval-infra", license_spdx="NOASSERTION")])

        self.assertIn("no_license", result["repos"][0]["gaps"])

    def test_totals_the_on_ramp_supply_across_repos(self):
        repos = [repo("a", good_first_issues=3), repo("b", good_first_issues=0, topics=[])]

        result = aggregate.ease_of_entry(repos)

        self.assertEqual(3, result["good_first_issues_total"])
        self.assertEqual(1, result["repos_without_topics"])

    def test_counts_how_many_repos_carry_security_insights(self):
        repos = [repo("a"), repo("b", has_security_insights=False)]

        result = aggregate.ease_of_entry(repos)

        self.assertEqual("1/2", result["security_insights_coverage"])


class LfxInsightsTest(unittest.TestCase):
    """The report must not restate numbers LFX already publishes. These
    metric families are linked, never recomputed."""

    def test_names_every_metric_family_it_is_deliberately_not_collecting(self):
        block = aggregate.lfx_insights()

        families = {entry["metric"] for entry in block["see_lfx_instead"]}
        self.assertIn("contributors_by_employer", families)
        self.assertIn("active_maintainers", families)
        self.assertIn("meeting_attendance", families)
        self.assertIn("scorecard", families)
        self.assertIn("contributor_retention", families)

    def test_every_delegated_metric_carries_a_link_and_no_value(self):
        block = aggregate.lfx_insights()

        for entry in block["see_lfx_instead"]:
            self.assertTrue(entry["url"].startswith("https://insights.linuxfoundation.org/"))
            self.assertNotIn("value", entry)

    def test_exposes_the_dashboard_link_the_report_should_point_readers_at(self):
        block = aggregate.lfx_insights()

        self.assertTrue(block["project_url"].startswith("https://insights.linuxfoundation.org/"))


class WindowBoundsTest(unittest.TestCase):
    def test_a_ninety_day_window_ends_on_the_given_day(self):
        start, end = aggregate.window_bounds("2026-11-17", 90)

        self.assertEqual("2026-11-17", end)
        self.assertEqual("2026-08-19", start)


class BotDetectionTest(unittest.TestCase):
    def test_graphql_bot_accounts_are_bots(self):
        self.assertTrue(aggregate.is_bot("copilot-pull-request-reviewer", typename="Bot"))

    def test_logins_ending_in_the_bot_suffix_are_bots(self):
        self.assertTrue(aggregate.is_bot("dependabot[bot]"))

    def test_known_app_accounts_without_the_suffix_are_bots(self):
        self.assertTrue(aggregate.is_bot("coderabbitai"))

    def test_a_person_is_not_a_bot(self):
        self.assertFalse(aggregate.is_bot("jpower432"))

    def test_a_missing_author_is_treated_as_a_bot_so_it_never_inflates_human_counts(self):
        self.assertTrue(aggregate.is_bot(None))


if __name__ == "__main__":
    unittest.main()
