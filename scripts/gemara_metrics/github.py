"""A small GitHub client over the standard library.

Everything this collector needs is public data on a public org, so the
workflow's built-in GITHUB_TOKEN is enough — no personal access token, no
secret to rotate. The one thing a PAT would buy is cross-org code search,
which is why spec adoption is tracked by hand in data/adopters.yml instead.

The HTTP call is injected so the pagination logic can be tested without a
network or a recorded cassette.
"""

import json
import time
import urllib.error
import urllib.request

GRAPHQL_URL = "https://api.github.com/graphql"
REST_URL = "https://api.github.com"
USER_AGENT = "gemara-community-health-collector"


class GitHubError(RuntimeError):
    pass


def urllib_transport(url, body, headers):
    """Default transport. Retries the handful of failures that are worth
    retrying and gives up loudly on the rest."""
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(url, data=data, headers=headers)
    last_error = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as error:
            # 403 here is nearly always secondary rate limiting, which clears.
            if error.code in (403, 429, 502, 503) and attempt < 3:
                last_error = error
                time.sleep(2 ** attempt * 5)
                continue
            raise GitHubError("{} {} for {}".format(error.code, error.reason, url)) from error
        except urllib.error.URLError as error:
            if attempt < 3:
                last_error = error
                time.sleep(2 ** attempt * 5)
                continue
            raise GitHubError("network failure for {}: {}".format(url, error)) from error
    raise GitHubError("gave up on {} after retries: {}".format(url, last_error))


def _dig(payload, path):
    """Walk a path of keys, stopping at the first null.

    A repository that was archived or renamed mid-run comes back as null
    rather than an error, and one of those should not end the collection.
    """
    node = payload
    for key in path:
        if node is None:
            return None
        node = node.get(key)
    return node


class Client:
    def __init__(self, token, transport=urllib_transport):
        if not token:
            raise GitHubError(
                "no token. In Actions set GH_TOKEN to ${{ secrets.GITHUB_TOKEN }}; "
                "locally export GH_TOKEN=$(gh auth token)."
            )
        self.token = token
        self.transport = transport

    def _headers(self):
        return {
            "Authorization": "bearer {}".format(self.token),
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        }

    def graphql(self, query, variables):
        payload = self.transport(GRAPHQL_URL, {"query": query, "variables": variables}, self._headers())
        if payload.get("errors"):
            messages = "; ".join(error.get("message", "?") for error in payload["errors"])
            raise GitHubError("GraphQL: {}".format(messages))
        return payload.get("data") or {}

    def paginate(self, query, variables, connection_path, page_size=100, stop_when=None):
        """Follow a GraphQL connection to the end and return every node.

        `connection_path` is the key path from `data` down to the connection
        holding `nodes` and `pageInfo`.

        `stop_when` takes a node and ends paging once it returns True for
        anything on the current page. Use it with a newest-first ordering to
        avoid walking the whole history for a 90-day window. The page that
        tripped it is still returned; callers filter afterwards.
        """
        collected = []
        cursor = None
        while True:
            page_vars = dict(variables)
            page_vars["cursor"] = cursor
            page_vars.setdefault("pageSize", page_size)
            data = self.graphql(query, page_vars)

            connection = _dig(data, connection_path)
            if connection is None:
                return collected

            nodes = connection.get("nodes") or []
            collected.extend(nodes)
            if stop_when is not None and any(stop_when(node) for node in nodes):
                return collected

            info = connection.get("pageInfo") or {}
            if not info.get("hasNextPage"):
                return collected
            cursor = info.get("endCursor")

    def rest(self, path, params=None):
        url = REST_URL + path
        if params:
            pairs = "&".join("{}={}".format(key, value) for key, value in params.items())
            url = "{}?{}".format(url, pairs)
        return self.transport(url, None, self._headers())
