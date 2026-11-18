"""Pure aggregation over GitHub payloads.

Nothing in here touches the network. The client layer hands these functions
plain dicts and they hand back the numbers that go into the report, which
keeps the arithmetic testable without recording HTTP traffic.
"""

import statistics
from datetime import datetime, timedelta, timezone

SECONDS_PER_DAY = 86400.0
SECONDS_PER_HOUR = 3600.0


def _instant(timestamp):
    """Parse an ISO-8601 instant. GitHub hands us a trailing Z, which
    datetime.fromisoformat only learned to read in 3.11."""
    return datetime.fromisoformat(timestamp.replace("Z", "+00:00")).astimezone(timezone.utc)


def _day(timestamp):
    """Trim an ISO-8601 instant down to its calendar date."""
    return timestamp[:10]


def new_contributors(prs, window_start, window_end):
    """Authors whose first-ever merged PR landed inside the window.

    `prs` must span all of history, not just the window — an author only
    counts as new if nothing of theirs merged before it.
    """
    first_merge = {}
    for item in prs:
        if item.get("author_is_bot"):
            continue
        if not item.get("merged_at"):
            continue
        login = item["author"]
        day = _day(item["merged_at"])
        if login not in first_merge or day < first_merge[login]:
            first_merge[login] = day

    cohort = [
        {"login": login, "first_merge": day}
        for login, day in first_merge.items()
        if window_start <= day <= window_end
    ]
    cohort.sort(key=lambda entry: (entry["first_merge"], entry["login"]))
    return cohort


def first_human_response(issue):
    """Seconds until the first comment from someone other than the issue
    author and not a bot, or None if nobody ever replied."""
    replies = [
        comment
        for comment in issue.get("comments", [])
        if not comment.get("author_is_bot") and comment.get("author") != issue.get("author")
    ]
    if not replies:
        return None
    earliest = min(_instant(comment["created_at"]) for comment in replies)
    return (earliest - _instant(issue["created_at"])).total_seconds()


def responsiveness(issues):
    """How long a newcomer waits before a human says anything back."""
    waits = []
    unanswered = 0
    for item in issues:
        seconds = first_human_response(item)
        if seconds is None:
            unanswered += 1
        else:
            waits.append(seconds / SECONDS_PER_DAY)

    return {
        "opened": len(issues),
        "unanswered": unanswered,
        "unanswered_pct": round(100.0 * unanswered / len(issues), 1) if issues else None,
        "median_days_to_first_response": round(statistics.median(waits), 1) if waits else None,
    }


def merge_velocity(prs):
    """Time from opening a PR to getting it merged.

    Dependabot merges in seconds and would drag the median to nothing, so
    bots are counted but kept out of the timing.
    """
    hours = []
    human_merged = 0
    bot_merged = 0
    for item in prs:
        if not item.get("merged_at"):
            continue
        if item.get("author_is_bot"):
            bot_merged += 1
            continue
        human_merged += 1
        delta = _instant(item["merged_at"]) - _instant(item["created_at"])
        hours.append(delta.total_seconds() / SECONDS_PER_HOUR)

    return {
        "human_merged": human_merged,
        "bot_merged": bot_merged,
        "median_hours_to_merge": round(statistics.median(hours), 1) if hours else None,
    }


def review_concentration(reviews, top_n=3):
    """How much of the review load sits on how few people — the bus factor.

    Bots review plenty but cannot approve on anyone's behalf, so they are
    reported alongside rather than folded into the share.
    """
    tally = {}
    bot_reviews = 0
    for item in reviews:
        if item.get("author_is_bot"):
            bot_reviews += 1
            continue
        tally[item["author"]] = tally.get(item["author"], 0) + 1

    human_reviews = sum(tally.values())
    ranked = sorted(tally.items(), key=lambda kv: (-kv[1], kv[0]))
    top = ranked[:top_n]
    top_total = sum(count for _, count in top)

    return {
        "human_reviews": human_reviews,
        "bot_reviews": bot_reviews,
        "top_n": top_n,
        "top_n_share_pct": round(100.0 * top_total / human_reviews, 1) if human_reviews else None,
        "top_reviewers": [
            {
                "login": login,
                "reviews": count,
                "share_pct": round(100.0 * count / human_reviews, 1),
            }
            for login, count in top
        ],
        "reviewers_total": len(tally),
    }


RECOGNISED_LICENCE_MISSING = {None, "", "NOASSERTION", "NONE", "other"}


def ease_of_entry(repos):
    """What a first-time contributor runs into before they can contribute.

    Every gap here is cheap to close, which is the point of tracking them
    separately from the activity numbers.
    """
    rows = []
    for item in repos:
        gaps = []
        if not item.get("topics"):
            gaps.append("no_topics")
        if not item.get("description"):
            gaps.append("no_description")
        if (item.get("license_spdx") or None) in RECOGNISED_LICENCE_MISSING:
            gaps.append("no_license")
        if not item.get("has_contributing"):
            gaps.append("no_contributing")
        if not item.get("has_issue_template"):
            gaps.append("no_issue_template")
        if not item.get("has_discussions"):
            gaps.append("no_discussions")
        if not item.get("has_security_insights"):
            gaps.append("no_security_insights")
        rows.append({
            "name": item["name"],
            "good_first_issues": item.get("good_first_issues", 0),
            "gaps": gaps,
        })

    with_insights = sum(1 for item in repos if item.get("has_security_insights"))
    return {
        "repos": rows,
        "good_first_issues_total": sum(row["good_first_issues"] for row in rows),
        "repos_without_topics": sum(1 for row in rows if "no_topics" in row["gaps"]),
        "security_insights_coverage": "{}/{}".format(with_insights, len(repos)),
    }


# LFX Insights already publishes these, and it has access to data the GitHub
# API will not give us (employer affiliation, meeting attendance, merge
# rights). Recomputing a worse version from public events would put two
# different numbers for the same thing in front of the same reader, so the
# collector links out instead. Each entry deliberately carries no value.
LFX_PROJECT_URL = (
    "https://insights.linuxfoundation.org/project/openssf/repository/ossf_gemara"
    "?timeRange=past365days"
)

LFX_DELEGATED = [
    ("contributors_by_employer", "Which companies are funding the work", "Contributors → Organizations"),
    ("active_maintainers", "Who currently holds merge rights", "Contributors → Maintainers"),
    ("meeting_attendance", "Community meeting turnout over time", "Community → Meetings"),
    ("scorecard", "OpenSSF Scorecard result per repository", "Security → Scorecard"),
    ("contributor_retention", "How many contributors come back next quarter", "Contributors → Retention"),
]


def lfx_insights(project_url=LFX_PROJECT_URL):
    """Pointers to the metrics LFX owns, so the report can link rather than
    restate them.

    Coverage is currently one repository under the pre-rename `ossf/gemara`
    path, which is itself worth reporting — see `coverage_note`.
    """
    return {
        "project_url": project_url,
        "coverage_note": (
            "LFX Insights tracks 1 of the org's repositories, still filed under the "
            "pre-rename path ossf/gemara. Numbers there describe that repo only."
        ),
        "see_lfx_instead": [
            {"metric": metric, "description": description, "where": where, "url": project_url}
            for metric, description, where in LFX_DELEGATED
        ],
    }


# Accounts that act like bots without carrying the [bot] suffix on every
# surface. Extend this rather than special-casing at a call site.
KNOWN_BOT_LOGINS = {
    "dependabot",
    "coderabbitai",
    "github-actions",
    "copilot-pull-request-reviewer",
    "copilot",
    "kusari-inspector",
    "renovate",
}


def is_bot(login, typename=None):
    """A missing author means a deleted or hidden account. Counting it as a
    bot keeps it out of the human totals, which is the safer direction to
    be wrong in."""
    if login is None:
        return True
    if typename == "Bot":
        return True
    if login.endswith("[bot]"):
        return True
    return login.lower() in KNOWN_BOT_LOGINS


def window_bounds(end_day, days):
    """Inclusive calendar bounds for a rolling window ending on `end_day`."""
    end = _instant(end_day + "T00:00:00Z")
    start = end - timedelta(days=days)
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")
