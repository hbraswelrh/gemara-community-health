"""Tests for the GitHub client.

The HTTP boundary is injected rather than mocked at the library level: each
test hands the client a transport that returns real-shaped GitHub payloads,
so the pagination and error handling under test are the production paths.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from gemara_metrics import github


class RecordingTransport:
    """Replays a scripted list of responses and remembers what it was sent."""

    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def __call__(self, url, body, headers):
        self.calls.append({"url": url, "body": body, "headers": headers})
        return self.responses.pop(0)


def page(nodes, has_next=False, cursor=None):
    return {
        "data": {
            "repository": {
                "items": {
                    "nodes": nodes,
                    "pageInfo": {"hasNextPage": has_next, "endCursor": cursor},
                }
            }
        }
    }


class GraphQLPaginationTest(unittest.TestCase):
    def test_returns_the_nodes_from_a_single_page(self):
        transport = RecordingTransport([page([{"number": 1}])])
        client = github.Client(token="t", transport=transport)

        nodes = client.paginate("query", {}, ["repository", "items"])

        self.assertEqual([{"number": 1}], nodes)

    def test_follows_the_cursor_until_the_last_page(self):
        transport = RecordingTransport([
            page([{"number": 1}], has_next=True, cursor="CUR1"),
            page([{"number": 2}]),
        ])
        client = github.Client(token="t", transport=transport)

        nodes = client.paginate("query", {}, ["repository", "items"])

        self.assertEqual([{"number": 1}, {"number": 2}], nodes)

    def test_passes_the_previous_cursor_into_the_next_request(self):
        transport = RecordingTransport([
            page([{"number": 1}], has_next=True, cursor="CUR1"),
            page([{"number": 2}]),
        ])
        client = github.Client(token="t", transport=transport)

        client.paginate("query", {"owner": "gemaraproj"}, ["repository", "items"])

        self.assertIsNone(transport.calls[0]["body"]["variables"]["cursor"])
        self.assertEqual("CUR1", transport.calls[1]["body"]["variables"]["cursor"])

    def test_sends_the_token_as_a_bearer_credential(self):
        transport = RecordingTransport([page([])])
        client = github.Client(token="secret-token", transport=transport)

        client.paginate("query", {}, ["repository", "items"])

        self.assertEqual("bearer secret-token", transport.calls[0]["headers"]["Authorization"])

    def test_raises_when_graphql_reports_an_error(self):
        transport = RecordingTransport([{"errors": [{"message": "Bad credentials"}]}])
        client = github.Client(token="t", transport=transport)

        with self.assertRaises(github.GitHubError) as caught:
            client.paginate("query", {}, ["repository", "items"])

        self.assertIn("Bad credentials", str(caught.exception))

    def test_treats_a_null_repository_as_empty_rather_than_crashing(self):
        """A repo can vanish or be archived between the repo list and the
        per-repo query. That should not take down the whole run."""
        transport = RecordingTransport([{"data": {"repository": None}}])
        client = github.Client(token="t", transport=transport)

        self.assertEqual([], client.paginate("query", {}, ["repository", "items"]))


class EarlyStopTest(unittest.TestCase):
    """Issues come back newest-first. Once a page predates the window there
    is nothing left worth paging through, and the whole point is to not
    walk years of history to build a 90-day report."""

    def test_stops_paging_once_the_predicate_says_the_page_is_too_old(self):
        transport = RecordingTransport([
            page([{"createdAt": "2026-10-01"}], has_next=True, cursor="CUR1"),
            page([{"createdAt": "2024-01-01"}], has_next=True, cursor="CUR2"),
        ])
        client = github.Client(token="t", transport=transport)

        nodes = client.paginate(
            "query", {}, ["repository", "items"],
            stop_when=lambda node: node["createdAt"] < "2026-08-19",
        )

        self.assertEqual(2, len(transport.calls))
        self.assertEqual(["2026-10-01", "2024-01-01"], [n["createdAt"] for n in nodes])


class TokenRequirementTest(unittest.TestCase):
    def test_refuses_to_start_without_a_token(self):
        with self.assertRaises(github.GitHubError):
            github.Client(token="", transport=RecordingTransport([]))


if __name__ == "__main__":
    unittest.main()
