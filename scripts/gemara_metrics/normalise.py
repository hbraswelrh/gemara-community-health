"""Flattens GraphQL nodes into the plain records the aggregation layer takes.

Keeping this separate from the client means the GraphQL shape can change
without touching any arithmetic, and the arithmetic can be tested without
knowing GraphQL exists.
"""

from .aggregate import is_bot


def _author(node):
    """GraphQL returns a null author for deleted accounts and for some
    app-authored content."""
    author = node.get("author") or {}
    login = author.get("login")
    return login, is_bot(login, author.get("__typename"))


def pull_request(node, repo):
    login, bot = _author(node)
    return {
        "repo": repo,
        "number": node.get("number"),
        "author": login,
        "author_is_bot": bot,
        "created_at": node.get("createdAt"),
        "merged_at": node.get("mergedAt"),
    }


def issue(node, repo):
    login, bot = _author(node)
    comments = []
    for comment in (node.get("comments") or {}).get("nodes") or []:
        comment_login, comment_bot = _author(comment)
        comments.append({
            "author": comment_login,
            "author_is_bot": comment_bot,
            "created_at": comment.get("createdAt"),
        })
    return {
        "repo": repo,
        "number": node.get("number"),
        "author": login,
        "author_is_bot": bot,
        "created_at": node.get("createdAt"),
        "comments": comments,
    }


def reviews_in_window(pr_nodes, window_start, window_end, repo):
    """Every review submitted in the window, flattened across pull requests."""
    out = []
    for pr in pr_nodes:
        for review in (pr.get("reviews") or {}).get("nodes") or []:
            submitted = review.get("submittedAt")
            if not submitted or not window_start <= submitted[:10] <= window_end:
                continue
            login, bot = _author(review)
            out.append({
                "repo": repo,
                "author": login,
                "author_is_bot": bot,
                "submitted_at": submitted,
            })
    return out


def _present(*objects):
    return any(obj for obj in objects)


def _count(node, key):
    return (node.get(key) or {}).get("totalCount", 0)


def repo_overview(node):
    return {
        "name": node.get("name"),
        "description": node.get("description"),
        "topics": [t["topic"]["name"] for t in (node.get("repositoryTopics") or {}).get("nodes") or []],
        "license_spdx": (node.get("licenseInfo") or {}).get("spdxId"),
        "has_discussions": bool(node.get("hasDiscussionsEnabled")),
        "has_contributing": _present(node.get("contributing"), node.get("contributingDotGithub")),
        "has_issue_template": _present(node.get("issueTemplates")),
        "has_security_insights": _present(
            node.get("securityInsights"), node.get("securityInsightsDotGithub")
        ),
        "good_first_issues": _count(node, "goodFirstIssues"),
        "help_wanted": _count(node, "helpWanted"),
        "forks": node.get("forkCount", 0),
        "open_issues": _count(node, "openIssues"),
        "open_prs": _count(node, "openPRs"),
        "releases": _count(node, "releases"),
    }
