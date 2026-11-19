"""Tests for turning GraphQL payloads into the flat records aggregate wants."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from gemara_metrics import normalise


class PullRequestTest(unittest.TestCase):
    def test_flattens_the_author_and_tags_humans(self):
        node = {
            "createdAt": "2026-10-01T00:00:00Z",
            "mergedAt": "2026-10-02T00:00:00Z",
            "author": {"login": "jpower432", "__typename": "User"},
        }

        result = normalise.pull_request(node, "gemara")

        self.assertEqual("jpower432", result["author"])
        self.assertFalse(result["author_is_bot"])
        self.assertEqual("gemara", result["repo"])

    def test_a_deleted_author_comes_through_without_crashing(self):
        node = {"createdAt": "2026-10-01T00:00:00Z", "mergedAt": None, "author": None}

        result = normalise.pull_request(node, "gemara")

        self.assertIsNone(result["author"])
        self.assertTrue(result["author_is_bot"])


class IssueTest(unittest.TestCase):
    def test_flattens_comments_with_their_authors(self):
        node = {
            "createdAt": "2026-10-01T00:00:00Z",
            "author": {"login": "asker", "__typename": "User"},
            "comments": {"nodes": [
                {"createdAt": "2026-10-03T00:00:00Z", "author": {"login": "dependabot[bot]", "__typename": "Bot"}},
            ]},
        }

        result = normalise.issue(node, "gemara")

        self.assertEqual("asker", result["author"])
        self.assertTrue(result["comments"][0]["author_is_bot"])


class ReviewsInWindowTest(unittest.TestCase):
    def test_keeps_only_reviews_submitted_inside_the_window(self):
        prs = [{
            "reviews": {"nodes": [
                {"submittedAt": "2026-09-01T00:00:00Z", "author": {"login": "a", "__typename": "User"}},
                {"submittedAt": "2026-01-01T00:00:00Z", "author": {"login": "b", "__typename": "User"}},
            ]},
        }]

        result = normalise.reviews_in_window(prs, "2026-08-19", "2026-11-17", "gemara")

        self.assertEqual(["a"], [r["author"] for r in result])


class RepoOverviewTest(unittest.TestCase):
    def test_reads_topics_license_and_counts_off_the_graphql_node(self):
        node = {
            "name": "gemara",
            "description": "spec",
            "forkCount": 31,
            "hasDiscussionsEnabled": False,
            "licenseInfo": {"spdxId": "Apache-2.0"},
            "repositoryTopics": {"nodes": [{"topic": {"name": "grc"}}]},
            "openIssues": {"totalCount": 34},
            "openPRs": {"totalCount": 39},
            "releases": {"totalCount": 30},
            "goodFirstIssues": {"totalCount": 0},
            "helpWanted": {"totalCount": 2},
            "contributing": {"__typename": "Blob"},
            "contributingDotGithub": None,
            "issueTemplates": None,
            "securityInsights": None,
            "securityInsightsDotGithub": None,
        }

        result = normalise.repo_overview(node)

        self.assertEqual(["grc"], result["topics"])
        self.assertEqual("Apache-2.0", result["license_spdx"])
        self.assertEqual(39, result["open_prs"])
        self.assertTrue(result["has_contributing"])
        self.assertFalse(result["has_issue_template"])
        self.assertFalse(result["has_security_insights"])

    def test_finds_community_files_in_the_dot_github_directory_too(self):
        node = {
            "name": "website",
            "description": None,
            "forkCount": 11,
            "hasDiscussionsEnabled": False,
            "licenseInfo": None,
            "repositoryTopics": {"nodes": []},
            "openIssues": {"totalCount": 8},
            "openPRs": {"totalCount": 19},
            "releases": {"totalCount": 0},
            "goodFirstIssues": {"totalCount": 0},
            "helpWanted": {"totalCount": 0},
            "contributing": None,
            "contributingDotGithub": {"__typename": "Blob"},
            "issueTemplates": None,
            "securityInsights": None,
            "securityInsightsDotGithub": {"__typename": "Blob"},
        }

        result = normalise.repo_overview(node)

        self.assertTrue(result["has_contributing"])
        self.assertTrue(result["has_security_insights"])
        self.assertIsNone(result["license_spdx"])


if __name__ == "__main__":
    unittest.main()
